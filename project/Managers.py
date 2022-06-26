from abc import abstractmethod
from typing import Callable, List, Dict

from project.entities import CRAWLING_STATUSES, Entity, CrawlableEntity


def check_deleted(entity_obj, original_entity_obj):
    return entity_obj is None


def check_created(entity_obj, original_entity_obj):
    return original_entity_obj is None


def check_is_deleted_changed(entity_obj, original_entity_obj):
    return entity_obj.is_deleted != original_entity_obj.is_deleted


def check_text_crawling_status_changed(entity_obj, original_entity_obj):
    return (
        entity_obj.crawling_status != original_entity_obj.crawling_status
        and entity_obj.crawling_status
        in [CRAWLING_STATUSES.TEXT_ANALYZED, CRAWLING_STATUSES.TEXT_UPLOADED]
    )


def check_is_blacklisted_changed(entity_obj, original_entity_obj):
    return entity_obj.is_blacklisted != original_entity_obj.is_blacklisted


class ConditionCallbacks:
    check_deleted = check_deleted
    check_created = check_created
    check_is_deleted_changed = check_is_deleted_changed
    check_text_crawling_status_changed = check_text_crawling_status_changed
    check_is_blacklisted_changed = check_is_blacklisted_changed


created_deleted = [ConditionCallbacks.check_created, ConditionCallbacks.check_deleted]
all_conditions = created_deleted + [
    ConditionCallbacks.check_is_deleted_changed,
    ConditionCallbacks.check_is_blacklisted_changed,
    ConditionCallbacks.check_text_crawling_status_changed,
]


class EntityManager:
    entity_class: type = None
    entity: Entity = None
    condition_callbacks: List[Callable] = None

    def __init__(self, *, entity: Entity):
        self.entity = entity

    def get_message(self):
        entity = self.get_notified_entity()
        return f"{entity.__class__.__name__} {entity.name} has changed"

    def test_conditions(self, entity_obj: Entity, original_entity_obj: Entity):
        return any(
            cb(entity_obj, original_entity_obj) for cb in self.condition_callbacks
        )

    @abstractmethod
    def get_notified_entity(self) -> CrawlableEntity:
        raise NotImplementedError()


class EventManager(EntityManager):
    condition_callbacks = all_conditions

    # def get_message(self):
    #     name = self.get_notified_entity().name
    #     return f"event {name} has changed"

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity


class CompanyManager(EntityManager):
    condition_callbacks = created_deleted + [
        ConditionCallbacks.check_is_deleted_changed,
        ConditionCallbacks.check_text_crawling_status_changed,
    ]

    # def get_message(self):
    #     name = self.get_notified_entity().name
    #     return f"company {name} has changed"

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity


class WebinarManager(EntityManager):
    condition_callbacks = all_conditions

    # def get_message(self):
    #     name = self.get_notified_entity().name
    #     return f"webinar {name} has changed"

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity


class ContentItemManager(EntityManager):
    condition_callbacks = all_conditions

    # def get_message(self):
    #     pass

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity.company


class CompanyForEventManager(EntityManager):
    condition_callbacks = created_deleted + [
        ConditionCallbacks.check_is_deleted_changed,
        ConditionCallbacks.check_is_blacklisted_changed,
    ]

    # def get_message(self):
    #     pass

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity.event


class CompanyForWebinarManager(EntityManager):
    condition_callbacks = created_deleted + [
        ConditionCallbacks.check_is_deleted_changed,
        ConditionCallbacks.check_is_blacklisted_changed,
    ]

    # def get_message(self):
    #     pass

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity.webinar


class CompanyCompetitorManager(EntityManager):
    condition_callbacks = created_deleted + [
        ConditionCallbacks.check_is_deleted_changed
    ]

    # def get_message(self):
    #     pass

    def get_notified_entity(self) -> CrawlableEntity:
        return self.entity.company


EntityManagers: Dict[str, EntityManager.__class__] = {
    "Event": EventManager,
    "Company": CompanyManager,
    "Webinar": WebinarManager,
    "ContentItem": ContentItemManager,
    "CompanyForEvent": CompanyForEventManager,
    "CompanyForWebinar": CompanyForWebinarManager,
    "CompanyCompetitor": CompanyCompetitorManager,
}
