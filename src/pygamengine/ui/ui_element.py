from pygamengine.gameobject import GameObject
from pygamengine.transform import Transform
from typing import Tuple, Union
from enum import Enum

class Anchor(Enum):
    CENTER = 0
    TOP_LEFT = 1

class UIElement(GameObject):
    def __init__(self, name: str, position: tuple[float, float], size: Union[tuple[float, float], None] = None, anchor: Anchor = Anchor.CENTER) -> None:
        super().__init__(name)
        self.current_image = None
        self.collider = None
        self.anchor: Anchor = anchor
        if size == None:
            self.width = None
            self.height = None
        else:
            self.width = size[0]
            self.height = size[1]
        self.transform.set_position(position)
        self.mark_as_to_update = False
        '''Use Ngine.update_draw_order to make it effective after updating'''
        self.draw_order: int = 1000
        self.children: list['UIElement'] = []
    
    def get_children(self) -> list['UIElement']:
        '''
        Gives a list of children (including self) with recursive search
        '''
        ret_children: list['UIElement'] = [self]
        if len(self.children) > 0:
            for child in self.children:
                ret_children.append(*child.get_children())
        return ret_children

    def construct(self):
        pass

    def set_position(self, position: tuple[float, float]):
        if self.anchor == Anchor.CENTER:
            new_pos = position
        elif self.anchor == Anchor.TOP_LEFT:
            new_pos = Transform.get_vectors_sum(position, (self.width/2, self.height/2))
        self.transform.set_position(new_pos)
    
    def get_position(self) -> tuple[float, float]:
        if self.anchor == Anchor.CENTER:
            return self.transform.get_position()
        elif self.anchor == Anchor.TOP_LEFT:
            return Transform.get_vectors_sum(self.transform.get_position(), (-self.width/2, -self.height/2)) 

    def start(self):
        self.set_position(self.transform.get_position())