import pygame
import context
from pygamengine import *
import time
from pygamengine.event import EventSystem
from pygamengine.custom_events import ObjectDeleted, GameObjectData

class Ship(GameObject):
    def __init__(self):
        super().__init__("ship")
        self.speed = 10
        self.sprite = "src/sprites/ship.png"
        self.bullet = Bullet()
        self.ignore_collisions_with_class(Bullet)
        self.__setup_on_alien_deletion()

    def start(self):
        self.boundaries = (100, Ngine.get_display()[0] - 100)
        self.transform.set_position((Ngine.get_display()[0]/2, Ngine.get_display()[1]*4/5))
        self.transform.set_rotation(0)
        Ngine.create_new_gameobject(self.bullet)
        self.bullet.enabled = False
        self.set_collision(True)

    def tick(self):
        if Input().get_key("a") and self.transform.get_position()[0] > self.boundaries[0]: 
            self.move(-self.speed, 0)
        if Input().get_key("d") and self.transform.get_position()[0] < self.boundaries[1]:
            self.move(self.speed, 0)
        if Input().get_key_down("SPACE"):
            self.shoot()
    
    def shoot(self):
        if not self.bullet.enabled:
            self.bullet.enabled = True
            self.bullet.transform.set_position(self.transform.get_position())
    
    def on_collision(self, other: GameObject):
        if other.name == "alien":
            Ngine.game_over()
    
    def __setup_on_alien_deletion(self):
        event_system = EventSystem()
    
        def try_game_over(data: GameObjectData):
            if isinstance(data.get_game_object(), Alien):
                if len(Ngine.get_gameobjects_by_name("alien")) == 0:
                    print("GAME OVER ALIENS!")
                    Ngine.game_over()
        
        event_system.subscribe(ObjectDeleted.event_type, try_game_over)

class Bullet(GameObject):
    def __init__(self):
        super().__init__("bullet")
        self.sprite ="src/sprites/bullet.png"
        self.speed = 15
        self.ignore_collisions_with_class(Ship)
    
    def start(self):
        self.set_collision(True)

    def tick(self):
        self.move(0, -self.speed)
        if self.transform.get_position()[1] < 0:
            # out of the screen
            self.disable()
    
    def on_collision(self, other: GameObject):
        if other.name == "alien":
            Ngine.destroy(other)
            self.disable()
    
    def disable(self):
        self.set_position((0,0))
        self.enabled = False

class Alien(GameObject):
    # Statics
    direction = 1
    level = 0 
    speed = 10 
    boundaries = (0, 1000)
    speed_down = 40
    time_to_move = 1
    aliens_start_count = 0

    def __init__(self):
        super().__init__("alien")
        self.sprite ="src/sprites/alien.png"
        self.start_height = self.transform.get_position()[1]
        self.time_counter = time.perf_counter()
        Alien.aliens_start_count += 1
        self.ignore_collisions_with_class(Alien)

    def start(self):
        Alien.boundaries = (30, Ngine.get_display()[0] - 30)
        self.set_collision(True)
    
    def tick(self):
        if self.transform.get_position()[0] < self.boundaries[0] and Alien.direction == -1:
            self.transform.set_position((self.boundaries[0], self.transform.get_position()[1]))
            Alien.level+=self.speed_down
            Alien.direction = 1
        if self.transform.get_position()[0] > self.boundaries[1] and Alien.direction == 1:
            self.transform.set_position((self.boundaries[1], self.transform.get_position()[1]))
            Alien.level+=self.speed_down
            Alien.direction = -1
        self.transform.set_position((self.transform.get_position()[0], self.start_height + Alien.level))
        if time.perf_counter() - self.time_counter > Alien.time_to_move:
            self.time_counter = time.perf_counter()
            self.move(self.direction * self.speed, 0)
    
    def on_destroy(self):
        aliens = Ngine.get_gameobjects_by_class(Alien)
        count = len(aliens)
        if count > 0:
            t = count/Alien.aliens_start_count
            x0 = 0.03
            Alien.time_to_move = x0 + t * (Alien.time_to_move - x0) 


if __name__ == "__main__":
    Ngine.set_display(1280,720, fullscreen=True)
    Ngine.set_background(Background("src/background/space.jpg", "src/background/space1080p.png"))
    ship = Ship()
    Ngine.create_new_gameobject(ship)
    for i in range(30, int(Ngine.get_display()[0]*2/3) , 150):
        for j in range (40, int(Ngine.get_display()[1]/2), 100):
            alien = Alien()
            alien.start_height = j
            alien.transform.set_position((i, j))
            Ngine.create_new_gameobject(alien)
    Alien.boundaries = (30, Ngine.get_display()[0] - 30)
    Ngine.run_engine()