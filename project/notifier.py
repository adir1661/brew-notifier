from project.entities import CRAWLING_STATUSES


def check_deleted(entity_obj, original_entity_obj):
    return entity_obj is None


def check_created(entity_obj, original_entity_obj):
    return original_entity_obj is None


def check_is_deleted_changed(entity_obj, original_entity_obj):
    return entity_obj.is_deleted != original_entity_obj.is_deleted


def check_text_crawling_status_changed(entity_obj, original_entity_obj):
    return entity_obj.crawling_status != original_entity_obj.crawling_status and entity_obj.crawling_status in [
        CRAWLING_STATUSES.TEXT_ANALYZED, CRAWLING_STATUSES.TEXT_UPLOADED]


def check_is_blacklisted_changed(entity_obj, original_entity_obj):
    return entity_obj.is_blacklisted != original_entity_obj.is_blacklisted


class ContidionCallbacks:
    check_deleted = check_deleted
    check_created = check_created
    check_is_deleted_changed = check_is_deleted_changed
    check_text_crawling_status_changed = check_text_crawling_status_changed
    check_is_blacklisted_changed = check_is_blacklisted_changed


created_deleted = [ContidionCallbacks.check_created, ContidionCallbacks.check_deleted]
all_conditions = created_deleted + [ContidionCallbacks.check_is_deleted_changed, ContidionCallbacks.check_is_blacklisted_changed,
                                    ContidionCallbacks.check_text_crawling_status_changed]

EntityManagers = {
    "Event": {
        "conditions_callbacks": all_conditions,
        "message": lambda event: f'event {event.name} has changed'
    },
    "Company": {
        "conditions_callbacks": created_deleted + [ContidionCallbacks.check_is_deleted_changed,
                                                   ContidionCallbacks.check_text_crawling_status_changed],
        "message": lambda company: f'company {company.name} has changed'
    },
    "Webinar": {
        "conditions_callbacks": all_conditions,
        "message": lambda webinar: f'webinar {webinar.name} has changed'
    },
    "ContentItem": {
        "conditions_callbacks": all_conditions,
        "message": lambda content_item: f'company {content_item.company.name} has changed'
    },
    "CompanyForEvent": {
        "conditions_callbacks": created_deleted + [ContidionCallbacks.check_is_deleted_changed,
                                                   ContidionCallbacks.check_is_blacklisted_changed],
        "message": lambda company_for_event: f'event {company_for_event.event.name} has changed'
    },
    "CompanyForWebinar": {
        "conditions_callbacks": created_deleted + [ContidionCallbacks.check_is_deleted_changed,
                                                   ContidionCallbacks.check_is_blacklisted_changed],
        "message": lambda company_for_webinar: f'webinar {company_for_webinar.webinar.name} has changed'
    },
    "CompanyCompetitor": {
        "conditions_callbacks": created_deleted + [ContidionCallbacks.check_is_deleted_changed],
        "message": lambda content_item: f'company {content_item.company.name} has changed'
    }
}


def notification_reducer(*, entity_obj, original_entity_obj, entity_type):
    entity_manager = EntityManagers[entity_type]
    if any(condition_check(entity_obj, original_entity_obj) for condition_check in entity_manager['conditions_callbacks']):
        print(entity_manager['message'](entity_obj or original_entity_obj))
