import logging

from mbq.pubsub.settings import project_settings

import django
from django.core.management.base import BaseCommand, CommandParser

import rollbar


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        # django fixed a long-standing annoyance in 2.1 so we only
        # need this hack if we're using a version before that.
        # SubParser inspired by:
        # https://stackoverflow.com/a/37414551/305736
        add_parsers_kwargs = {}
        if django.VERSION < (2, 1):
            command = self

            class SubParser(CommandParser):
                def __init__(self, **kwargs):
                    return super().__init__(command, **kwargs)

            add_parsers_kwargs["parser_class"] = SubParser

        queue_choices = sorted(project_settings.QUEUES)

        subparsers = parser.add_subparsers(dest="command", **add_parsers_kwargs)
        # we should be able to pass this to .add_subparsers above but
        # that kwarg is broken in Python 3.6
        subparsers.required = True

        consume_parser = subparsers.add_parser("consume")
        consume_parser.add_argument("-q", "--queue", required=True, choices=queue_choices)

        replay_parser = subparsers.add_parser("replay")
        replay_parser.add_argument("-q", "--queue", required=True, choices=queue_choices)
        replay_parser.add_argument("num_messages", type=int)

    def handle(self, **options):
        getattr(self, f'handle_{options["command"]}')(**options)

    def handle_consume(self, queue=None, **options):
        try:
            consumer = project_settings.CONSUMER_CLASS(queue)
            consumer.consume()
        except Exception:
            logger.exception("Consume failed")
            rollbar.report_exc_info()

    def handle_replay(self, queue=None, num_messages=None, **options):
        consumer = project_settings.CONSUMER_CLASS(queue)
        consumer.replay_dead_letter_queue(num_messages)
