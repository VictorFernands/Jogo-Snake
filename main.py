
import pygame
import sys
import os
import configparser
import random

# Carregar configuração
CONFIG_FILE = os.path.join('conf', 'conf.ini')
config = configparser.ConfigParser()
controls = {}
SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN = 800, 600, False

try:
    config.read(CONFIG_FILE)
    SCREEN_WIDTH = config.getint('Display', 'width', fallback=800)
    SCREEN_HEIGHT = config.getint('Display', 'height', fallback=600)
    FULLSCREEN = config.getboolean('Display', 'fullscreen', fallback=False)
    controls['UP'] = pygame.key.key_code(config.get('Controls', 'up', fallback='w'))
    controls['DOWN'] = pygame.key.key_code(config.get('Controls', 'down', fallback='s'))
    controls['LEFT'] = pygame.key.key_code(config.get('Controls', 'left', fallback='a'))
    controls['RIGHT'] = pygame.key.key_code(config.get('Controls', 'right', fallback='d'))
    controls['PAUSE'] = pygame.key.key_code(config.get('Controls', 'pause', fallback='enter'))
except:
    controls = {'UP': pygame.K_w, 'DOWN': pygame.K_s, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d, 'PAUSE': pygame.K_RETURN}

pygame.init()
flags = pygame.FULLSCREEN | pygame.SCALED if FULLSCREEN else 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
clock = pygame.time.Clock()

snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
direction = 'RIGHT'
block_size = 20
food = (random.randint(0, SCREEN_WIDTH // block_size - 1) * block_size,
        random.randint(0, SCREEN_HEIGHT // block_size - 1) * block_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == controls['PAUSE']:
                running = False
            elif event.key == controls['UP'] and direction != 'DOWN':
                direction = 'UP'
            elif event.key == controls['DOWN'] and direction != 'UP':
                direction = 'DOWN'
            elif event.key == controls['LEFT'] and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == controls['RIGHT'] and direction != 'LEFT':
                direction = 'RIGHT'

    head_x, head_y = snake[0]
    if direction == 'UP': head_y -= block_size
    if direction == 'DOWN': head_y += block_size
    if direction == 'LEFT': head_x -= block_size
    if direction == 'RIGHT': head_x += block_size

    new_head = (head_x, head_y)
    if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT or new_head in snake:
        running = False
    else:
        snake.insert(0, new_head)
        if new_head == food:
            food = (random.randint(0, SCREEN_WIDTH // block_size - 1) * block_size,
                    random.randint(0, SCREEN_HEIGHT // block_size - 1) * block_size)
        else:
            snake.pop()

    screen.fill((10, 10, 10))
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, block_size, block_size))
    pygame.draw.rect(screen, (255, 0, 0), (*food, block_size, block_size))
    pygame.display.flip()
    clock.tick(15)

pygame.quit()
sys.exit()
