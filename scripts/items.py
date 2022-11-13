import pygame
from random import randint

from scripts.constants import *
from scripts.assets import *


class AbstractCollectableItem:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = image
        if type(image) != list:
            self.image = pygame.transform.scale(
                self.image, (self.width, self.height))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.speed = 1
        self.timer = 0

        self.first_spawn = True

    def draw(self):
        SCREEN.blit(self.image, self.rect)

        if HITBOX:
            pygame.draw.rect(SCREEN, RED, self.rect, 2)

    def collision(self, player, collectable_items):
        if self.rect.colliderect(player.rect):
            collectable_items.remove(self)

    def move(self):
        self.rect.y += self.speed
        if self.timer > 20:
            self.timer = 0
            self.speed = -self.speed
        self.timer += 1

    def spawn(self):
        if self.first_spawn:
            self.first_spawn = False
            choice = randint(1, 4)
            if choice == 1:
                x = randint(0, 19)
                y = randint(0, 19 - x)
                self.rect.x = x * 32 + WIDTH / 2 - 20
                self.rect.y = y * 16 + HEIGHT / 2 - 20

            elif choice == 2:
                x = randint(0, 19)
                y = randint(0, x)
                self.rect.x = x * 32
                self.rect.y = y * 16 + HEIGHT / 2 - 20

            elif choice == 3:
                y = randint(0, 19)
                x = randint(0, y)
                self.rect.x = x * 32 + WIDTH / 2
                self.rect.y = y * 16

            elif choice == 4:
                y = randint(0, 19)
                x = randint(0, y)
                self.rect.x = WIDTH / 2 - x * 32
                self.rect.y = y * 16 - 20

    def update(self, player, collectable_items):
        self.spawn()
        self.draw()
        self.collision(player, collectable_items)
        self.move()


class Gun(AbstractCollectableItem):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.first = True
        self.last_direction = ''
        self.on_player = False

    def transform_image(self, flip, angle):
        image = gun
        image = pygame.transform.flip(
            image, flip, False)
        image = pygame.transform.scale(
            image, (self.width, self.height))
        image = pygame.transform.rotate(image, angle)
        return image

    def animation(self, player):
        if player.direction == 'down' and self.last_direction != 'down':
            self.last_direction = player.direction
            self.image = self.transform_image(True, 20)

        elif player.direction == 'right' and self.last_direction != 'right':
            self.last_direction = player.direction
            self.image = self.transform_image(False, -20)

        elif player.direction == 'up' and self.last_direction != 'up' or player.direction == 'left' and self.last_direction != 'left':
            self.last_direction = player.direction
            self.image = pygame.transform.scale(self.image, (1, 1))

    def collision(self, player, guns):
        if self.rect.colliderect(player.rect):

            self.rect.x = player.rect.centerx - \
                20 if self.last_direction == 'down' else player.rect.centerx
            self.rect.y = player.rect.centery

            self.animation(player)

            if self.first:
                item_music.play()
                self.on_player = True
                player.ammo = player.add_ammo
                player.armed = True
                self.first = False

            if player.ammo <= 0:
                guns.remove(self)
                player.armed = False


class Heal(AbstractCollectableItem):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def collision(self, player, collectable_items):
        if self.rect.colliderect(player.rect):
            item_music.play()
            if player.health <= 120 - player.add_heal:
                player.health += (player.health % 5) + \
                    1 + player.add_heal
            else:
                player.health = 125
            collectable_items.remove(self)


class Coin(AbstractCollectableItem):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.coin_img = image
        self.coin_index = 0
        self.image = self.coin_img[self.coin_index]
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width()/3), self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def animation(self):
        self.coin_index += 0.1
        if self.coin_index >= len(self.coin_img):
            self.coin_index = 0
        self.image = self.coin_img[int(self.coin_index)]
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width()/3), self.height))

    def collision(self, player, coins):
        self.animation()
        if self.rect.colliderect(player.rect):
            item_music.play()
            coins.remove(self)
            player.coins += player.coin_spawn
