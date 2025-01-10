import pygame
import context
from pygamengine import *
import time
from typing import Tuple
import random

class TetrisBlock(Rectangle):
    grid_step = 30
    move_time = 1
    
    def __init__(self, name="block", color=(255,255,255,255), fake=False) -> None:
        super().__init__(name, TetrisBlock.grid_step, TetrisBlock.grid_step, color)
        self.block_position = (0,0)
        self.fake = fake
        Globals.Blocks.append(self)
        self.transform.set_position((Ngine.get_display()[0]/2, TetrisBlock.grid_step))
    
    def start(self):
        self.set_collision(False)
    
    def set_block_position(self, x: int, y: int):
        self.block_position = x,y
        self.transform.set_position((Ngine.get_display()[0]/2 + x*TetrisBlock.grid_step, y*TetrisBlock.grid_step))
    
    def move_left(self):
        self.set_block_position(self.block_position[0] - 1, self.block_position[1])
        return self
    
    def move_right(self):
        self.set_block_position(self.block_position[0] + 1, self.block_position[1])
        return self
        
    def move_down(self):
        self.set_block_position(self.block_position[0], self.block_position[1] + 1)
        return self
        
    def move_up(self):
        self.set_block_position(self.block_position[0], self.block_position[1] - 1)
        return self
    
    def get_tetris_block_at_position(x: int, y: int):
        pos = x, y
        return next((block for block in Globals.Blocks if block.block_position == pos), None)
    
    def get_tetris_block_at_relative_position(self, x: int, y: int):
        world_x, world_y = self.block_position[0] + x, self.block_position[1] + y
        return TetrisBlock.get_tetris_block_at_position(world_x, world_y)

    def can_move(self, x: int, y: int) -> bool:
        return self.get_tetris_block_at_relative_position(x,y) == None
    
        
class Globals:
    Blocks = list[TetrisBlock]()
    Score = 0
    Probabilities = {
        'T': 10,
        'J': 10,
        'Z': 10,
        'O': 10,
        'S': 10,
        'L': 10,
        'I': 10 
        }
    NextChoice = 'Z' # it will be overwritten
    Score_info: PygameObject = None
    Probabilities_info = {}
    Speed_info: PygameObject = None
    Next_info: PygameObject = None

class BlocksSet(GameObject):
    def __init__(self, name="blockSet", color=(255,255,255,255), color_name="color") -> None:
        super().__init__(name)
        self.blocks = list[TetrisBlock]()
        self.color = color
        self.color_name = color_name
        self.time = time.perf_counter()
        self.new_block()
        self.rotations_positions = []
        self.rotation_index = 0
    
    def start(self):
        self.set_collision(False)
    
    def left(self):
        if not self.can_move(-1,0):
            return self
        # else, if it's free
        for block in self.blocks:
            block.move_left()
        return self
    
    def right(self):
        if not self.can_move(1,0):
            return self
        # else, if it's free
        for block in self.blocks:
            block.move_right()
        return self
    
    def down(self):
        if not self.can_move(0,1):
            return self
        for block in self.blocks:
            block.move_down()
        return self

    def rotate(self):
        if len(self.rotations_positions) == 0:
            return self
        # Check if can rotate
        center = self.blocks[0].block_position
        new_relative_positions = self.rotations_positions[self.rotation_index]
        blocks_to_move = self.blocks[1:]
        if len(new_relative_positions) != len(blocks_to_move):
            print("ERROR in rotations positions")
            return self
        for i in range(0,len(blocks_to_move)):
            new_position = center[0] + new_relative_positions[i][0], center[1] + new_relative_positions[i][1]
            block_at_position = TetrisBlock.get_tetris_block_at_position(*new_position)
            if block_at_position is not None and block_at_position not in self.blocks:
                # Can't rotate
                return self
        # Rotate
        for i in range(1, len(self.blocks)):
            p = new_relative_positions[i-1]
            self.blocks[i].set_block_position(center[0] + p[0], center[1] + p[1])
        self.rotation_index = (self.rotation_index+1) % len(self.rotations_positions)
        return self
    
    def can_move(self, x:int, y:int) -> bool:
        for block in self.blocks:
            block_at_position = block.get_tetris_block_at_relative_position(x,y)
            if block_at_position != None and block_at_position not in self.blocks:
                return False
        return True
    
    def new_block(self) -> TetrisBlock:
        block = TetrisBlock(self.color_name + "_block", self.color)
        Ngine.create_new_gameobject(block)
        self.blocks.append(block)
        block.move_down()
        block.move_down()
        block.move_down()
        return block
    
    def tick(self):
        if time.perf_counter() - self.time > TetrisBlock.move_time:
            # Check if it should move
            if not self.can_move(0,1):
                BlocksSet.delete_blocks_in_line()
                # Check if game over
                for block in Globals.Blocks:
                    if block.block_position == (0,0):
                        print(f"GAME OVER! Score: {Globals.Score}")
                        Ngine.game_over()
                        return
                BlocksSet.instance_new_random_blocks_set()
                Ngine.destroy(self)
                return
            else:
                self.time = time.perf_counter()
                for block in self.blocks:
                    block.move_down()
        
        # Movement
        if Input().get_key_down("a"):
            self.left()
        elif Input().get_key_down("d"):
            self.right()
        elif Input().get_key_down("SPACE"):
            self.rotate()
        
        if Input().get_key("s"):
            self.down()
    
    def pick_new_random_blocks_set() -> str:
        # Chose a BlockSet (letter)
        letters = []
        weights = []
        for k, v in Globals.Probabilities.items():
            letters.append(k)
            weights.append(v)
        choice = random.choices(letters, weights=weights)[0]
        
        # Increase weight for the non-chosen letters
        for k in Globals.Probabilities:
            if k != choice:
                Globals.Probabilities[k]*=2
        
        # Reset weight for chosen one
        Globals.Probabilities[choice] = 10
        
        # Save choice
        Globals.NextChoice = choice
    
    def instance_new_random_blocks_set():
        # Instance chosen blockset
        choice = Globals.NextChoice

        # Get the class of the block set basing on the choice
        blocks_set_cls = globals()[choice]

        Ngine.create_new_gameobject(blocks_set_cls())
        
        BlocksSet.pick_new_random_blocks_set()
        set_stats_text()
    
    def delete_blocks_in_line():
        blocks_dict: dict[int, list[TetrisBlock]] = {}
        for block in Globals.Blocks:
            line = block.block_position[1]
            if line not in blocks_dict:
                blocks_dict[line] = list[TetrisBlock]()
            if not block.fake:
                blocks_dict[line].append(block)
        
        blocks_dict = dict(sorted(blocks_dict.items(), reverse=True))
        min_i = min(blocks_dict.keys())
        for i in blocks_dict:
            if len(blocks_dict[i]) == 10:
                for block in blocks_dict[i]:
                    Globals.Blocks.remove(block)
                    Ngine.destroy(block)
                for j in range(min_i, i):
                    for block in blocks_dict[j]:
                        block.move_down()
                Globals.Score+=10
                TetrisBlock.move_time-=0.01
                

class T(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_T", color=(204, 102, 255, 255), color_name="purple")
        self.new_block().move_left()
        self.new_block().move_right()
        self.new_block().move_down()
        # All rotations_positions are relative to self.block[0].block_position.
        # self.block[0] never moves during a rotation
        self.rotations_positions = [
            [(0,-1), (1, 0), (0, 1)],
            [(-1,0), (0, -1), (1, 0)],
            [(0,-1), (-1, 0), (0, 1)],
            [(-1,0), (0, 1), (1, 0)]
        ]

class J(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_J", color=(0, 0, 255, 255), color_name="blue")
        self.new_block().move_left()
        self.new_block().move_up()
        self.new_block().move_up().move_up()
        self.rotations_positions = [
            [(0,-1), (1, 0), (2, 0)],
            [(1,0), (0, 1), (0, 2)],
            [(-1,0), (-2, 0), (0, 1)],
            [(0,-1), (0, -2), (-1, 0)]
        ]

class Z(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_Z", color=(255, 0, 0, 255), color_name="red")
        self.new_block().move_right()
        self.new_block().move_right().move_down()
        self.new_block().move_right().move_down().move_right()
        self.rotations_positions = [
            [(0,-1), (1, -1), (1, -2)],
            [(1 ,0), (1, 1), (2, 1)]
        ]
        
class O(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_O", color=(255, 255, 0, 255), color_name="yellow")
        self.new_block().move_right()
        self.new_block().move_down()
        self.new_block().move_right().move_down()

class S(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_S", color=(0, 255, 0, 255), color_name="green")
        self.new_block().move_left()
        self.new_block().move_left().move_down()
        self.new_block().move_left().move_down().move_left()
        self.rotations_positions = [
            [(0,-1), (-1, -1), (-1, -2)],
            [(-1 ,0), (-1, 1), (-2, 1)]
        ]
    
class L(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_L", color=(204, 102, 0, 255), color_name="orange")
        self.new_block().move_right()
        self.new_block().move_up()
        self.new_block().move_up().move_up()
        self.rotations_positions = [
            [(0, 1), (1, 0), (2, 0)],
            [(-1 ,0), (0, 1), (0, 2)],
            [(0, -1), (-1, 0), (-2, 0)],
            [(1, 0), (0, -1), (0, -2)]
        ]

class I(BlocksSet):
    def __init__(self) -> None:
        super().__init__(name="blockset_I", color=(170, 216, 230, 255), color_name="white")
        self.new_block().move_up()
        self.new_block().move_up().move_up()
        self.new_block().move_up().move_up().move_up()
        self.rotations_positions = [
            [(1, 0), (2, 0), (3, 0)],
            [(0 , -1), (0, -2), (0, -3)],
        ]

class TetrisInfo(Text):
    def __init__(self, name="info") -> None:
        super().__init__(name, color=(0,255,0,255))

def set_info_text():
    text_start_position = (Ngine.get_display()[0]*4/5, Ngine.get_display()[1]/2)
    line_spacing = 20
    i = 1
    Globals.Score_info = Ngine.create_new_gameobject(TetrisInfo("Score"))
    Globals.Score_info.gameobject.transform.set_position(text_start_position)
    for k, _ in Globals.Probabilities.items():
        tetris_info = TetrisInfo(f"Probabilities_{k}")
        Ngine.create_new_gameobject(tetris_info)
        tetris_info.transform.set_position(text_start_position)
        tetris_info.move(0, i*line_spacing)
        Globals.Probabilities_info[k] = tetris_info
        i+=1
    Globals.Speed_info = Ngine.create_new_gameobject(TetrisInfo("Speed"))
    Globals.Speed_info.gameobject.set_position(text_start_position)
    Globals.Speed_info.gameobject.move(0, i*line_spacing)
    i+=1
    Globals.Next_info = Ngine.create_new_gameobject(TetrisInfo("Next"))
    Globals.Next_info.gameobject.set_position(text_start_position)
    i+=1
    Globals.Next_info.gameobject.move(0, i*line_spacing)

def set_board():
    _, display_y = Ngine.get_display()
    max_height = int(display_y*0.9/TetrisBlock.grid_step)
    for y in range(0, max_height):
        block = TetrisBlock(fake=True)
        block.set_block_position(-6,y)
        Ngine.create_new_gameobject(block)
        block = TetrisBlock(fake=True)
        block.set_block_position(5,y)
        Ngine.create_new_gameobject(block)
    for i in range(-6, 6):
        block = TetrisBlock(fake=True)
        block.set_block_position(i,max_height)
        Ngine.create_new_gameobject(block)

def set_stats_text():
    Globals.Score_info.gameobject.set_update(f"Score {Globals.Score}")
    for k, v in Globals.Probabilities.items():
        Globals.Probabilities_info[k].set_update(f"{k} : {v}")
    Globals.Speed_info.gameobject.set_update(f"Speed {1/(float)(TetrisBlock.move_time):.2f}")
    Globals.Next_info.gameobject.set_update(f"Next '{Globals.NextChoice}'")

if __name__ == "__main__":
    # Set frame
    # Ngine.set_display(TetrisBlock.grid_step * 14, TetrisBlock.grid_step * 25)
    Ngine.set_caption("Tetris")
    Ngine.set_display(1000, 1000)
    set_info_text()
    set_board()
    
    BlocksSet.pick_new_random_blocks_set()
    BlocksSet.instance_new_random_blocks_set()
    #Ngine.create_new_gameobject()
    Ngine.run_engine()  
    