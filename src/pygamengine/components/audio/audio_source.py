import pygame
from .audio_listener import AudioListener, SpatialAudioClip
from pygamengine.transform import Transform

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
    def __init__(self, source_path, volume = 1, transform: Transform = None):
        super().__init__(source_path, volume)
        self.source = pygame.mixer.Sound(source_path)
        self.source.set_volume(volume)
        self.transform = transform
    
    def load(self, source_path):
        self.source_path = source_path
        self.source = pygame.mixer.Sound(source_path)
        self.source.set_volume(self.volume)
    
    def unload(self):
        self.source = None
    
    def play(self):
        AudioListener().request_play_sound(SpatialAudioClip(self.source))
    
    def play_spatial_sound(self, left=-1, right=-1):
        '''
        Plays a sound on left and right speaker considering emitter position.
        
        Parameters:
        left (float): Volume to override the left speaker.
        right (float): Volume to override the right speaker.
        '''
        from pygamengine.engine import PyGameNgine
        center_x = PyGameNgine().get_display()[0]*0.5
        if left >= 0 and right >=0:
            AudioListener().request_play_sound(SpatialAudioClip(self.source, left, right))
            return
        if not self.transform:
            self.play()
            return
        position_x = self.transform.get_position()[0]
        volume = self.source.get_volume()
        volume_right = (1 if position_x > center_x else position_x/center_x)*volume
        volume_left = (1 if position_x < center_x else 2 - position_x/center_x)*volume
        AudioListener().request_play_sound(SpatialAudioClip(self.source, volume_left, volume_right))

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
    
    def play(self, time: float = 0, loops: int = 0, fade_ms: int = 0):
        pygame.mixer.music.play(start=time, loops=loops, fade_ms=fade_ms)
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def fadeout(self, time: int):
        pygame.mixer.music.fadeout(time)
    
    def is_playing(self):
        return pygame.mixer.music.get_busy()
