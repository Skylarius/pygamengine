import pygame
import context
from pygamengine import *


class PongObject(Rectangle):
    def __init__(self, name: str, width=10, height=20) -> None:
        super().__init__(name, width, height)
        self.set_collision(True)


class Player(PongObject):
    def __init__(self) -> None:
        super().__init__("player", 50, 150)
        self.speed = 10
        self.transform.set_position((50, int(Ngine.display[1]/2)))
    
    def start(self):
        self.boundaries = (100, Ngine.display[1] - 100)
    
    def tick(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w] and self.transform.get_position()[1] > self.boundaries[0]:
            self.move(0, -self.speed)
        if keys[pygame.K_s] and self.transform.get_position()[1] < self.boundaries[1]: 
            self.move(0, self.speed)


class Ball(PongObject):
    def __init__(self) -> None:
        super().__init__("ball", 50, 50)
        self.init_ball()
    
    def init_ball(self):
        self.speed = 5
        self.direction_x = 1
        self.direction_y = -1
        self.transform.set_position((int(Ngine.display[0]/2), int(Ngine.display[1]/2)))
    
    def tick(self):
        next_move_y = self.transform.get_position()[1] + self.speed*self.direction_y
        if next_move_y < self.boundaries[0] or next_move_y > self.boundaries[1]:
            self.direction_y *= -1
        self.move(self.speed*self.direction_x, self.speed*self.direction_y)

        if self.transform.get_position()[0] < 0:
            Ngine.get_gameobjects_by_name("score")[0].gameobject.on_score_opponent()
            self.init_ball()
        
        if self.transform.get_position()[0] > Ngine.display[0]:
            Ngine.get_gameobjects_by_name("score")[0].gameobject.on_score_player()
            self.init_ball()
            Ngine.get_gameobjects_by_name("opponent")[0].gameobject.speed+=1
        
        self.transform.set_rotation(self.transform.get_rotation() + self.speed/10)
    
    def on_collision(self, other: GameObject):
        if isinstance(other, Player) or isinstance(other, Opponent):
            self.direction_x*=-1
            self.speed += 1


class Opponent(PongObject):
    def __init__(self) -> None:
        super().__init__("opponent", 50, 150)
        self.speed = 8
        self.transform.set_position((Ngine.display[0] - 50, int(Ngine.display[1]/2)))
    
    def tick(self):
        ball = Ngine.get_gameobjects_by_name("ball")[0]
        ball_y = ball.gameobject.transform.get_position()[1]
        if ball_y > self.transform.get_position()[1] + 3:
            self.move(0, self.speed)
        if ball_y < self.transform.get_position()[1] - 3:
            self.move(0, -self.speed)


class Score(Text):
    def __init__(self) -> None:
        super().__init__("score")
        self.player_score = 0
        self.opponent_score = 0
        self.text = f"Player {self.player_score} || {self.opponent_score} Opponent"
        self.transform.set_position((int(Ngine.display[0]/2), int(Ngine.display[1]/2)))

    def on_score_player(self):
        self.player_score+=1
        self.text = f"Player {self.player_score} || {self.opponent_score} Opponent"
        self.update_text()
    
    def on_score_opponent(self):
        self.opponent_score+=1
        self.text = f"Player {self.player_score} || {self.opponent_score} Opponent"
        self.update_text()


if __name__ == "__main__":
    Ngine.create_new_gameobject(Player())
    Ngine.create_new_gameobject(Opponent())
    Ngine.create_new_gameobject(Ball())
    Ngine.create_new_gameobject(Score())
    Ngine.run_engine()
    
        

        