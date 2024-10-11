from __future__ import annotations

from pygamengine.event import EventData, EventType
from pygamengine.components import Component
from .event import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gameobject import GameObject
    from pygamengine.coroutines import Coroutine
    from pygamengine.engine import PygameObject

ColliderEnabledChangedEventType: EventType = "collider_enabled_changed"
NewObjectCreatedEventType: EventType = "new_object_created"
ObjectDeletedEventType: EventType = "object_deleted"
ObjectLayerUpdatedEventType: EventType = "object_layer_updated"
ObjectStartedEventType: EventType = "object_started_event_type"
ComponentAddedToObjectEventType: EventType = "component_added_to_object"
CoroutineEndEventType: EventType = "coroutine_end"
VideoResizeEventType: EventType = "video_resize"


'''Collider Events'''
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

'''Game Object Events'''
class GameObjectData(EventData):
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(game_object)
    
    def get_game_object(self):
        return self.data
    
class ComponentData(EventData):
    def __init__(self, pygameobject: PygameObject, component: Component) -> None:
        super().__init__((pygameobject, component))
    
    def get_pygameobject(self):
        return self.data[0]
    
    def get_component(self):
        return self.data[1]

class NewObjectCreated(Event):
    event_type = NewObjectCreatedEventType
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(NewObjectCreated.event_type, GameObjectData(game_object))

class ObjectDeleted(Event):
    event_type = ObjectDeletedEventType
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(ObjectDeleted.event_type, GameObjectData(game_object))

class ObjectStarted(Event):
    event_type = ObjectStartedEventType
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(ObjectStarted.event_type, GameObjectData(game_object))

class ComponentAddedToObject(Event):
    event_type = ComponentAddedToObjectEventType
    def __init__(self, pygameobject: PygameObject, component: Component) -> None:
        super().__init__(ComponentAddedToObject.event_type, ComponentData(pygameobject, component))

class ObjectLayerUpdated(Event):
    event_type = ObjectLayerUpdatedEventType
    def __init__(self, game_object: GameObject) -> None:
        super().__init__(ObjectLayerUpdated.event_type, GameObjectData(game_object))


'''Coroutine Events'''
class CoroutineData(EventData):
    def __init__(self, coroutine: Coroutine) -> None:
        super().__init__(coroutine)
    
    def get_coroutine(self):
        return self.data

class CoroutineEnd(Event):
    event_type = CoroutineEndEventType
    def __init__(self, coroutine: Coroutine) -> None:
        super().__init__(CoroutineEnd.event_type, CoroutineData(coroutine))

'''Video Event'''
class VideoResize(Event):
    event_type = VideoResizeEventType
    def __init__(self, new_size: tuple[int, int]) -> None:
        super().__init__(VideoResize.event_type, EventData(new_size))
