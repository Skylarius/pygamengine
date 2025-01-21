from .ui_element import UIElement, Anchor
from .text import Text
import pygame
from pygamengine.input import Input
from pygamengine.caches import SpriteCache
from typing import Union

NONE = 0
SELECTED = 1
PRESSED = 2
RELEASED = 3

class Button(UIElement):

    sprite_cache = SpriteCache()

    def __init__(
            self, name: str, position: tuple[float, float] = (100,100), size: Union[tuple[float, float], None] = None, 
            unselected_image: Union[str,tuple[int,int,int,int]] = (255,255,255,255),
            selected_image: Union[str,tuple[int,int,int,int]] = (255,0,0,255),
            pressed_image: Union[str,tuple[int,int,int,int]] = (0,255,0,255),
            has_text: bool = True, anchor=Anchor.CENTER, initial_text: str = "button_text") -> None:
        image_path = unselected_image if type(unselected_image) is str else None
        super().__init__(name, position, size=size, anchor=anchor, image_path=image_path)
        self.__input = Input()
        self.state = NONE
        self.old_state = NONE
        self.text_offset = (0,0)
        self.unselected_image = unselected_image
        self.selected_image = selected_image
        self.pressed_image = pressed_image
        self.has_text = has_text
        self.initial_text = initial_text
    
    def add_text(self, text: Text):
        self.text = text
        self.children.append(self.text)
    
    def construct(self):
        self.unselected_image = self.make_button_image(self.unselected_image)
        self.selected_image = self.make_button_image(self.selected_image)
        self.pressed_image = self.make_button_image(self.pressed_image)
        self.width, self.height = self.unselected_image.get_size()
        self.current_image = self.unselected_image
        if self.has_text:
            self.add_text(Text(
                f"button_text_{self.name}", self.transform.get_position(), (0,0,0,255), 
                anchor=Anchor.CENTER, text=self.initial_text, max_width=self.width
            ))
        else:
            self.text = None
        
    def make_button_image(self, in_data: Union[str, tuple[int,int,int,int]]) -> pygame.Surface:
        if type(in_data) is str:
            image = Button.sprite_cache.load_sprite(in_data)
            new_width, new_height = image.get_size()
            if self.width is None or self.height is None:
                self.width, self.height = new_width, new_height
            else:
                self.width, self.height = max(self.width, new_width), max(self.height, new_height)
        else:
            color = in_data
            image = pygame.Surface((self.width, self.height))
            rect = pygame.Rect(1, 1, self.width - 1, self.height -1)
            pygame.draw.rect(image, pygame.Color(*color), rect)
            image.convert()
        return image

    def on_click(self):
        print(f"Clicked on button {self.name}")

    def tick(self):
        self.state_machine()
        self.update_image()
        # if self.text:
        #     self.text.transform.set_position(Transform.get_vectors_sum(self.transform.get_position(), self.text_offset))

    def update_image(self):
        if self.state == NONE:
            self.current_image = self.unselected_image
        if self.state == SELECTED:
            self.current_image = self.selected_image
        if self.state == PRESSED:
            self.current_image = self.pressed_image
        if self.old_state != self.state:
            self.mark_as_to_update = True
            self.transform.force_update()
        self.old_state = self.state

    def state_machine(self):
        x, y = self.transform.get_position()
        mousex, mousey = self.__input.get_mouse_position()
        size_x, size_y = self.width, self.height

        in_button_area: bool = x - size_x/2 < mousex < x + size_x/2 and y - size_y/2 < mousey < y + size_y/2
        
        if self.state == SELECTED and self.__input.get_mouse_pressed()[0]:
            self.state = PRESSED
            return
        if not in_button_area and self.state != PRESSED:
            self.state = NONE
        if in_button_area and self.state != PRESSED:
            self.state = SELECTED
            return
        if self.state == PRESSED and not self.__input.get_mouse_pressed()[0]:
            self.on_click()
            self.state = RELEASED
            return
        if self.state == RELEASED:
            self.state = NONE
            return
    
    def start(self):
        super().start()


        