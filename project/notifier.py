from typing import Dict, Optional

from project.managers import EntityManagers, EntityManager
from project.entities import Entity
from brew_common.brew_logger.decorators import logger


@logger(logger_name="notification_reducer", log_exit=True, log_params=True)
def notification_reducer(
    *,
    entity_obj: Optional[Entity],
    original_entity_obj: Optional[Entity],
    entity_type: str
):
    entity_manager: EntityManager = EntityManagers[entity_type](
        entity=entity_obj or original_entity_obj
    )
    if entity_manager.test_conditions(entity_obj, original_entity_obj):
        notified_entity = entity_manager.get_notified_entity()
        print(entity_manager.get_message())
        return notified_entity
