import pygame
from config import *

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = 0


    def move_by(self, vec : pygame.Vector2):
        self.x += vec.x
        self.y += vec.y

    
    def draw(self, surface):
        center = (self.x + CELL_SIZE/2, self.y + CELL_SIZE/2)
        turet_end = pygame.Vector2()
        turet_end.from_polar((CELL_SIZE * .8, self.dir))

        pygame.draw.rect(surface, "dark olive green", pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.line(surface, "dark green", center, center + turet_end.xy, 6)
        pygame.draw.circle(surface, "olive drab", center, CELL_SIZE * .4)

    