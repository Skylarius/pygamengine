from __future__ import annotations

from pygamengine.event import EventData, EventType
from .event import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gameobject import GameObject

ColliderEnabledChangedEventType: EventType = "collider_enabled_changed"
NewObjectCreatedEventType: EventType = "new_object_created"
ObjectDeletedEventType: EventType = "object_deleted"

class ColliderEnabledChangedData(EventData):
    def __init__(self, game_object: GameObject, condition: bool) -> None:
        super().__init__((game_object, condition))
    
    def get_game_object(self):
        return self.data[0]

    def get_condition(self):
        return self.data[1]
    

class ColliderEnabledChanged(Event):
    def __init__(self, game_object: GameObject, condition: bool) -> None:
        super().__init__(ColliderEnabledChangedEventType, ColliderEnabledChangedData(game_object, condition))

class GameObjectData(EventData):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(game_object)
    
    def get_game_object(self):
        return self.data

class NewObjectCreated(Event):
    event_type = NewObjectCreatedEventType
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(NewObjectCreated.event_type, GameObjectData(game_object))

class ObjectDeleted(Event):
    event_type = ObjectDeletedEventType
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(ObjectDeleted.event_type, GameObjectData(game_object))