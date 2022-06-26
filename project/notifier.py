from typing import Dict, Optional

from project.Managers import EntityManagers, EntityManager
from project.entities import Entity


def notification_reducer(
    *,
    entity_obj: Optional[Entity],
    original_entity_obj: Optional[Entity],
    entity_type: str
):
    entity_manager_class = EntityManagers[entity_type]
    entity_manager = entity_manager_class(entity=entity_obj or original_entity_obj)
    if entity_manager.test_conditions(entity_obj , original_entity_obj):
        notified_entity = entity_manager.get_notified_entity()
        print(entity_manager.get_message())
        return notified_entity
