from __future__ import annotations
from .custom_events import ColliderEnabledChanged
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gameobject import GameObject

class Collider:
    def __init__(self) -> None:
        self.__enable = False
        self.size: tuple[2] = (0,0)
        self.ignored_colliders = list[type]()
    
    def set_collision(self, game_object: GameObject, condition: bool):
        self.__enable = condition
        ColliderEnabledChanged(game_object, condition)
    
    def is_enabled(self):
        return self.__enable