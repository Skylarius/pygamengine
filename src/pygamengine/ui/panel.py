from pygamengine.caches.sprite_cache import SpriteCache
from .ui_element import UIElement, Anchor
from typing import Union
import pygame

class Panel(UIElement):

    sprite_cache = SpriteCache()

    def __init__(
            self, name: str, position: tuple[float, float] = (100,100), size: Union[tuple[float, float], None] = (100,100), 
            background: Union[str,tuple[int,int,int,int]] = (255,255,255,255),
            anchor=Anchor.CENTER) -> None:
        super().__init__(name, position, size=size, anchor=anchor)
        self.background = background
    
    def construct(self):
        if isinstance(self.background, str):
            self.current_image = Panel.sprite_cache.load_sprite(self.background)
            self.current_image.convert()
            self.width, self.height = self.current_image.get_size()
        else:
            color = self.background
            self.current_image = pygame.Surface((self.width, self.height))
            rect = pygame.Rect(1, 1, self.width - 1, self.height -1)
            pygame.draw.rect(self.current_image, pygame.Color(*color), rect)
            self.current_image.convert()
    
