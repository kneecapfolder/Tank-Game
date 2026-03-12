import pygame
from classes.config import *
from classes.tank import Tank
from classes.entity import Entity

class Bullet(Entity):
    def __init__(self, tank : Tank, speed, boom):
        super().__init__(tank.x, tank.y)
        self.vel = pygame.Vector2()
        self.vel.from_polar((speed, tank.dir))
        self.boom = boom

    def move(self, dt, tiles):
        self.x += self.vel.x * dt
        self.y += self.vel.y * dt
        print(self.x, self.y)
        print(f"{self.x} > {GRID_SIZE*CELL_SIZE} : {self.x >= GRID_SIZE*CELL_SIZE}")


        # Map border collision
        if self.x < 0 or self.x >= GRID_SIZE*CELL_SIZE or self.y < 0 or self.y >= GRID_SIZE*CELL_SIZE:
            self.boom(self)
            print('boom!')
            return
            
        # Tile collision
        grid_x, grid_y = self.world_to_grid(self.x, self.y)
        if tiles[grid_y][grid_x] == 1:
            self.boom(self)
            print('boom!')


    def draw(self, surface):
        pygame.draw.circle(surface, "yellow", (self.x, self.y), CELL_SIZE * .2)

        