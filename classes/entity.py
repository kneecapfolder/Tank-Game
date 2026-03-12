from classes.config import *

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def world_to_grid(self, x, y):
        return int(x/CELL_SIZE), int(y/CELL_SIZE)


    def draw(self, surface):
        pass