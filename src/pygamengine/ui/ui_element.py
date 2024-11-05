from pygamengine.gameobject import GameObject
from pygamengine.transform import Transform
from typing import Union

class UIElement(GameObject):
    def __init__(self, name: str, position: tuple[float, float], size: Union[tuple[float, float], None] = None) -> None:
        super().__init__(name)
        self.current_image = None
        self.transform.set_position(position)
        self.collider = None
        if size == None:
            self.width = None
            self.height = None
        else:
            self.width = size[0]
            self.height = size[1]
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