from typing import Generator
from pygamengine import *
from pygamengine.coroutines import WaitSeconds, Coroutine
import pygame
import random
from enum import Enum
from pygamengine.engine import PygameObject

class SnakePart(Rectangle):
    parts_amount = 0
    def __init__(self, name: str) -> None:
        super().__init__(name, 10, 10, (0,0,0,0))
        self.previous: SnakePart = None
        self.proximity = 0.4
        SnakePart.parts_amount+=1

    def start(self):
        self.set_collision(True)
        self.ignore_collisions_with_class(SnakePart)
    
    def tick(self):
        if self.previous:
            self.transform.set_position(
                Transform.lerp(self.transform.get_position(), self.previous.transform.get_position(), self.proximity)
                )


class SnakeHead(SnakePart):
    def __init__(self) -> None:
        super().__init__("head")
        self.direction = (-1,0)
        self.orientation = 0
        self.speed = 5
        self.last: SnakePart = self

    def tick(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and self.direction[0] != 1:
            self.direction = -1, 0
            self.orientation = 0
        if keys[pygame.K_d] and self.direction[0] != -1:
            self.direction = 1, 0
            self.orientation = 180
        if keys[pygame.K_s] and self.direction[1] != -1:
            self.direction = 0, 1
            self.orientation = 270
        if keys[pygame.K_w] and self.direction[1] != 1:
            self.direction = 0, -1
            self.orientation = 90
        
        self.move(self.direction[0]*self.speed, self.direction[1]*self.speed)
        # self.transform.set_rotation(self.orientation)
    
    def add_new_part(self):
        new_part = SnakePart(f"part_{SnakePart.parts_amount}")
        new_part.transform.set_position(self.last.transform.get_position())
        new_part.move(self.last.width, 0)
        new_part.previous = self.last
        Ngine.create_new_gameobject(new_part)
        self.last = new_part
    
    def on_collision(self, other: GameObject):
        if isinstance(other, Food):
            Ngine.destroy(other)
            self.add_new_part()

class Food(Rectangle):
    food_amount = 0
    def __init__(self) -> None:
        super().__init__("food", 10, 10)
        Food.food_amount+=1
    
    def start(self):
        x = random.randint(30, Ngine.display[0] - 30)
        y = random.randint(30, Ngine.display[1] - 30)
        self.transform.set_position((x,y))
    
    def on_destroy(self):
        Food.food_amount-=1

class DrawSnake(Coroutine):
    def __init__(self) -> None:
        super().__init__()
        self.__x_offset = 10
        self.__y_offset = 5
    
    def get_top_left(pygameobj: PygameObject):
        return pygameobj.get_screen_position()
    
    def get_top_right(pygameobj: PygameObject):
        return Transform.get_vectors_sum(pygameobj.get_screen_position(), (pygameobj.image.get_width(), 0))
    
    def get_bottom_left(pygameobj: PygameObject):
        return Transform.get_vectors_sum(pygameobj.get_screen_position(), (0, pygameobj.image.get_height()))
    
    def get_bottom_right(pygameobj: PygameObject):
        return Transform.get_vectors_sum(pygameobj.get_screen_position(), (pygameobj.image.get_width(), pygameobj.image.get_height()))
    
    class PART_POSITION(Enum):
        HEAD = 0
        UP = 1
        RIGHT = 2
        DOWN = 3
        LEFT = 4
    
    def get_previous_part_relative_position(self, part: SnakePart):
        if part.previous == None:
            head : SnakeHead = part
            if head.direction == (-1, 0): # LEFT
                return self.PART_POSITION.LEFT
            elif head.direction == (1,0): # RIGHT
                return self.PART_POSITION.RIGHT
            elif head.direction == (0,1): # DOWN
                return self.PART_POSITION.DOWN
            elif head.direction == (0,-1): # UP
                return self.PART_POSITION.UP
        pos = part.transform.get_position()
        prev_pos = part.previous.transform.get_position()
        x_dist = prev_pos[0] - pos[0]
        x_dist_abs = x_dist if x_dist > 0 else -x_dist
        y_dist = prev_pos[1] - pos[1]
        y_dist_abs = y_dist if y_dist > 0 else -y_dist
        if x_dist_abs > y_dist_abs: # OR RIGHT OR LEFT
            return self.PART_POSITION.RIGHT if x_dist > 0 else self.PART_POSITION.LEFT
        else: #OR UP OR DOWN
            return self.PART_POSITION.DOWN if y_dist > 0 else self.PART_POSITION.UP      

    def execute(self):
        while True:
            min_x = 10000
            min_y = 10000
            max_x = -10000
            max_y = -10000
            objects = Ngine.get_gameobjects_by_class(SnakePart)
            for pygameobject in objects:
                if pygameobject.get_screen_position()[0] < min_x:
                    min_x = pygameobject.get_screen_position()[0]
                if pygameobject.get_screen_position()[1] < min_y:
                    min_y = pygameobject.get_screen_position()[1]
                if pygameobject.get_screen_position()[0] > max_x:
                    max_x = pygameobject.get_screen_position()[0]
                if pygameobject.get_screen_position()[1] > max_y:
                    max_y = pygameobject.get_screen_position()[1]
            top_left = (min_x , min_y)
            points = []
            upper_points = []
            lower_points = []
            # follow CLOCKWISE drawing
            head = objects[0]
            # Add top points
            for i in range(0, len(objects)):
                pyobj = objects[i]
                part: SnakePart = objects[i].gameobject
                previous_relative_pos = self.get_previous_part_relative_position(part)
                if previous_relative_pos is self.PART_POSITION.LEFT:
                    upper_points.append(DrawSnake.get_top_left(pyobj))
                    lower_points.append(DrawSnake.get_bottom_left(pyobj))
                elif previous_relative_pos is self.PART_POSITION.RIGHT:
                    upper_points.append(DrawSnake.get_bottom_right(pyobj))
                    lower_points.append(DrawSnake.get_top_right(pyobj))
                elif previous_relative_pos is self.PART_POSITION.DOWN:
                    upper_points.append(DrawSnake.get_bottom_left(pyobj))
                    lower_points.append(DrawSnake.get_bottom_right(pyobj))
                elif previous_relative_pos is self.PART_POSITION.UP:
                    upper_points.append(DrawSnake.get_top_right(pyobj))
                    lower_points.append(DrawSnake.get_top_left(pyobj))
            # Add last two points to the last one (clockwise)
            tail : SnakePart = objects[len(objects)-1].gameobject
            tail_previous = self.get_previous_part_relative_position(tail)
            if tail_previous is self.PART_POSITION.LEFT:
                upper_points.append(DrawSnake.get_top_right(pyobj))
                lower_points.append(DrawSnake.get_bottom_right(pyobj))
            elif tail_previous is self.PART_POSITION.RIGHT:
                upper_points.append(DrawSnake.get_bottom_left(pyobj))
                lower_points.append(DrawSnake.get_top_left(pyobj))
            elif tail_previous is self.PART_POSITION.DOWN:
                upper_points.append(DrawSnake.get_top_left(pyobj))
                lower_points.append(DrawSnake.get_top_right(pyobj))
            elif tail_previous is self.PART_POSITION.UP:
                upper_points.append(DrawSnake.get_bottom_right(pyobj))
                lower_points.append(DrawSnake.get_bottom_left(pyobj))

            # Draw polygon
            head: PygameObject = objects[0]
            rect_top_left = Transform.get_vectors_sum(top_left, (-head.image.get_width(), -head.image.get_height()))
            
            # Combine upperpoints and lowerpoints (clockwise way)
            for i in range(0, len(upper_points)):
                points.append(Transform.get_vectors_distance(rect_top_left, upper_points[i]))
            for i in range(0, len(lower_points)):
                points.append(Transform.get_vectors_distance(rect_top_left, lower_points[len(lower_points) - i - 1]))                        
            
            image = pygame.Surface((max_x - min_x + head.image.get_width()*3, max_y - min_y + head.image.get_height()*3))
            # image.fill((0,255,0,255))
            image.fill(0)
            pygame.draw.polygon(image, pygame.Color(255, 0, 0, 255), points)
            Ngine.get_screen().blit(image, top_left)
            rect = pygame.rect.Rect(Transform.get_vectors_sum(top_left, (-10, -10)) + Transform.get_vectors_sum(image.get_size(), (10,10)))
            pygame.display.update(rect)
            yield 0

class GenerateFood(Coroutine):
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self) -> Generator:
        while True:
            wait = WaitSeconds(2)
            for i in wait():
                yield i
            Ngine.create_new_gameobject(Food())

if __name__ == "__main__":
    head = SnakeHead()
    head.transform.set_position((int(Ngine.display[0]/2), int(Ngine.display[1]/2)))
    Ngine.create_new_gameobject(head)
    previous_part = head
    for i in range (0,4):
        head.add_new_part()
    GenerateFood()
    DrawSnake()
    Ngine.run_engine()