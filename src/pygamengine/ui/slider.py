from pygamengine.caches.sprite_cache import SpriteCache
from pygamengine.ui.ui_element import Anchor
from .ui_element import UIElement
from pygamengine.input import Input
from typing import Union
import pygame
from enum import Enum

NONE = 0
PRESSED = 1

class SliderType(Enum):
    Horizontal = 0
    Vertical = 1

class SliderIndicator(UIElement):
    def __init__(self, name: str, position: tuple[float, float], size: tuple[float, float],#
                anchor: Anchor, image: pygame.Surface, slider: 'Slider') -> None:
        super().__init__(name, position, size, anchor)
        self.__input = Input()
        self.indicator_image = image
        self.state = NONE
        self.slider: 'Slider' = slider
    
    def construct(self):
        self.current_image = self.indicator_image
    
    def state_machine(self):
        x, y = self.transform.get_position()
        mousex, mousey = self.__input.get_mouse_position()
        size_x, size_y = self.width, self.height

        in_button_area: bool = x - size_x/2 < mousex < x + size_x/2 and y - size_y/2 < mousey < y + size_y/2
        
        if in_button_area and self.__input.get_mouse_pressed()[0]:
            self.state = PRESSED
            return
        if self.state == PRESSED and not self.__input.get_mouse_pressed()[0]:
            self.state = NONE
            return
    
    def tick(self):
        self.state_machine()
        if self.state == PRESSED:
            pos = self.transform.get_position()
            mouse_x, mouse_y = self.__input.get_mouse_position()
            slider_pos_x, slider_pos_y = self.slider.transform.get_position()
            if self.slider.slider_type == SliderType.Horizontal:
                slider_min_x = slider_pos_x - self.slider.width/2
                slider_max_x =  slider_pos_x + self.slider.width/2
                pos_x = max(slider_min_x, min(mouse_x, slider_max_x)) # clamp
                new_pos = pos_x, pos[1]
            elif self.slider.slider_type == SliderType.Vertical:
                slider_min_y = slider_pos_y + self.slider.height/2
                slider_max_y =  slider_pos_y - self.slider.height/2 
                pos_y = min(slider_min_y, max(mouse_y, slider_max_y)) # clamp
                new_pos = pos[0], pos_y
            self.transform.set_position(new_pos)
            self.slider.update_value_with_indicator_position(self.transform.get_position())
                

class Slider(UIElement):

    sprite_cache = SpriteCache()
    
    def __init__(self, 
            name: str, position: tuple[float, float], 
            anchor: Anchor = Anchor.CENTER,
            bar_image: Union[str, None] = None, bar_size: Union[tuple[float, float], None] = (300,20),
            bar_color: Union[tuple[int,int,int,int], None] = (0,255,255),
            indicator_image: Union[str, None] = None, indicator_size: Union[tuple[float, float], None] = (30,30),
            indicator_color: Union[tuple[int,int,int,int], None] = (0,0,255),
            min_value = 0, max_value = 10, start_value = 5,
            slider_type: SliderType = SliderType.Horizontal
        ) -> None:
        super().__init__(name, position, None, anchor)
        self.bar_image = bar_image
        self.bar_size = bar_size
        self.bar_color = bar_color
        self.indicator_image = indicator_image
        self.indicator_size = indicator_size
        self.indicator_color = indicator_color
        self.min_value = min_value
        self.max_value = max_value
        self.__value = start_value
        self.value = self.__value
        self.old_value = self.__value
        self.slider_type = slider_type
                
    def construct(self):
        # make bar
        bar_image = None
        if self.bar_image:
            bar_image = Slider.sprite_cache.load_sprite(self.bar_image)
        else:
            bar_image = pygame.Surface(self.bar_size)
            rect = pygame.Rect(1, 1, self.bar_size[0] - 1, self.bar_size[1] - 1)
            pygame.draw.rect(bar_image, pygame.Color(*self.bar_color), rect)
        bar_image.convert()
        self.width, self.height = bar_image.get_size()
        # make indicator
        indicator_image = None
        if self.indicator_image:
            indicator_image = Slider.sprite_cache.load_sprite(self.indicator_image)
        else:
            indicator_image = pygame.Surface(self.indicator_size)
            rect = pygame.Rect(1, 1, self.indicator_size[0] - 1, self.indicator_size[1] - 1)
            pygame.draw.rect(indicator_image, pygame.Color(*self.indicator_color), rect)
        self.current_image = bar_image
        indicator = SliderIndicator(
            f"{self.name}_indicator",
            self.transform.get_position(),
            indicator_image.get_size(), 
            Anchor.CENTER,
            indicator_image,
            self
        )
        self.indicator = indicator
        self.children.append(indicator)

    def start(self):
        self.set_position(self.transform.get_position())
        self.indicator.transform.set_position(self.transform.get_position())
    
    def set_value(self, value: float):
        self.__value = value
        self.old_value = value
        self.value = value
        self.on_slider_change(value)

    def update_value_with_indicator_position(self, position: tuple[float, float]):
        if self.slider_type == SliderType.Horizontal:
            t = (position[0] - (self.transform.get_position()[0] - self.width/2)) / self.width
            value = self.min_value + t*self.max_value    
        elif self.slider_type == SliderType.Vertical:
            t = (-position[1] + (self.transform.get_position()[1] + self.height/2)) / self.height    
            value = t*self.max_value - self.min_value
        if value != self.old_value:
            self.set_value(value)
    
    def update_indicator_position_with_value(self, value: float):
        pos = self.transform.get_position()
        t = (value - self.min_value)/self.max_value
        if self.slider_type == SliderType.Horizontal:
            indicator_pos_x = t*self.width + (pos[0] - self.width/2)
            self.indicator.set_position((indicator_pos_x, pos[1]))
        elif self.slider_type == SliderType.Vertical:
            indicator_pos_y = t*self.height + (pos[1] - self.height/2)
            self.indicator.set_position((pos[0], indicator_pos_y))
    
    def tick(self):
        self.value = self.__value
    
    def on_slider_change(self, new_value: float):
        pass
        
