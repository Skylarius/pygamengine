import pygame
import context
from pygamengine import *
from pygamengine.components.animation import Animation, Frame
from pygamengine.components import Animator

class Stickman(GameObject):
    def __init__(self):
        super().__init__("ship")
        self.speed = 4
        self.boundaries = [(100, Ngine.display[0] - 100), (100, Ngine.display[1] - 100)]
        self.sprite = "src/sprites/animations/stickman/stick_0.png"

    def start(self):
        self.transform.set_position((Ngine.display[0]/2, 600))
        animator: Animator = Ngine.add_new_component(Animator(), self)
        # Setup walk_right
        animation_right = Animation("stick_walk_right", Frame.make_frames_from_sprites_in_folder("src/sprites/animations/stickman",10))
        animation_right.build_sequence_indices([0,1,2,1])
        animator.add_animation_at_state("walk_right", animation_right)

        # Setup walk left by copying and flipping right
        animation_left = Animation("stick_walk_left", Frame.make_frames_from_images(animation_right.get_all_frames_as_images(), 10))
        
        animation_left.flip_all_frames(True, False)
        animation_left.build_sequence_indices([0,1,2,1])
        animator.add_animation_at_state("walk_left", animation_left)

        animation_idle = Animation("stick_idle", [animation_right.get_frame_at_index(0)])
        animator.add_animation_at_state("idle", animation_idle)

        self.my_animator: Animator = animator

        self.my_animator.set_state("walk_right")


    def tick(self):
        if Input().get_key(Input.A) and self.transform.get_position()[0] > self.boundaries[0][0]: 
            self.move(-self.speed, 0)
            self.my_animator.set_state("walk_left")
            self.my_animator.speed = 1
        elif Input().get_key(Input.D) and self.transform.get_position()[0] < self.boundaries[0][1]:
            self.move(self.speed * 3, 0)
            self.my_animator.set_state("walk_right")
            self.my_animator.speed = 3
        elif Input().get_key(Input.W) and self.transform.get_position()[1] > self.boundaries[1][0]:
            self.move(0, -self.speed)
            self.my_animator.speed = 1
        elif Input().get_key(Input.S) and self.transform.get_position()[1] < self.boundaries[1][1]:
            self.move(0, self.speed)
            self.my_animator.speed = 1
        else:
            self.my_animator.set_state("idle")

if __name__ == "__main__":
    Ngine.set_background_color((255,255,255,255))
    Ngine.create_new_gameobject(Stickman())
    Ngine.run_engine()