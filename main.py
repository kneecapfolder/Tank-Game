import pygame
import pygame.math
from config import *
from classes.tank import Tank


pygame.init()
screen = pygame.display.set_mode((CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE))
pygame.display.set_caption('Tank Game')
clock = pygame.time.Clock()
running = True
dt = 0

player = Tank(0, 0)
speed = 50
turning_speed = 50


def draw():
    screen.fill('burlywood3')
    player.draw(screen)
    pygame.display.flip()



# Gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()

    # Movement
    dir_vec = pygame.Vector2()
    if (keys[pygame.K_w]):
        dir_vec.y -= 1
    if (keys[pygame.K_s]):
        dir_vec.y += 1
    if (keys[pygame.K_d]):
        dir_vec.x += 1
    if (keys[pygame.K_a]):
        dir_vec.x -= 1
    
    if dir_vec.magnitude() != 0:
        dir_vec.normalize_ip()
        player.move_by(dir_vec * speed * dt)

    # Turning
    if (keys[pygame.K_RIGHT]):
        player.dir += turning_speed * dt
    if (keys[pygame.K_LEFT]):
        player.dir -= turning_speed * dt

    draw()

    dt = clock.tick(60) / 1000

pygame.quit()


