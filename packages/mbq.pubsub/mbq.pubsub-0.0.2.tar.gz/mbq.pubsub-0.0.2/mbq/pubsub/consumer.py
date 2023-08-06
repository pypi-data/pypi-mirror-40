import json
import logging

from mbq import metrics

import boto3
import rollbar
from django.db import close_old_connections

from . import _collector as collector
from . import exceptions
from .settings import project_settings

logger = logging.getLogger(__name__)

NOT_PROVIDED = object()


class Consumer:
    def __init__(self, queue_name: str):
        self._queue_full_name = (
            f"mbq-{project_settings.SERVICE}-{queue_name}-{project_settings.ENV.short_name}"
        )

    @property
    def queue(self):
        if not hasattr(self, "_queue"):
            sqs = boto3.resource("sqs")
            self._queue = sqs.get_queue_by_name(QueueName=self._queue_full_name)
        return self._queue

    @property
    def dead_letter_queue(self):
        """
        Find the dead letter queue from the primary queue's redrive policy.

        https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html
        """

        if not hasattr(self, "_dead_letter_queue"):
            try:
                redrive_policy = json.loads(self.queue.attributes["RedrivePolicy"])
                dlq_name = redrive_policy["deadLetterTargetArn"].split(":")[-1]
            except Exception as e:
                raise exceptions.ConsumerException(
                    f"No dead letter queue configured for {self.queue}"
                ) from e

            sqs = boto3.resource("sqs")
            self._dead_letter_queue = sqs.get_queue_by_name(QueueName=dlq_name)
        return self._dead_letter_queue

    def consume(self):
        # the logging serves two purposes: give the user some feedback
        # that the service is probably configured correctly and force
        # all of the message handlers to be imported (so we know they're
        # importable).
        logger.info(f"Found {len(project_settings.MESSAGE_HANDLERS)} message handlers.")

        while True:
            collector.increment("sqs.receive.attempt_read")
            messages = self.queue.receive_messages(WaitTimeSeconds=20, MaxNumberOfMessages=10)
            # Sends heartbeat metric. Datadog should be configured to alert
            # if it doesn't receive this metric for some period of time.
            # Make sure this time period is longer than the WaitTimeSeconds above
            collector.service_check("sqs.receive.Consumer Heartbeat", metrics.OK)
            if len(messages) > 0:
                logger.info(f"Received {len(messages)} messages")

            for message in messages:
                try:
                    body = json.loads(message.body)
                    data = json.loads(body["Message"])
                    message_type = data["message_type"]
                    payload = data["payload"]
                except Exception:
                    rollbar.report_exc_info()
                    continue

                try:
                    handler = project_settings.MESSAGE_HANDLERS.get(message_type)

                    if handler:
                        logger.info(f"Processing {message_type} message")
                        handler(payload)
                        logger.info(f"Done processing {message_type} message")

                        collector.increment(
                            "sqs.receive.processed",
                            tags={"result": "succeeded", "type": message_type},
                        )

                    else:
                        logger.info(
                            f"Received unregistered message_type: {message_type} \n"
                            f"Message body: {body}"
                        )
                        collector.increment(
                            "sqs.receive.processed",
                            tags={"result": "skipped", "type": message_type},
                        )

                except Exception:
                    logger.exception("An error occurred while processing the message.")
                    collector.increment(
                        "sqs.receive.processed", tags={"result": "failed", "type": message_type}
                    )

                    rollbar.report_exc_info()
                else:
                    message.delete()

        # django only cleans up db connections when handling the "request_finished" signal
        # so we want to make sure it happens regularly here in the long-lived consumer
        close_old_connections()

    def replay_dead_letter_queue(self, max_messages: int):
        if max_messages < 1:
            raise exceptions.ConsumerException("max_messages must be greater than 0")

        logger.info(
            f"Replaying at most {max_messages} messages "
            f"from {self.dead_letter_queue} to {self.queue}"
        )

        messages_processed = 0
        while True:
            messages = self.dead_letter_queue.receive_messages(
                WaitTimeSeconds=20, MaxNumberOfMessages=10
            )

            for message in messages:
                self.queue.send_message(MessageBody=message.body)
                message.delete()
                messages_processed += 1

                if messages_processed >= max_messages:
                    return
