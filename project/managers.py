from abc import abstractmethod
from enum import Enum
from functools import partial
from typing import Callable, List, Dict

from project.entities import CRAWLING_STATUSES, Entity, CrawlableEntity


class TrackFields(Enum):
    IS_DELETED = 'is_deleted'
    IS_BLACKLISTED = 'is_blacklisted'
    
    
def check_field_changed(entity_obj, original_entity_obj, *, track_field: TrackFields):
    field = getattr(entity_obj, track_field.value)
    original_field = getattr(original_entity_obj, track_field.value)
    return field != original_field


def check_deleted(entity_obj, original_entity_obj):
    return entity_obj is None


def check_created(entity_obj, original_entity_obj):
    return original_entity_obj is None


def check_text_crawling_status_changed(entity_obj, original_entity_obj):
    return (
        entity_obj.crawling_status != original_entity_obj.crawling_status
        and entity_obj.crawling_status
        in [CRAWLING_STATUSES.TEXT_ANALYZED, CRAWLING_STATUSES.TEXT_UPLOADED]
    )


class ConditionCallbacks:
    check_deleted = check_deleted
    check_created = check_created
    check_text_crawling_status_changed = check_text_crawling_status_changed


created_deleted = [ConditionCallbacks.check_created, ConditionCallbacks.check_deleted]
all_conditions = created_deleted + [
    ConditionCallbacks.check_text_crawling_status_changed,
]


class EntityManagerClass(type):
    def __new__(mcs, *args, **kwargs):
        instance = type.__new__(mcs, *args, **kwargs)
        if getattr(instance, "track_fields"):
            instance.condition_functions += [
                partial(check_field_changed, track_field=track_field)
                for track_field in instance.track_fields
            ]

        return instance


class EntityManager(metaclass=EntityManagerClass):
    entity_class: type = None
    entity: Entity = None
    original_entity_obj: Entity = None
    condition_functions: List[Callable] = None
    track_fields: List[TrackFields] = None

    def __init__(self, *, entity: Entity,original_entity_obj: Entity):
        self.entity = entity
        self.original_entity_obj = original_entity_obj

    @property
    def available_entity(self):
        return self.entity or self.original_entity_obj

    def test_conditions(self):
        return any(
            cb(self.entity, self.original_entity_obj) for cb in self.condition_functions
        )

    @abstractmethod
    def get_notified_entity(self) -> CrawlableEntity:
        raise NotImplementedError()


class EventManager(EntityManager):
    condition_functions = all_conditions
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity


class CompanyManager(EntityManager):
    condition_functions = created_deleted + [
        ConditionCallbacks.check_text_crawling_status_changed,
    ]
    track_fields = [TrackFields.IS_DELETED]

    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity


class WebinarManager(EntityManager):
    condition_functions = all_conditions
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]


    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity


class ContentItemManager(EntityManager):
    condition_functions = all_conditions
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]


    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity.company


class CompanyForEventManager(EntityManager):
    condition_functions = created_deleted
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity.event


class CompanyForWebinarManager(EntityManager):
    condition_functions = created_deleted
    track_fields = [TrackFields.IS_DELETED, TrackFields.IS_BLACKLISTED]

    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity.webinar


class CompanyCompetitorManager(EntityManager):
    condition_functions = created_deleted
    track_fields = [TrackFields.IS_DELETED]

    def get_notified_entity(self) -> CrawlableEntity:
        return self.available_entity.company


EntityManagers: Dict[str, EntityManagerClass] = {
    "Event": EventManager,
    "Company": CompanyManager,
    "Webinar": WebinarManager,
    "ContentItem": ContentItemManager,
    "CompanyForEvent": CompanyForEventManager,
    "CompanyForWebinar": CompanyForWebinarManager,
    "CompanyCompetitor": CompanyCompetitorManager,
}
