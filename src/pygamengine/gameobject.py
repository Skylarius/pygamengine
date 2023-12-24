from __future__ import annotations
from typing import Tuple
from .collider import Collider

class Transform:
    def __init__(self) -> None:
        self.__position: Tuple[float, float] = (0,0)
        self.__rotation: float = 0
        self.__scale: Tuple[float, float] = (1,1)
        self.__dirty = False
    
    def set_position(self, position: Tuple[float, float]):
        self.__position = position
        self.__dirty = True
    
    def set_rotation(self, rotation: float):
        self.__rotation = rotation
        self.__dirty = True

    def set_scale(self, scale: Tuple[float, float]):
        self.__scale = scale
        self.__dirty = True
    
    def get_position(self) -> Tuple[float, float]:
        return self.__position
    
    def get_rotation(self) -> float:
        return self.__rotation
    
    def get_scale(self) -> Tuple[float, float]:
        return self.__scale
    
    def force_update(self):
        self.__dirty = True

    def is_dirty(self) -> bool:
        return self.__dirty

    def clean(self):
        self.__dirty = False

    def is_dirty_and_then_clean(self):
        if self.__dirty:
            self.__dirty = False
            return True
        return False

    def lerp(A: tuple[float, float], B: tuple[float, float], t: float) -> tuple[float, float]:
        return A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1])
    
    def get_relative_position(self, position: tuple[float, float]) -> tuple[float, float]:
        return (position[0] - self.__position[0], position[1] - self.__position[1])
    
    """
    Get distance between vector A and B
    """
    def get_vectors_distance(A: tuple[float, float], B: tuple[float, float]) -> tuple[float, float]:
        return B[0] - A[0], B[1] - A[1]
    
    def get_vectors_sum(*vectors: tuple[float, float]):
        sum_x = 0
        sum_y = 0
        for v in vectors:
            sum_x+=v[0]
            sum_y+=v[1]
        return sum_x, sum_y


        
class GameObject:
    def __init__(self, name: str) -> None:
        self.name = name
        self.sprite: str = ""
        self.transform = Transform()
        self.collider = Collider()
    
    def __str__(self) -> str:
        return f"{self.name}, {type(self)}"
        
    def ignore_collisions_with_class(self, *object_class: type):
        self.collider.ignored_colliders.append(object_class)
    
    def set_collision(self, condition: bool):
        self.collider.set_collision(self, condition)

    def is_collider_enabled(self) -> False:
        return self.collider.enabled

    def on_collision(self, other: GameObject):
        pass

    def on_destroy(self):
        pass

    def start(self):
        pass

    def tick(self):
        pass

    def move(self,x: int, y: int):
        delta = (x, y)
        self.transform.set_position(tuple(map(sum, zip(self.transform.get_position(), delta))))

class Rectangle(GameObject):
    def __init__(self, name: str, width=10, height=20, color=(240,240,240,255)) -> None:
        super().__init__(name)
        self.width = width
        self.height = height
        self.color=color

class Text(GameObject):
    def __init__(self, name: str, color=(240,240,240,255)) -> None:
        super().__init__(name)
        self.font = None
        self.text = ""
        self.mark_as_to_update = False
        self.color = color
    
    def update_text(self):
        self.mark_as_to_update = True
        self.transform.force_update()
    

