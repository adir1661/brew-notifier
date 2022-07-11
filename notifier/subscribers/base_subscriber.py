from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notifier.models import Entity

from abc import ABC, abstractmethod, ABCMeta


class BaseSubscriber(ABC):
    entity: Entity

    def __init__(self, entity: Entity):
        self.entity = entity

    @abstractmethod
    def notify(self, options: dict):
        raise NotImplementedError()
