import pygame
from random import randint, choice

from scripts.constants import *


class Particle:
    def __init__(self):
        self.particles = []

    def emit(self, subtraction=1, colors=[WHITE, ORANGE]):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= subtraction
                rect = pygame.Rect(
                    particle[0][0], particle[0][1], int(particle[1]), int(particle[1]))
                pygame.draw.rect(SCREEN, choice(colors), rect)

                if HITBOX:
                    pygame.draw.rect(SCREEN, RED, rect, 2)

    def add_particles(self, x, y, radius=20, direction_x=(-5, 0), direction_y=(-5, 0)):
        direction_x = randint(direction_x[0], direction_x[1])
        direction_y = randint(direction_y[0], direction_y[1])
        particle_circle = [[x, y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [
            particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


class FireBall(Particle):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.timer = 0

        self.target_x = 0
        self.target_y = 0

    def move(self, player):

        if self.timer < 1 * FPS:
            self.target_x = player.rect.centerx + randint(-1, 1) * PIXELS
            self.target_y = player.rect.centery + randint(-1, 1) * PIXELS
            self.timer += 1

        directionx = (self.target_x - self.x)
        directiony = (self.target_y - self.y)

        self.x += 8 if directionx >= 0 else -8
        self.y += 4 if directiony >= 0 else -4

        self.add_particles(self.x, self.y)

        if HITBOX:
            pygame.draw.line(SCREEN, BLUE, [self.x, self.y], [
                self.target_x, self.target_y], 5)

    def update(self, player):
        self.move(player)
        self.emit()
