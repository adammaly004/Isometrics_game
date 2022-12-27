import pygame
from scripts.random_map import CreateMap

WIDTH, HEIGHT = 1280, 640
NAME = "SquareLand Survival"
NUMBER_OF_BLOCKS = 20
PIXELS = 64

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

FPS = 60


ENEMY_SPEED = 25
DEMAGE = 0.2

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (50, 100, 100)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


HITBOX = False

create_map = CreateMap(19, 32, 10)
MAP = create_map.create()
