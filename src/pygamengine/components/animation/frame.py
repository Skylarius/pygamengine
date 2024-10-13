from pygame import Surface, transform
from pygame import image as pygameimage
from typing import Union
import os

class Frame:
    '''
    Class describing an animation frame.

    Properties:
            image (pygame.Surface): the image of the frame 
            duration (int): the duration, in frames amount, of the single frame before update
    '''
    def __init__(self, image: Union[Surface, str], duration: int = 0) -> None:
        self.image: Surface = image if isinstance(image, Surface) else pygameimage.load(image)
        self.image.convert()
        self.duration: int = duration
    
    @staticmethod
    def make_frames_from_sprites_in_folder(folder_path: str, all_frames_duration: int = 0, prefix="") -> list['Frame']:
        frames: list[Frame] = []
        paths = os.listdir(folder_path)
        paths.sort()
        for filename in paths:
            if prefix == "" or prefix in filename:
                filepath = os.path.join(folder_path, filename)
                frames.append(Frame(pygameimage.load(filepath), all_frames_duration))
        return frames
    
    def make_frames_from_images(images: list[Surface], all_frames_duration: int = 0) -> list['Frame']:
        frames: list[Frame] = []
        for image in images:
            frames.append(Frame(image, all_frames_duration))
        return frames
    
    def flip_image(self, x: bool, y: bool):
        self.image = transform.flip(self.image, x, y)