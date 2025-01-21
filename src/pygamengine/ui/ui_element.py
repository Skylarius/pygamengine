from pygamengine.gameobject import GameObject
from pygamengine.transform import Transform
from typing import Tuple, Union
from enum import Enum
from PIL import Image 

class Anchor(Enum):
    CENTER = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT = 4

class UIElement(GameObject):
    def __init__(self, name: str, position: tuple[float, float], size: Union[tuple[float, float], None] = None, anchor: Anchor = Anchor.CENTER, image_path: str = None) -> None:
        super().__init__(name)
        self.current_image = None
        self.collider = None
        self.anchor: Anchor = anchor
        if size == None:
            self.get_size_from_image(image_path)
        else:
            self.width = size[0]
            self.height = size[1]
        self.set_position(position)
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
    
    def get_size_from_image(self, image_path) -> tuple[float, float]:
        if image_path is None:
            raise Exception("Image path is None and no size was set. Please set a size for the UIElement or provide the image path.")
        img = Image.open(image_path) 
        # get width and height 
        self.width = img.width 
        self.height = img.height 



    def construct(self):
        pass

    def set_position(self, position: tuple[float, float]):
        if self.anchor == Anchor.CENTER:
            new_pos = position
        elif self.anchor == Anchor.TOP_LEFT:
            new_pos = Transform.get_vectors_sum(position, (self.width/2, self.height/2))
        elif self.anchor == Anchor.TOP_RIGHT:
            new_pos = Transform.get_vectors_sum(position, (-self.width/2, self.height/2))
        elif self.anchor == Anchor.BOTTOM_LEFT:
            new_pos = Transform.get_vectors_sum(position, (self.width/2, -self.height/2))
        elif self.anchor == Anchor.BOTTOM_RIGHT:
            new_pos = Transform.get_vectors_sum(position, (-self.width/2, -self.height/2))
        self.transform.set_position(new_pos)

    def get_position_with_anchor(self, anchor: Anchor):
        if anchor == Anchor.CENTER:
            return self.transform.get_position()
        elif anchor == Anchor.TOP_LEFT:
            return Transform.get_vectors_sum(self.transform.get_position(), (-self.width/2, -self.height/2))
        elif anchor == Anchor.TOP_RIGHT:
            return Transform.get_vectors_sum(self.transform.get_position(), (self.width/2, -self.height/2))
        elif anchor == Anchor.BOTTOM_LEFT:
            return Transform.get_vectors_sum(self.transform.get_position(), (-self.width/2, self.height/2))
        elif anchor == Anchor.BOTTOM_RIGHT:
            return Transform.get_vectors_sum(self.transform.get_position(), (self.width/2, self.height/2))
    
    def get_position(self) -> tuple[float, float]:
        return self.get_position_with_anchor(self.anchor)
        
    def move_with_children(self, x: int, y: int):
        super().move(x, y)
        for c in self.children:
            c.move(x,y)
    
    def set_position_with_children(self, position: tuple[float,float]):
        old_pos = self.transform.get_position()
        self.set_position(position)
        new_pos = self.transform.get_position()
        delta = Transform.get_vectors_diff(new_pos, old_pos)
        for c in self.children:
            c.move_with_children(*delta)

    def start(self):
        pass
        #self.set_position_with_children(self.transform.get_position())