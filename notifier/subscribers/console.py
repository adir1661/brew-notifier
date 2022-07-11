from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notifier.models import Entity

import logging

from notifier.subscribers.base_subscriber import BaseSubscriber

default_logger = logging.getLogger("default")


class ConsoleSubscriber(BaseSubscriber):
    entity: Entity

    def notify(self, options: dict):
        if options.get("log_message"):
            default_logger.info(self.get_message())

    def get_message(self):
        return (
            f"{self.entity.__class__.__name__.lower()} {self.entity.name} has changed"
        )
