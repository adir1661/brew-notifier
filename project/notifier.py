from typing import Dict, Optional, List
import logging
from project.managers import EntityManagers, EntityManager
from project.entities import Entity
from brew_common.brew_logger.decorators import logger


# should move to app settings.
from project.subscribers.base_subscriber import SubscriberClass
from project.subscribers.console import ConsoleSubscriber

default_logger = logging.getLogger("default")
default_logger.setLevel(logging.INFO)

Subscribers: List[SubscriberClass] = [ConsoleSubscriber]

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

STREAM = False
FILE = True

if FILE:
    file_handler = logging.FileHandler("./notifier.log")
    file_handler.setFormatter(formatter)
    default_logger.addHandler(file_handler)

if STREAM:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    default_logger.addHandler(stream_handler)


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
