from mbq import metrics
from mbq.pubsub.settings import project_settings

from django.apps import AppConfig


class PubSubConfig(AppConfig):
    name = "mbq.pubsub"
    verbose_name = "PubSub"

    def ready(self):
        self.module._collector = metrics.Collector(
            namespace="mbq.pubsub",
            tags={"env": project_settings.ENV, "service": project_settings.SERVICE},
        )
