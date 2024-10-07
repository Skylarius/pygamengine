from pygamengine.components.animation import Animation
from pygamengine.components import Component
from typing import Dict, TYPE_CHECKING
from pygame import Surface

if TYPE_CHECKING:
    from pygamengine.engine import PygameObject


class Animator(Component):
    def __init__(self, name="animator"):
        super().__init__(name)
        self._states_animations_dict: Dict[str, Animation] = {}
        self._state = ""
    
    def set_state(self, state: str):
        self._state = state
        self.__reset_cached_animation()
        self.__reset_cached_image()
    
    def __reset_cached_animation(self):
        self.__cached_animation = self._states_animations_dict[self._state]
    
    def __reset_cached_image(self):
        self.__cached_image = self.__cached_animation.get_image()

    def get_current_animation(self) -> Animation:
        return self.__cached_animation
    
    def get_current_image(self) -> Surface:
        return self.__cached_image
    
    '''Play current animation and return it'''
    def play_current_animation(self) -> bool:
        if self.get_current_animation().play():
            self.__cached_image = self.get_current_animation().get_image()
            return True
        return False
    
    def add_animation_at_state(self, state: str, animation: Animation):
        self._states_animations_dict[state] = animation

    def remove_state(self, state: str):
        del self._states_animations_dict[state]

    def get_all_states(self) -> list[str]:
        return [k for k in self._states_animations_dict]

    def update(self, pygameobject: 'PygameObject'):
        if self._state == '':
            return
        if self.play_current_animation():
            pygameobject.update_original_image(self.__cached_image)
            pygameobject.gameobject.transform.force_update()