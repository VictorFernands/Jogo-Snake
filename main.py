
import pygame
import sys
import os
import configparser
import random

CONFIG_FILE = os.path.join('conf', 'conf.ini')
config = configparser.ConfigParser()
controls = {}
SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN = 800, 600, False

