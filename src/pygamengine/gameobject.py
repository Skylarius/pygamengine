from __future__ import annotations
from typing import Tuple
from .collider import Collider
from .transform import Transform

class GameObject:
    def __init__(self, name: str) -> None:
        self.enabled = True
        self.name = name
        self.sprite: str = ""
        self.transform = Transform()
        self.collider = Collider(self)
        self.mark_as_to_update = False
        '''Use Ngine.update_draw_order to make it effective after updating'''
        self.draw_order: int = -1
    
    def __str__(self) -> str:
        return f"{self.name}, {type(self)}"
        
    def ignore_collisions_with_class(self, *object_class: type):
        self.collider.ignored_colliders.append(object_class)
    
    def set_collision(self, condition: bool):
        self.collider.set_collision(condition)

    def is_collider_enabled(self) -> False:
        return getattr(self, 'collider', False) and self.collider.is_enabled()

    def on_collision(self, other: GameObject):
        pass

    def on_destroy(self):
        pass

    def start(self):
        pass

    def tick(self):
        pass

    '''Transform Section'''
    '''Move the sprite'''
    def move(self,x: int, y: int):
        delta = (x, y)
        self.transform.set_position(tuple(map(sum, zip(self.transform.get_position(), delta))))

    '''Update image according to the sprite path (self.sprite)'''
    def update_sprite(self):
        self.mark_as_to_update = True
        self.transform.force_update()
    
    def set_position(self, position : Tuple[float, float]):
        self.transform.set_position(position)
    
    def set_position_lerp(self, position: Tuple[float, float], t: float):
        self.transform.set_position(
            Transform.lerp(
                self.transform.get_position(), position, t
            )
        )

    def set_enabled(self, condition: bool = True):
        self.enabled = condition
        self.transform.force_update()

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
        self.color = color
        self.line_spacing = 10
    
    def update_text(self):
        self.mark_as_to_update = True
        self.transform.force_update()
    
    def set_update(self, text: str):
        self.text = text
        self.update_text()
    

