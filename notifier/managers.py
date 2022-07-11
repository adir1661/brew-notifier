from __future__ import annotations

from abc import abstractmethod, ABC, ABCMeta
from enum import Enum
from functools import partial
from typing import Callable, List, Dict, TYPE_CHECKING

from notifier.consts import CRAWLING_STATUSES

if TYPE_CHECKING:
    from notifier.models import CrawlableModel, Entity


class TrackFields(Enum):
    IS_DELETED = "is_deleted"
    IS_BLACKLISTED = "is_blacklisted"


class ConditionFunctions:
    @staticmethod
    def check_deleted(entity_obj, original_entity_obj):
        return entity_obj is None

    @staticmethod
    def check_created(entity_obj, original_entity_obj):
        return original_entity_obj is None

    @staticmethod
    def check_text_crawling_status_changed(entity_obj, original_entity_obj):
        return (
            entity_obj.crawling_status != original_entity_obj.crawling_status
            and entity_obj.crawling_status
            in [CRAWLING_STATUSES.TEXT_ANALYZED, CRAWLING_STATUSES.TEXT_UPLOADED]
        )

    @staticmethod
    def check_field_changed(
        entity_obj, original_entity_obj, *, track_field: TrackFields
    ):
        field = getattr(entity_obj, track_field.value)
        original_field = getattr(original_entity_obj, track_field.value)
        return field != original_field


created_deleted = [ConditionFunctions.check_created, ConditionFunctions.check_deleted]
all_conditions = created_deleted + [
    ConditionFunctions.check_text_crawling_status_changed,
]


class EntityManager(ABC):
    entity_class: type = None
    entity: Entity = None
    original_entity_obj: Entity = None
    condition_functions: List[Callable] = None
    track_fields: List[TrackFields] = None

    def __init__(self, *, entity: Entity, original_entity_obj: Entity):
        self.entity = entity
        self.original_entity_obj = original_entity_obj

    @property
    def available_entity(self):
        return self.entity or self.original_entity_obj

    def test_conditions(self):
        test_field = partial(
            ConditionFunctions.check_field_changed,
            entity_obj=self.entity,
            original_entity_obj=self.original_entity_obj,
        )

        return any(
            cb(self.entity, self.original_entity_obj) for cb in self.condition_functions
        ) or any(test_field(field) for field in self.track)

    @abstractmethod
    def get_notified_entity(self) -> CrawlableModel:
        raise NotImplementedError()


class EventManager(EntityManager):
    condition_functions = all_conditions
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity


class CompanyManager(EntityManager):
    condition_functions = created_deleted + [
        ConditionFunctions.check_text_crawling_status_changed,
    ]
    track_fields = [TrackFields.IS_DELETED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity


class WebinarManager(EntityManager):
    condition_functions = all_conditions
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity


class ContentItemManager(EntityManager):
    condition_functions = all_conditions
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity.company


class CompanyForEventManager(EntityManager):
    condition_functions = created_deleted
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity.event


class CompanyForWebinarManager(EntityManager):
    condition_functions = created_deleted
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity.webinar


class CompanyCompetitorManager(EntityManager):
    condition_functions = created_deleted
    track_fields = [TrackFields.IS_DELETED]

    def get_notified_entity(self) -> CrawlableModel:
        return self.available_entity.company


EntityManagers: Dict[str, type] = {
    "Event": EventManager,
    "Company": CompanyManager,
    "Webinar": WebinarManager,
    "ContentItem": ContentItemManager,
    "CompanyForEvent": CompanyForEventManager,
    "CompanyForWebinar": CompanyForWebinarManager,
    "CompanyCompetitor": CompanyCompetitorManager,
}
