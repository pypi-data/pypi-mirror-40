from .settings import project_settings


def construct_full_queue_name(queue_name):
    return f"mbq-{project_settings.SERVICE}-{queue_name}-{project_settings.ENV.short_name}"
