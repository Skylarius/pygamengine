from pygamengine.gameobject import GameObject
from pygamengine.transform import Transform

class UIElement(GameObject):
    def __init__(self, name: str, position: tuple[float, float], size: tuple[float, float] = None) -> None:
        self.enabled = True
        self.name = name
        self.sprite: str = None
        self.current_image = None
        self.transform = Transform()
        self.transform.set_position(position)
        self.width = 100
        self.height = 50
        self.mark_as_to_update = False
        '''Use Ngine.update_draw_order to make it effective after updating'''
        self.draw_order: int = -1
        self.children: list['UIElement'] = []

    def construct(self):
        pass