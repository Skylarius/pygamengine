import pygame
from .design_patterns import Singleton

class Input(metaclass=Singleton):

    W = "w"
    A = "a"
    S = "s"
    D = "d"
    SPACE = "SPACE"

    def __init__(self) -> None:
        self.pressed_keys = pygame.key.get_pressed()
        self.key_value_map: dict[str, int] = {}
        self.keys_up = {}
        self.keys_down = {}
        self.pressed_mouse = pygame.mouse.get_pressed()
        self.mouse_up = {}
        self.mouse_down = {}
        self.update_pressed()

    def update_pressed(self):
        self.update_pressed_keys()
        self.update_pressed_mouse()
    
    def update_pressed_keys(self):
        local_pressed_keys = pygame.key.get_pressed()
        self.keys_up = {i: self.pressed_keys[i] and not local_pressed_keys[i]  for i in range(0, len(self.pressed_keys))}
        self.keys_down = {i: not self.pressed_keys[i] and local_pressed_keys[i]  for i in range(0, len(self.pressed_keys))}
        self.pressed_keys = local_pressed_keys

    def get_key_pressed(self) -> pygame.key.ScancodeWrapper:
        return self.pressed_keys

    def get_key(self, key: str) -> bool:
        key_value: int = self.__get_key_from_key_value_map(key)
        return self.__get_key(key_value)

    def get_key_down(self, key: str) -> bool:
        key_value: int = self.__get_key_from_key_value_map(key)
        return self.keys_down.get(key_value, False)

    def get_key_up(self, key: str) -> bool:
        key_value: int = self.__get_key_from_key_value_map(key)
        return self.keys_up.get(key_value, False)
    
    def update_pressed_mouse(self):
        local_pressed_mouse = pygame.mouse.get_pressed()
        self.muouse_up = {i: self.pressed_mouse[i] and not local_pressed_mouse[i]  for i in range(0, len(self.pressed_mouse))}
        self.mouse_down = {i: not self.pressed_mouse[i] and local_pressed_mouse[i]  for i in range(0, len(self.pressed_mouse))}
        self.pressed_mouse = local_pressed_mouse

    def get_mouse_pressed(self) -> tuple[bool, bool, bool]:
        return pygame.mouse.get_pressed()
    
    def get_mouse_down(self, button_index: int) -> bool:
        return self.mouse_down.get(button_index, False)
    
    def get_mouse_up(self, button_index: int) -> bool:
        return self.mouse_up.get(button_index, False)
    
    def get_mouse_position(self) -> tuple[int, int]:
        return pygame.mouse.get_pos()
    
    def get_mouse_movement(self) -> tuple[int, int]:
        return pygame.mouse.get_rel()

    def __get_key(self, key: int) -> bool:
        return self.pressed_keys[key]

    def __get_key_from_key_value_map(self, key: str):
            if key not in self.key_value_map:
                pygamekey = getattr(pygame, f"K_{key}")
                if pygamekey is not None:
                    return self.key_value_map.setdefault(key, pygamekey)
                else:
                    raise KeyError(f"PygameNgine: Unknown key '{key}'")
            return self.key_value_map[key]

    

