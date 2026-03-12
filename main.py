import pygame
import asyncio
import threading
from game.config import *
from game.tank import Tank
from game.bullet import Bullet
from network.client import Client

GAME_RESOLUTION = (CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE)  # Example: a small, fixed resolution
WINDOW_RESOLUTION = (480, 480)

HOST = "127.0.0.1"
PORT = 8989

client = Client(HOST, PORT)

tiles = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 1, 1, 0, 0, 0 ],
    [ 0, 0, 1, 0, 0, 1, 1, 0, 0, 0 ],
    [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 1, 1, 1, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
]

# Init pygame
pygame.init()
screen = pygame.display.set_mode((500, 650))
game_surface = pygame.Surface(GAME_RESOLUTION)
pygame.display.set_caption('Tank Game')
pixel_font = pygame.font.Font("pixel-font.ttf", 30)
clock = pygame.time.Clock()
running = True
dt = 0

# Game vars
player = Tank(2*CELL_SIZE, CELL_SIZE, ["dark olive green", "olive drab"])
enemy = Tank(2*CELL_SIZE, CELL_SIZE, ["royalblue4", "royalblue3"])
bullets = []
booms = []
speed = 50
turning_speed = 100
cooldown = 0.0

client.connect_to_server()

async def move_enemy():
    async for x, y, dir, shoot in client.get_enemy_data():
        enemy.x = x
        enemy.y = y
        enemy.dir = dir
        if shoot:
            bullets.append(Bullet(enemy, 200, boom, True))

threading.Thread(target=asyncio.run, args=(move_enemy(),)).start()

def draw():
    screen.fill('black')
    game_surface.fill('burlywood3')

    for exp in booms:
        pygame.draw.circle(game_surface, "wheat4", exp, CELL_SIZE)

    for bullet in bullets:
        bullet.draw(game_surface)

    for y in range(0, 10):
        for x in range(0, 10):
            if tiles[y][x] == 1:
                pygame.draw.rect(game_surface, "tan4", pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw players
    enemy.draw(game_surface)
    player.draw(game_surface)

    scaled_surface = pygame.transform.scale(game_surface, WINDOW_RESOLUTION)
    screen.blit(scaled_surface, (10, 10))

    # HP Bar
    text_surface = pixel_font.render("hp:", False, (255, 255, 255))
    screen.blit(text_surface, (10, 500))
    pygame.draw.rect(screen, "white", pygame.Rect(60, 505, 120, 30))
    pygame.draw.rect(screen, "black", pygame.Rect(63, 508, 114, 24))
    pygame.draw.rect(screen, "red", pygame.Rect(66, 511, 108, 18))
    pygame.draw.rect(screen, "lime", pygame.Rect(66, 511, 108*player.hp//5, 18))

    # Load
    text_surface = pixel_font.render("ammo:", False, (255, 255, 255))
    screen.blit(text_surface, (10, 540))
    pygame.draw.rect(screen, "white", pygame.Rect(110, 545, 70, 30))
    pygame.draw.rect(screen, "black", pygame.Rect(113, 548, 64, 24))
    # pygame.draw.rect(screen, "red", pygame.Rect(116, 551, 88, 18))
    pygame.draw.rect(screen, "yellow" if cooldown <= 0 else "yellow4", pygame.Rect(116, 551, 58*(player.shot_cooldown-cooldown)//player.shot_cooldown, 18))

    pygame.display.flip()


def boom(bullet):
    booms.append((bullet.x, bullet.y))
    bullets.remove(bullet)


# Gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Inputs
    shoot = False
    keys = pygame.key.get_pressed()

    # Shoot
    if cooldown  > 0:
        cooldown -= dt
    elif keys[pygame.K_SPACE]:
        shoot = True
        bullets.append(Bullet(player, 200, boom, False))
        cooldown = player.shot_cooldown

    # Movement
    dir_vec = pygame.Vector2()
    if keys[pygame.K_w]:
        dir_vec.y -= 1
    if keys[pygame.K_s]:
        dir_vec.y += 1
    if keys[pygame.K_d]:
        dir_vec.x += 1
    if keys[pygame.K_a]:
        dir_vec.x -= 1

    # Turning
    if keys[pygame.K_RIGHT]:
        player.dir += turning_speed * dt
    if keys[pygame.K_LEFT]:
        player.dir -= turning_speed * dt

    # Update
    if dir_vec.magnitude() != 0:
        dir_vec.normalize_ip()
        player.move_by(dir_vec * speed * dt, tiles)
    
    for bullet in bullets:
        bullet.move(dt, tiles, player)

    client.send_data(player, shoot)



    draw()

    dt = clock.tick(60) / 1000

pygame.quit()


