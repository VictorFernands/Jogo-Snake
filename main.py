
import pygame
import sys
import os
import configparser
import random


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
    controls['EXIT'] = pygame.key.key_code(config.get('Controls', 'action_b', fallback='p'))  # Tecla para sair
except:
    controls = {
        'UP': pygame.K_w, 'DOWN': pygame.K_s, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d,
        'PAUSE': pygame.K_RETURN, 'EXIT': pygame.K_p
    }

pygame.init()
flags = pygame.FULLSCREEN | pygame.SCALED if FULLSCREEN else 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption("Snake Game - Versão 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)


block_size = 20
fps = 15

def get_random_position():
    x = random.randint(0, (SCREEN_WIDTH - block_size) // block_size) * block_size
    y = random.randint(0, (SCREEN_HEIGHT - block_size) // block_size) * block_size
    return x, y

def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont("Arial", size)
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def game_loop():
    snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    direction = 'RIGHT'
    food = get_random_position()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == controls['PAUSE']:
                    pygame.quit()
                    sys.exit()
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


        if (head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT or new_head in snake):
            return score  

        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            food = get_random_position()
        else:
            snake.pop()

        # Desenhar
        screen.fill((10, 10, 10))
        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, block_size, block_size))
        pygame.draw.rect(screen, (255, 0, 0), (*food, block_size, block_size))
        draw_text(f"Score: {score}", 28, (255, 255, 255), 10, 10, center=False)
        pygame.display.flip()
        clock.tick(fps)

def game_over_screen(score):
    screen.fill((0, 0, 0))
    draw_text("GAME OVER", 64, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"Score: {score}", 48, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
    draw_text("ENTER para reiniciar | 'P' para sair", 28, (200, 200, 200), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False
                elif event.key == controls['EXIT']: 
                    pygame.quit()
                    sys.exit()

while True:
    score = game_loop()
    game_over_screen(score)
