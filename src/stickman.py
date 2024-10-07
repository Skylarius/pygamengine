from pygamengine import *
import pygame

from pygamengine.components.animation import Animation, Frame
from pygamengine.components import Animator

class Stickman(GameObject):
    def __init__(self):
        super().__init__("ship")
        self.speed = 10
        self.boundaries = [(100, Ngine.display[0] - 100), (100, Ngine.display[1] - 100)]
        self.sprite = "src/sprites/animations/stickman/stick_0.png"
        
        animator = Animator()
        # Setup walk_right
        animation_right = Animation("stick_walk_right", Frame.make_frames_from_sprites_in_folder("src/sprites/animations/stickman",10))
        animation_right.build_sequence_indices([0,1,2,1])
        animator.add_animation_at_state("walk_right", animation_right)

        # Setup walk left by copying and flipping right
        animation_left = Animation("stick_walk_left", Frame.make_frames_from_images(animation_right.get_all_frames_as_images(), 10))
        animation_left.flip_all_frames(True, False)
        animation_left.build_sequence_indices([0,1,2,1])
        animator.add_animation_at_state("walk_left", animation_left)

        animator.state = "walk_right"

        self.add_component(animator)
        self.my_animator: Animator = self.get_component(Animator)


    def start(self):
        self.transform.set_position((Ngine.display[0]/2, 600))

    def tick(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and self.transform.get_position()[0] > self.boundaries[0][0]: 
            self.move(-self.speed, 0)
            self.my_animator.state = "walk_left"
        if keys[pygame.K_d]and self.transform.get_position()[0] < self.boundaries[0][1]:
            self.move(self.speed, 0)
            self.my_animator.state = "walk_right"
        if keys[pygame.K_w]and self.transform.get_position()[1] > self.boundaries[1][0]:
            self.move(0, -self.speed)
        if keys[pygame.K_s]and self.transform.get_position()[1] < self.boundaries[1][1]:
            self.move(0, self.speed)

if __name__ == "__main__":
    Ngine.set_background_color((255,255,255,255))
    Ngine.create_new_gameobject(Stickman())
    Ngine.run_engine()