import context
from pygamengine import *
from math import sin, cos, pi
from functools import reduce
from pygamengine.coroutines import RunAfterSeconds
import random

class Ship(GameObject):
    def __init__(self):
        super().__init__("ship")
        self.speed = 10
        self.sprite = "src/sprites/ship.png"
        self.bullet = Bullet()

    def start(self):
        self.transform.set_position((Ngine.display[0]/2, Ngine.display[1]/2))
        self.transform.set_rotation(0)
        self.set_collision(True)
        Ngine.create_new_gameobject(self.bullet)
        self.bullet.enabled = False

    def tick(self):
        if Input().get_key("a"):
            self.transform.set_rotation(self.transform.get_rotation()+self.speed)
        if Input().get_key("d"):
            self.transform.set_rotation(self.transform.get_rotation()-self.speed)
        if Input().get_key("SPACE"):
            self.shoot()

        position = self.transform.get_position()
        self.transform.set_position((position[0] % Ngine.display[0], position[1] % Ngine.display[1]))
    
    def shoot(self):
        if self.bullet.enabled:
            return
        self.bullet.transform.set_position(self.transform.get_position())
        self.bullet.set_direction(self.transform.get_rotation())
        self.bullet.enabled = True
    
    def on_collision(self, other: GameObject):
        if isinstance(other, Asteroid):
            Ngine.destroy(other)
            Ngine.destroy(self)
    
    def on_destroy(self):
        RunAfterSeconds(2, respawn)

class Bullet(Rectangle):
    def __init__(self) -> None:
        super().__init__("bullet", 20, 20)
        self.speed = 40
        self.direction = (1, 0)
        self.offset = 180
    
    def set_direction(self, angle_deg):
        angle_rad = (angle_deg + self.offset) * pi / 180
        self.direction = (sin(angle_rad), cos(angle_rad))
        
    def start(self):
        self.set_collision(True)
    
    def tick(self):
        product = lambda x, y: (int(x* self.speed), int(y*self.speed))
        velocity = reduce(product, self.direction)
        self.move(*velocity)
        if not Ngine.is_in_display(self.transform.get_position()):
            # out of the screen
            self.disable()
    
    def disable(self):
        self.enabled = False
        self.set_position((-1,-1))

class Asteroid(Rectangle):
    def __init__(self, x, y, color) -> None:
        super().__init__("asteroid", 100, 100, color)
        self.speed = 2
        self.transform.set_position((x,y))
    
    def start(self):
        i1 = random.randint(0 , 1)
        i2 = random.randint(0 , 1)
        self.direction = ((1, -1)[i1], (1, -1)[i2])
        self.set_collision(True)
    
    def tick(self):
        product = lambda x, y: (int(x* self.speed), int(y*self.speed))
        velocity = reduce(product, self.direction)
        self.move(*velocity)
        position = self.transform.get_position()
        self.transform.set_position((position[0] % Ngine.display[0], position[1] % Ngine.display[1]))

    def on_collision(self, other: GameObject):
        if other.name in ["bullet"]:
            # break in 4 small asteroids
            x, y = int(self.width/4), int(self.height/4)
            centre_x, centre_y = self.transform.get_position()
            other.disable()
            Ngine.create_new_gameobject(SmallAsteroid(centre_x - x, centre_y - y, self.color))
            Ngine.create_new_gameobject(SmallAsteroid(centre_x + x, centre_y - y, self.color))
            Ngine.create_new_gameobject(SmallAsteroid(centre_x + x, centre_y + y, self.color))
            Ngine.create_new_gameobject(SmallAsteroid(centre_x - x, centre_y + y, self.color))
            Ngine.destroy(self)

class SmallAsteroid(Asteroid):
    def __init__(self, x, y, color) -> None:
        super().__init__(x, y, color)
        self.width = self.height = 50
    
    def on_collision(self, other: GameObject):
        if other.name in ["bullet"]:
            other.disable()
            Ngine.destroy(self)
        
    def on_destroy(self):
        global wave_number
        if len(Ngine.get_gameobjects_by_class(Asteroid)) == 1:
            wave_number+=1
            RunAfterSeconds(3, add_asteroids, 3 + wave_number)


def add_asteroids(n):
    global wave_number
    colors = [
        (73, 190, 37, 255),
        (190, 77, 37, 255),
        (37, 150, 190, 255),
        (153, 37, 190, 255)
    ]
    for _ in range(0, n):
        x = random.randint(0, Ngine.display[0])
        y = random.randint(-int(Ngine.display[1]/4), int(Ngine.display[1]/4))
        color = colors[random.randint(0, 3)]
        Ngine.create_new_gameobject(Asteroid(x,y,color))

def respawn():
    Ngine.create_new_gameobject(Ship())

wave_number = 0

if __name__ == "__main__":
    Ngine.create_new_gameobject(Ship())
    add_asteroids(3 + wave_number)
    Ngine.run_engine()