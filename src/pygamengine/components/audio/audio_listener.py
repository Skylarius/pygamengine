import pygame

from pygamengine.components.component import Component
from pygamengine.design_patterns import Singleton

class AudioListener(Component, metaclass=Singleton):
    '''
    AudioListener is a class that represents the audio listener of the game.
    '''
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        self.enabled = False
    
    def request_play_sound(self, sound: pygame.mixer.Sound):
        #TODO: to be improved with a queue of sounds to play
        if self.enabled:
            sound.play()
    
    def start(self):
        self.enabled = True



    
