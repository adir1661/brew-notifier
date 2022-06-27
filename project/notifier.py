from typing import Dict, Optional
import logging
from project.managers import EntityManagers, EntityManager
from project.entities import Entity
from brew_common.brew_logger.decorators import logger


# should move to app settings.
default_logger = logging.getLogger("default")
default_logger.setLevel(logging.INFO)

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
        entity=entity_obj or original_entity_obj
    )
    if entity_manager.test_conditions(entity_obj, original_entity_obj):
        notified_entity = entity_manager.get_notified_entity()

        # todo: implement a generic way to activate 3rd party actions with list or something similar.
        if options.get("log_message"):
            default_logger.info(entity_manager.get_message())

        return notified_entity
