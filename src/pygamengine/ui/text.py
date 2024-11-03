from .ui_element import UIElement
from pygamengine.exceptions import ConstructionOrderError
import pygame

class Text(UIElement):
    def __init__(self, name: str, position: tuple[float, float] = (0,0), color=(240,240,240,255)) -> None:
        super().__init__(name, position, (1,1))
        self.font = None
        self.text = name
        self.color = color
        self.line_spacing = 10
    
    def construct(self):
        self.font = pygame.font.SysFont(None, 24)
        self.current_image = self.font.render(self.text, True, self.color)
    
    def update_text(self):
        if self.font is None:
            raise ConstructionOrderError("Text.font is None: maybe you're tryig to call update_text before the Ngine created the object...")
        self.current_image = self.font.render(self.text, False, self.color)
        self.mark_as_to_update = True
        self.transform.force_update()
    
    def set_update(self, text: str):
        self.text = text
        self.update_text()