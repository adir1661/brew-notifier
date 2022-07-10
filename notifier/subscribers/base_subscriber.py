from abc import ABC, abstractmethod, ABCMeta

from project.entities import Entity


class BaseSubscriber(ABC):
    entity: Entity

    def __init__(self, entity: Entity):
        self.entity = entity

    @abstractmethod
    def notify(self, options: dict):
        raise NotImplementedError()
