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
        self.dragging = False  # Flag to track the dragging state
    
    def construct(self):
        self.current_image = self.indicator_image
    
    def state_machine(self):
        x, y = self.transform.get_position()
        mousex, mousey = self.__input.get_mouse_position()
        size_x, size_y = self.width, self.height

        in_button_area: bool = x - size_x/2 < mousex < x + size_x/2 and y - size_y/2 < mousey < y + size_y/2
        
        # If mouse is over the indicator and the button is pressed, start dragging
        if in_button_area and self.__input.get_mouse_pressed()[0]:
            self.state = PRESSED
            self.dragging = True  # Start dragging
            return
        # When the mouse is released, finalize the slider value
        if self.state == PRESSED and not self.__input.get_mouse_pressed()[0]:
            self.state = NONE
            if self.dragging:
                self.finalize_slider_value()  # Calculate and finalize the slider value
            self.dragging = False  # Stop dragging

    def move_indicator_to_mouse(self, mousex: int, mousey: int):
        pos = self.transform.get_position()
        slider_pos_x, slider_pos_y = self.slider.transform.get_position()
        
        # Move the indicator within the slider bounds (horizontal or vertical)
        if self.slider.slider_type == SliderType.Horizontal:
            slider_min_x = slider_pos_x - self.slider.width / 2
            slider_max_x = slider_pos_x + self.slider.width / 2
            pos_x = max(slider_min_x, min(mousex, slider_max_x))  # Limit position within bounds
            new_pos = (pos_x, pos[1])
        elif self.slider.slider_type == SliderType.Vertical:
            slider_min_y = slider_pos_y + self.slider.height / 2
            slider_max_y = slider_pos_y - self.slider.height / 2
            pos_y = min(slider_min_y, max(mousey, slider_max_y))  # Limit position within bounds
            new_pos = (pos[0], pos_y)

        self.transform.set_position(new_pos)
    
    def finalize_slider_value(self):
        pos = self.transform.get_position()
        slider_pos_x, slider_pos_y = self.slider.transform.get_position()
        
        # Calculate the final slider value based on the indicator position
        if self.slider.slider_type == SliderType.Horizontal:
            slider_min_x = slider_pos_x - self.slider.width / 2
            slider_max_x = slider_pos_x + self.slider.width / 2
            # Calculate proportional value based on position
            t = (pos[0] - slider_min_x) / (slider_max_x - slider_min_x)
            value = self.slider.min_value + t * (self.slider.max_value - self.slider.min_value)
            
            # Round value to the nearest step (up or down)
            if self.slider.step > 0:
                value = round(value / self.slider.step) * self.slider.step

            # Set the final slider value and update the indicator position accordingly
            self.slider.set_value(value)
            self.slider.update_indicator_position_with_value(value)

        elif self.slider.slider_type == SliderType.Vertical:
            slider_min_y = slider_pos_y + self.slider.height / 2
            slider_max_y = slider_pos_y - self.slider.height / 2
            # Calculate proportional value based on position
            t = (slider_min_y - pos[1]) / (slider_min_y - slider_max_y)
            value = self.slider.min_value + t * (self.slider.max_value - self.slider.min_value)

            # Round value to the nearest step (up or down)
            if self.slider.step > 0:
                value = round(value / self.slider.step) * self.slider.step

            # Set the final slider value and update the indicator position accordingly
            self.slider.set_value(value)
            self.slider.update_indicator_position_with_value(value)
    
    def tick(self):
        self.state_machine()
        if self.dragging:
            mousex, mousey = self.__input.get_mouse_position()
            self.move_indicator_to_mouse(mousex, mousey)  # Move the indicator continuously during dragging

class Slider(UIElement):

    sprite_cache = SpriteCache()
    
    def __init__(self, 
            name: str, position: tuple[float, float], 
            anchor: Anchor = Anchor.CENTER,
            bar_image: Union[str, None] = None, bar_size: Union[tuple[float, float], None] = (300,20),
            bar_color: Union[tuple[int,int,int,int], None] = (0,255,255),
            indicator_image: Union[str, None] = None, indicator_size: Union[tuple[float, float], None] = (30,30),
            indicator_color: Union[tuple[int,int,int,int], None] = (0,0,255),
            min_value = 0, max_value = 10, start_value = 5, step = 0,
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
        self.step = step
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
        self.update_indicator_position_with_value(self.__value)

    def set_value(self, value: float):
        self.__value = value
        self.old_value = value
        self.value = value
        self.on_slider_change(value)

    def update_value_with_indicator_position(self, position: tuple[float, float]):
        if self.slider_type == SliderType.Horizontal:
            t = (position[0] - (self.transform.get_position()[0] - self.width/2)) / self.width
        elif self.slider_type == SliderType.Vertical:
            t = (-position[1] + (self.transform.get_position()[1] + self.height/2)) / self.height    
        value = self.min_value + t*(self.max_value - self.min_value)
        # Round the value according to the step
        if self.step > 0:
            value = round(value / self.step) * self.step
            self.update_indicator_position_with_value(value)
        if value != self.old_value:
            self.set_value(value)
    
    def update_indicator_position_with_value(self, value: float):
        pos = self.transform.get_position()
        t = (value - self.min_value)/(self.max_value - self.min_value)
        if self.slider_type == SliderType.Horizontal:
            indicator_pos_x = t*self.width + (pos[0] - self.width/2)
            self.indicator.set_position((indicator_pos_x, pos[1]))
        elif self.slider_type == SliderType.Vertical:
            indicator_pos_y = (pos[1] + self.height/2) - t* self.height
            self.indicator.set_position((pos[0], indicator_pos_y))

    def tick(self):
        self.value = self.__value