
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
except:
    controls = {'UP': pygame.K_w, 'DOWN': pygame.K_s, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d, 'PAUSE': pygame.K_RETURN}

pygame.init()
flags = pygame.FULLSCREEN | pygame.SCALED if FULLSCREEN else 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
clock = pygame.time.Clock()
