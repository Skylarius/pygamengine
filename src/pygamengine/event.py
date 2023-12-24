from collections import defaultdict
from .design_patterns import Singleton
from typing import TypeAlias

EventType: TypeAlias = str

class EventData:
    def __init__(self, data) -> None:
        self.data = data

class Event:
    def __init__(self, type: EventType, data: EventData) -> None:
        self.type = type
        self.data = data
        event_system = EventSystem()
        event_system.post_event(type, data)
        

class EventSystem(metaclass=Singleton):
    def __init__(self):
        self.__subscribers = defaultdict(list)

    def subscribe(self, event_type: EventType, fn):    
        self.__subscribers[event_type].append(fn)

    def post_event(self, event_type: EventType, data: EventData):
        if event_type in self.__subscribers:
            for fn in self.__subscribers[event_type]:
                fn(data)
    
    def get_subscriber(self, event_type:  EventType):
        for key in self.__subscribers:
            if event_type.name == key.name:
                return self.__subscribers[key]
        return None
