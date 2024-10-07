from pygamengine.components.animation import Animation
from pygamengine.components import Component
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from pygamengine.engine import PygameObject


class Animator(Component):
    def __init__(self, name="animator"):
        super().__init__(name)
        self._states_animations_dict: Dict[str, Animation] = {}
        self.state = ""

    def get_current_animation(self) -> Animation:
        return self._states_animations_dict[self.state]
    
    '''Play current animation and return it'''
    def play_current_animation(self) -> Animation:
        return self.get_current_animation().play()
    
    def add_animation_at_state(self, state: str, animation: Animation):
        self._states_animations_dict[state] = animation

    def remove_state(self, state: str):
        del self._states_animations_dict[state]

    def get_all_states(self) -> list[str]:
        return [k for k in self._states_animations_dict]

    def update(self, pygameobject: 'PygameObject'):
        image = pygameobject.get_original_image()
        new_image = self.play_current_animation().get_image()
        if image != new_image:
            pygameobject.update_original_image(new_image)
            pygameobject.gameobject.transform.force_update()