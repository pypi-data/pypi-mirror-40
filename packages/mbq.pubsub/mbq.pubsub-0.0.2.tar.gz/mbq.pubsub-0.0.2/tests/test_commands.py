from unittest import mock

import pytest
from mbq.pubsub.settings import project_settings

from django.core.management import CommandError, call_command
from django.test import TestCase


class CommandTest(TestCase):
    def test_command_required(self):
        with pytest.raises(CommandError) as excinfo:
            call_command("pubsub")
        assert "the following arguments are required" in str(excinfo.value)


class ConsumeCommandTest(TestCase):
    def test_require_queue(self):
        with pytest.raises(CommandError) as excinfo:
            call_command("pubsub", "consume")

        assert "the following arguments are required" in str(excinfo.value)
        assert "-q/--queue" in str(excinfo.value)

    @project_settings(QUEUES=["my-queue"])
    def test_queue_choices(self):
        with pytest.raises(CommandError) as excinfo:
            call_command("pubsub", "consume", "--queue", "other-queue")

        assert "-q/--queue: invalid choice" in str(excinfo.value)

    @project_settings(QUEUES=["queue"])
    def test_consume(self):
        MockConsumerClass = mock.MagicMock()
        with project_settings(CONSUMER_CLASS=MockConsumerClass):
            call_command("pubsub", "consume", "--queue", "queue")

        self.assertEqual(MockConsumerClass.call_args[0][0], "queue")
        self.assertEqual(MockConsumerClass().consume.call_count, 1)


class ReplayCommandTest(TestCase):
    def test_require_queue(self):
        with pytest.raises(CommandError) as excinfo:
            call_command("pubsub", "replay")

        assert "the following arguments are required" in str(excinfo.value)
        assert "-q/--queue" in str(excinfo.value)

    @project_settings(QUEUES=["my-queue"])
    def test_queue_choices(self):
        with pytest.raises(CommandError) as excinfo:
            call_command("pubsub", "replay", "--queue", "other-queue")

        assert "-q/--queue: invalid choice" in str(excinfo.value)

    @project_settings(QUEUES=["queue"])
    def test_consume(self):
        MockConsumerClass = mock.MagicMock()
        with project_settings(CONSUMER_CLASS=MockConsumerClass):
            call_command("pubsub", "replay", "--queue", "queue", "5")

        self.assertEqual(MockConsumerClass.call_args[0][0], "queue")
        self.assertEqual(MockConsumerClass.call_args[0][0], "queue")
        self.assertEqual(MockConsumerClass().replay_dead_letter_queue.call_count, 1)
        self.assertEqual(MockConsumerClass().replay_dead_letter_queue.call_args[0][0], 5)
