import pygame

pressed_keys = pygame.key.ScancodeWrapper()
key_value_map: dict[str, int] = {}
keys_down = {}

def update_pressed():
    global pressed_keys
    global keys_down
    local_pressed_keys = pygame.key.get_pressed()
    keys_down = {i: (pressed_keys[i] and not local_pressed_keys[i])  for i in range(0, len(pressed_keys))}
    pressed_keys = local_pressed_keys
    if len(keys_down) > 0:
        print(keys_down)

def get_pressed() -> pygame.key.ScancodeWrapper:
    return pressed_keys

def get_key(key: str) -> bool:
    key_value: int = __get_key_from_key_value_map(key)
    return __get_key(key_value_map.get(key_value, None))

def get_key_down(key: str) -> bool:
    key_value: int = __get_key_from_key_value_map(key)
    return keys_down.get(key_value, False)

def __get_key(key: int) -> bool:
    return pressed_keys[key]

def __get_key_from_key_value_map(key: str):
        if key not in key_value_map:
            pygamekey = getattr(pygame, f"K_{key}")
            if pygamekey is not None:
                return key_value_map.setdefault(key, pygamekey)
            else:
                print("Key unrecognised")
                return -1

    

