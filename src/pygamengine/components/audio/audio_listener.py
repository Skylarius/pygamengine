from typing import Generator
from pygamengine.transform import Transform
import pygame

from pygamengine.components.component import Component
from pygamengine.coroutines import Coroutine, WaitSeconds
from pygamengine.design_patterns import Singleton

class SpatialAudioClip:
    def __init__(self, sound: pygame.mixer.Sound, left_speaker_volume: float = -1, right_speaker_volume: float = -1):
        self.sound = sound
        if left_speaker_volume == -1 or right_speaker_volume == -1:
            self.left_speaker_volume = self.right_speaker_volume = sound.get_volume()
        else:
            self.left_speaker_volume = left_speaker_volume
            self.right_speaker_volume = right_speaker_volume

class AudioListener(Component, metaclass=Singleton):
    '''
    AudioListener is a class that represents the audio listener of the game.
    '''
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        self.enabled = False
        self.audio_queue = list[SpatialAudioClip]()
        self.max_audio_queue_length = 5
        pygame.mixer.set_num_channels(self.max_audio_queue_length*2)
        self.__is_coroutine_on = False

    def request_play_sound(self, spatial_sound: SpatialAudioClip):
        if self.enabled:
            self.audio_queue.append(spatial_sound)
            if len(self.audio_queue) > self.max_audio_queue_length:
                self.audio_queue.pop(0)
            if not self.__is_coroutine_on:
                PlayAudioCoroutine()
    
    def start(self):
        self.enabled = True

class PlayAudioCoroutine(Coroutine):
    def __init__(self) -> None:
        super().__init__()
        self.listener = AudioListener()
        self.listener.__is_coroutine_on = True
        self.r = 1
    
    def execute(self) -> Generator:
        while len(self.listener.audio_queue):
            spatial_sound = self.listener.audio_queue.pop(0)
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(spatial_sound.sound)
                channel.set_volume(spatial_sound.left_speaker_volume, spatial_sound.right_speaker_volume)
            yield None
        self.listener.__is_coroutine_on = False




    
