from pygame import image as pygameimage

from pygamengine.components.animation.frame import Frame

class Animation:
    '''
    Class describing an animation frame.

    Properties:
            size (int): the amount of animation frames 
            index (int): index of current animation frame
    '''
    def __init__(self, name, frames: list[Frame] = []):
        self.name = name
        self._frames: list[Frame] = frames
        '''sequence index'''
        self.index = 0
        self._frame_timelaps = 0
        self.build_sequence_indices()
    
    def build_sequence_indices(self, custom_index_sequence: list[int] = []):
        if len(custom_index_sequence) > 0:
            self._sequence: list[int] = custom_index_sequence
        else:
            self._sequence = [i for i in range(0, len(self._frames))]
        self.sequence_size = len(self._sequence)

    '''Returns the frame at the sequence index'''
    def get_frame(self) -> Frame:
        return self._frames[self._sequence[self.index]]
    
    def get_image(self) -> pygameimage:
        return self.get_frame().image
    
    def get_frame_at_index(self, i: int) -> Frame:
        return self._frames[self._sequence[i]]
    
    def get_all_frames(self):
        return [f for f in self._frames]
    
    def get_all_frames_as_images(self):
        return [f.image for f in self._frames]
    
    # TODO: broken if custom sequence
    def insert_frame(self, i: int, frame: Frame):
        self._frames.insert(i, frame)
        self.build_sequence_indices()
    
    # TODO: broken if custom sequence
    def remove_frame_at(self, index: int):
        del self._frames[index]
        self.build_sequence_indices()
    
    def play(self) -> 'Animation':
        self._frame_timelaps+=1
        if (self._frame_timelaps > self.get_frame().duration):
            self.index = (self.index + 1) % self.sequence_size
            self._frame_timelaps = 0
        return self
    
    def flip_frame(self, index: int, x: bool, y: bool):
        self._frames[index].flip_image(x, y)
    
    def flip_all_frames(self, x: bool, y: bool):
        for f in self._frames:
            f.flip_image(x, y)
    
    @classmethod
    def make_single_frame_animation_from_image(cls, name: str, image: pygameimage):
        return Animation(name, [Frame(image)])
