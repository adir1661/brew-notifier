from __future__ import annotations

from typing import Dict, Optional, List, TYPE_CHECKING
import logging
from notifier.managers import EntityManagers, EntityManager
if TYPE_CHECKING:
    from notifier.models import Entity
from brew_common.brew_logger.decorators import logger


# should move to app settings.
from notifier.subscribers.console import ConsoleSubscriber

default_logger = logging.getLogger("default")

Subscribers: List[type] = [ConsoleSubscriber]


@logger(logger_name="default", log_level="error", log_exit=True, log_params=True)
def notification_reducer(
    *,
    entity_obj: Optional[Entity],
    original_entity_obj: Optional[Entity],
    entity_type: str,
    options: Optional[Dict] = None
):
    options = options or {}
    entity_manager: EntityManager = EntityManagers[entity_type](
        entity=entity_obj, original_entity_obj=original_entity_obj
    )
    if entity_manager.test_conditions():
        notified_entity = entity_manager.get_notified_entity()
        for subscriber_class in Subscribers:
            subscriber = subscriber_class(notified_entity)
            subscriber.notify(options=options)
        return True
    return False
