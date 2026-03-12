import pygame
from game.config import *
from game.entity import Entity

class Tank(Entity):
    def __init__(self, x, y, theme):
        super().__init__(x, y)
        self.dir = 0
        self.hp = 5
        self.shot_cooldown = 2
        self.theme = theme


    def circle_rect_collision(self, circle_center_x, circle_center_y, circle_radius, rect):
        # Find the closest point on the rect to the circle's center
        closest_x = max(rect.left, min(circle_center_x, rect.right))
        closest_y = max(rect.top, min(circle_center_y, rect.bottom))

        # Calculate the distance between the circle's center and this closest point
        distance_x = circle_center_x - closest_x
        distance_y = circle_center_y - closest_y
        distance_pythagoras = (distance_x * distance_x) + (distance_y * distance_y)

        # Check if the distance is less than the circle's radius
        return distance_pythagoras < (circle_radius * circle_radius)


    def move_by(self, vec : pygame.Vector2, tiles):
        self.x += vec.x
        self.y += vec.y

        # Get position on grid
        grid_x, grid_y = self.world_to_grid(self.x, self.y)
        offset_x = self.x % CELL_SIZE
        offset_y = self.y % CELL_SIZE

        # Check for collisions
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = grid_y + i
                x = grid_x + j
                if y < 0 or y >= GRID_SIZE or x < 0 or x >= GRID_SIZE or tiles[y][x] == 1:
                    if self.circle_rect_collision(offset_x, offset_y, CELL_SIZE//2.5, pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)):
                        self.x -= vec.x
                        self.y -= vec.y
                        return
       
    
    def draw(self, surface):
        # center = (self.x + CELL_SIZE/2, self.y + CELL_SIZE/2)
        turet_end = pygame.Vector2()
        turet_end.from_polar((CELL_SIZE * .5, self.dir))
        turet_end.xy += (self.x, self.y)

        # theme = ["dark olive green", "olive drab"]
        # theme = ["royalblue4", "royalblue3"]

        # pygame.draw.rect(surface, "dark olive green", pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(surface, self.theme[0], (self.x, self.y), CELL_SIZE * .5)
        # pygame.draw.rect(surface, "dark green", pygame.Rect(center[0] - 0.25 * CELL_SIZE, center[1] - 0.25 * CELL_SIZE, CELL_SIZE, CELL_SIZE/8))
        # pygame.draw.line(surface, "olive drab 4", (center[0]-.1, center[1]-.1), turet_end.xy, CELL_SIZE//6)
        pygame.draw.circle(surface, self.theme[1], turet_end, CELL_SIZE * .2)
        pygame.draw.circle(surface, self.theme[1], (self.x, self.y), CELL_SIZE * .4)

    