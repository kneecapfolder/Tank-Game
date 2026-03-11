import pygame
from classes import Tank


pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
dt = 0



def draw():
    screen.fill("black")
    pygame.display.flip()



# Gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()

    dt = clock.tick(60)

pygame.quit()


