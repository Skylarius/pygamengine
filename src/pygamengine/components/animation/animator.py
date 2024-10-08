from pygamengine.components.animation import Animation, SINGLE_FRAME
from pygamengine.components import Component
from pygamengine.coroutines import WaitSeconds, Coroutine
from typing import Dict, TYPE_CHECKING, Generator
from pygame import Surface

if TYPE_CHECKING:
    from pygamengine.engine import PygameObject


class Animator(Component):
    def __init__(self, name="animator"):
        super().__init__(name)
        self._states_animations_dict: Dict[str, Animation] = {}
        self._state = ""
        self.animation_coroutine: AnimationCoroutine = None
    
    def set_state(self, state: str):
        old_state = self._state
        self._state = state
        if old_state != self._state:
            self.__reset_cached_animation()
            self.__reset_cached_image()
            self.start_current_animation()
    
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
    
    '''Get next frame on current animation. Returns -1 if the animation is single_frame'''
    def next_frame_current_animation(self):
        framecount = self.get_current_animation().next_frame()
        if framecount > 0:
            self.__cached_image = self.get_current_animation().get_image()
        return framecount

    '''Start Animation, play it until you stop it'''
    def start_current_animation(self, loop = True):
        self.stop_current_animation()
        self.animation_coroutine = AnimationCoroutine(self, loop)
    
    def stop_current_animation(self):
        if not self.animation_coroutine:
            return
        self.animation_coroutine.play = False
    
    def add_animation_at_state(self, state: str, animation: Animation):
        self._states_animations_dict[state] = animation

    def remove_state(self, state: str):
        del self._states_animations_dict[state]

    def get_all_states(self) -> list[str]:
        return [k for k in self._states_animations_dict]

    def update_image(self):
        if self.pygameobject is None:
            return
        self.pygameobject.update_original_image(self.__cached_image)
        self.pygameobject.gameobject.transform.force_update()
    
    def start(self):
        self.start_current_animation()

class AnimationCoroutine(Coroutine):
    def __init__(self, animator: Animator, loop: bool = True) -> None:
        super().__init__()
        self.animator = animator
        self.play = True
        self.loop = loop
    
    def execute(self) -> Generator:
        while True:
            if not self.play:
                yield None
                break
            framecount = self.animator.next_frame_current_animation()
            self.animator.update_image()
            if framecount == SINGLE_FRAME:
                yield None
                self.play = False
                self.loop = False
                break
            i = 0
            while self.play and i <= framecount:
                yield i
                i+=1
            if not self.loop:
                yield None
                break


