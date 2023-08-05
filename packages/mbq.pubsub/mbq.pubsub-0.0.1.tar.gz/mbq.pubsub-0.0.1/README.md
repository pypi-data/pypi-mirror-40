# mbq.pubsub

[![PyPI Version](https://img.shields.io/pypi/v/mbq.pubsub.svg)](repo)
[![PyPI License](https://img.shields.io/pypi/l/mbq.pubsub.svg)](repo)
[![Python Versions](https://img.shields.io/pypi/pyversions/mbq.pubsub.svg)](repo)
[![Travis CI Status](https://img.shields.io/travis/managedbyq/mbq.pubsub/master.svg)](repo)

[repo]: https://pypi.python.org/pypi/mbq.pubsub


## Installation

```bash
$ pip install mbq.pubsub
🚀✨
```

Guaranteed fresh.

## Configuration

```python
# settings.py

SERVICE_NAME = "my-service"

PUBSUB = {
    "ENV": mbq.get_environment("ENV_NAME"),
    "SERVICE": SERVICE_NAME,
    "QUEUES": [
        "foo-updates",
        "bar-updates",
    ],
    "MESSAGE_HANDLERS": {
        "foo.updated": "path.to.handlers.handle_foo_updated",
        "bar.updated": "path.to.handlers.handle_bar_updated",
    },
}
```

```yaml
# convox.yml

services:
  foo-consumer:
    image: {{DOCKER_IMAGE_NAME}}
    command: newrelic-admin run-python -m manage pubsub consume --queue foo-updates
    init: true
    environment:
      - "*"

  bar-consumer:
    image: {{DOCKER_IMAGE_NAME}}
    command: newrelic-admin run-python -m manage pubsub consume --queue bar-updates
    init: true
    environment:
      - "*"
```
