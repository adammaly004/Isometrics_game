import pygame
from sys import exit

pygame.init()

WIDTH = 1280
HEIGHT = 640

BLACK = (0, 0, 0)

# Start pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("TEST")


class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.rect.y = self.rect.x * self.rect.x + 10


while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick(60)
