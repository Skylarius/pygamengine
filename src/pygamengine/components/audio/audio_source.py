import pygame
from .audio_listener import AudioListener

class AudioSource:
    def __init__(self, source_path: str, volume: float = 1):
        self.source_path = source_path
        self.volume = volume
    
    def play(self):
        pass

    def load(self, source_path: str):
        pass

    def unload(self):
        pass

class AudioEffect(AudioSource):
    '''AudioEffect is a class that represents a sound effect that can be played once.
    Without an AudioListener attached elsewhere as a component, the sound will not be played'''
    def __init__(self, source_path, volume = 1):
        super().__init__(source_path, volume)
        self.source = pygame.mixer.Sound(source_path)
        self.source.set_volume(volume)
    
    def load(self, source_path):
        self.source_path = source_path
        self.source = pygame.mixer.Sound(source_path)
        self.source.set_volume(self.volume)
    
    def unload(self):
        self.source = None
    
    def play(self):
        # SHOULD REQUEST TO PLAY THE SOUND TO THE AUDIO LISTENER
        AudioListener().request_play_sound(self.source)

class AudioBackgroundMusic(AudioSource):
    '''AudioBackgroundMusic is a class that represents a background music that can be played,
    paused, stopped, faded out, and checked if it is playing.'''
    def __init__(self, source_path, volume = 1):
        super().__init__(source_path, volume)
        pygame.mixer.music.load(source_path)
        pygame.mixer.music.set_volume(volume)
    
    def load(self, source_path):
        if self.source:
            pygame.mixer.music.unload()
        self.source_path = source_path
        self.source = pygame.mixer.music.load(source_path)
    
    def unload(self):
        if self.source:
            pygame.mixer.music.unload()
    
    def play(self, time: float = 0):
        pygame.mixer.music.play(start=time)
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def fadeout(self, time: int):
        pygame.mixer.music.fadeout(time)
    
    def is_playing(self):
        return pygame.mixer.music.get_busy()
