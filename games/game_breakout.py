import context
from pygamengine import *
from pygamengine.coroutines import RunAfterSeconds, Coroutine, WaitSeconds
import random

class Player(Rectangle):
    def __init__(self) -> None:
        super().__init__("player", 80, 20)
        self.speed = 1
        self.ignore_collisions_with_class(Brick)
        
    def start(self):
        self.transform.set_position((int(Ngine.display[0]/2), int(Ngine.display[1]*9/10)))
        self.start_y = self.transform.get_position()[1]
        self.boundaries = [int(self.width/2), Ngine.display[0] - int(self.width/2)]
        self.set_collision(True)
    
    def tick(self):
        x, y = Input().get_mouse_position()
        if x > self.boundaries[0] and x < self.boundaries[1]:
            self.set_position((x, self.start_y))

class Ball(Rectangle):
    def __init__(self) -> None:
        super().__init__("ball", 20, 20)
        self.max_height = 10
        self.init_ball()
        
    def start(self):
        self.boundaries = [10, Ngine.display[0] - 10]
        self.set_collision(True)
    
    def init_ball(self):
        self.speed = 5
        self.direction_x = 1
        self.direction_y = -1
        self.transform.set_position((int(Ngine.display[0]/2), int(Ngine.display[1]/2)))
    
    def tick(self):
        next_move_x = self.transform.get_position()[0] + self.speed*self.direction_x
        next_move_y = self.transform.get_position()[1] + self.speed*self.direction_y
        if next_move_y < self.max_height:
            self.direction_y *= -1
        if next_move_x < self.boundaries[0] or next_move_x > self.boundaries[1]:
            self.direction_x *= -1
        self.move(self.speed*self.direction_x, self.speed*self.direction_y)

        if self.transform.get_position()[1] > Ngine.display[1]:
            self.transform.set_position((-100,-100))
            self.speed = 0
            RunAfterSeconds(2, self.init_ball)
        
        self.transform.set_rotation(self.transform.get_rotation()+self.speed/10)
    
    def on_collision(self, other: GameObject):
        if isinstance(other, Player):
            self.direction_y*=-1
            self.direction_x = 2*(self.transform.get_position()[0] - other.transform.get_position()[0])/other.width
            self.speed+=0.1


class Brick(Rectangle):
    def __init__(self, x, y, width, height, color=...) -> None:
        super().__init__("brick", width, height, color)
        self.transform.set_position((x,y))
        self.ignore_collisions_with_class(Brick, Player)
    
    def on_collision(self, other: GameObject):
        global m
        global n
        if (isinstance(other, Ball)):
            Ngine.destroy(self)
            other.direction_y*=-1
            if (len(Ngine.get_gameobjects_by_class(Brick)) == 0):
                # Winning procedure
                m+=1
                n+=0.3
                RunAfterSeconds(2, init_bricks, m, n)
                RunAfterSeconds(3, other.init_ball)
                player = Ngine.get_gameobjects_by_class(Player)[0]
                width = player.gameobject.width
                Ngine.destroy(player.gameobject)
                player = Player()
                player.width=width+10
                Ngine.create_new_gameobject(player)
    
    def start(self):
        self.set_collision(True)

def init_bricks(m,n):
    m=int(m)
    n=int(n)
    colors = [
        (73, 190, 37, 255),
        (190, 77, 37, 255),
        (37, 150, 190, 255),
        (153, 37, 190, 255)
    ]
    brick_width = int(Ngine.display[0]/m)
    brick_height = int(Ngine.display[1]/(3*n))
    for i in range(int(brick_width/2), brick_width*m, brick_width):
        for j in range(int(brick_height/2), brick_height*n, brick_height):
            color = colors[random.randint(0, 3)]
            Ngine.create_new_gameobject(Brick(i,j,brick_width, brick_height, color))

m = 42
n = 12

# Test performance
# 13 x 4 = 52 bricks starts to be a problem
# 54 objects on screen OK
# New improvement: 28/11/2023
# 42 x 12 = 504
class IncreaseBricksAmount(Coroutine):
    def execute(self):
        global m
        global n
        while True:
            wait = WaitSeconds(5)
            for k in wait():
                yield k
            m+=1
            n+=0.3
            for pygameobj in Ngine.get_gameobjects_by_class(Brick):
                Ngine.destroy(pygameobj.gameobject)
            init_bricks(m, n)
        

if __name__ == "__main__":
    Ngine.create_new_gameobject(Player())
    Ngine.create_new_gameobject(Ball())
    init_bricks(m, n)
    # IncreaseBricksAmount()
    Ngine.run_engine()