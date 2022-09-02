import pygame
from sys import exit
import time
from random import randint, choice

from constants import *


pygame.init()

# Start pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(NAME)

# Assets
grass = pygame.image.load('img/grass.png').convert_alpha()
grass1 = pygame.image.load('img/grass1.png').convert_alpha()
grass2 = pygame.image.load('img/grass2.png').convert_alpha()
stone = pygame.image.load('img/stone.png').convert_alpha()
stone1 = pygame.image.load('img/stone1.png').convert_alpha()
bush = pygame.image.load('img/bush.png').convert_alpha()
flower = pygame.image.load('img/flower.png').convert_alpha()
water = pygame.image.load('img/water.png').convert_alpha()


player_up1 = pygame.image.load('img/player/up1.png').convert_alpha()
player_up2 = pygame.image.load('img/player/up2.png').convert_alpha()
player_up3 = pygame.image.load('img/player/up3.png').convert_alpha()
player_up4 = pygame.image.load('img/player/up4.png').convert_alpha()

player_down1 = pygame.image.load('img/player/down1.png').convert_alpha()
player_down2 = pygame.image.load('img/player/down2.png').convert_alpha()
player_down3 = pygame.image.load('img/player/down3.png').convert_alpha()
player_down4 = pygame.image.load('img/player/down4.png').convert_alpha()


block = pygame.image.load('img/block.png').convert_alpha()
enemy_down1 = pygame.image.load('img/enemy1/down0.png').convert_alpha()
enemy_down2 = pygame.image.load('img/enemy1/down2.png').convert_alpha()

enemy_death1 = pygame.image.load('img/enemy1/down3.png').convert_alpha()
enemy_death2 = pygame.image.load('img/enemy1/down4.png').convert_alpha()
enemy_death3 = pygame.image.load('img/enemy1/down5.png').convert_alpha()
enemy_death4 = pygame.image.load('img/enemy1/down6.png').convert_alpha()
enemy_death5 = pygame.image.load('img/enemy1/down7.png').convert_alpha()

enemy_up1 = pygame.image.load('img/enemy/up1.png').convert_alpha()
enemy_up2 = pygame.image.load('img/enemy/up2.png').convert_alpha()

gun = pygame.image.load('img/guns/shot_side.png').convert_alpha()
heal = pygame.image.load('img/heal.png').convert_alpha()

coin_1 = pygame.image.load('img/coins/coin_1.png').convert_alpha()
coin_2 = pygame.image.load('img/coins/coin_2.png').convert_alpha()
coin_3 = pygame.image.load('img/coins/coin_3.png').convert_alpha()
coin_4 = pygame.image.load('img/coins/coin_4.png').convert_alpha()
coin_5 = pygame.image.load('img/coins/coin_5.png').convert_alpha()
coin_6 = pygame.image.load('img/coins/coin_6.png').convert_alpha()

shop = pygame.image.load('img/house2.png').convert_alpha()

coin_sack_img = pygame.image.load('img/coin_sack.png').convert_alpha()


# Load fonts
font_type = 'Pixeltype.ttf'

# Vytvoreni bloku


class Block:
    def __init__(self, x, y, width, height, image, floor, action=False):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.image = image
        self.image = pygame.transform.scale(
            self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.floor = floor
        self.action = action

    def draw(self):
        # Vÿtvoření posunu všech bloků
        off_set = NUMBER_OF_BLOCKS * \
            (NUMBER_OF_BLOCKS / 2 / NUMBER_OF_BLOCKS) * \
            self.width - self.width / 2

        # Upravování pozice na základě obdržené pozice (x, y)
        self.rect.x = (self.x * 1 + self.y * -1) * self.width / 2 + off_set
        self.rect.y = (self.x * 0.5 + self.y * 0.5) * self.height / 2

        # Zobrazení bloku
        screen.blit(self.image, self.rect)
        self.collide_point = pygame.Rect(
            self.rect.centerx - 5, self.rect.centery - 10, 15, 1)

        # Bod kolize
        if HITBOX:
            pygame.draw.rect(screen, RED,  self.collide_point)

        # pygame.draw.polygon(screen, (255, 255, 255), [
            # (self.rect.x + 32, self.rect.y + 8), (self.rect.x + 64, self.rect.y + 24), (self.rect.x + 32, self.rect.y + 40), (self.rect.x, self.rect.y + 24)])


class IsoMap:
    def __init__(self, map, block):
        self.map = map
        self.blocks = []
        self.block = block

    def create_map(self):
        # Vytvoření herní mapy
        for floor in range(len(self.map)):
            for i in range(len(self.map[floor])):
                for j in range(len(self.map[floor])):
                    if self.map[floor][i][j] == 0:
                        continue
                    elif self.map[floor][i][j] == 1:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, grass, floor))
                    elif self.map[floor][i][j] == 2:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, grass1, floor))
                    elif self.map[floor][i][j] == 3:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, grass2, floor))
                    elif self.map[floor][i][j] == 4:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, stone, floor))
                    elif self.map[floor][i][j] == 5:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, stone1, floor))
                    elif self.map[floor][i][j] == 6:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, water, floor))
                    elif self.map[floor][i][j] == 7:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, bush, floor))
                    elif self.map[floor][i][j] == 8:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, flower, floor))
                    elif self.map[floor][i][j] == 9:
                        self.blocks.append(
                            self.block(i - floor * 0.5, j - floor * 0.5, 180, 140, shop, floor, True))

    def draw(self, player, enemies, shop_menu):
        # Vykreslení vrstvy bloků za hráčem
        for layer1 in self.blocks:
            layer1.draw()
            # Kolize hráče s bloky
            player.collision(layer1)
            # Kolize nepřítele s bloky
            for enemy in enemies:
                enemy.collision(layer1)

        # Vykreslení hráče
        player.draw()

        # Vykreslení a určení druhé vrstvy bluků před hráčem
        for layer2 in self.blocks:
            # Když je blok o patro výše než hráč a jeho pozice y je vyšší, tak se vykreslí blok
            if layer2.floor > player.last_collistion and player.rect.bottom < layer2.rect.bottom - 16 or layer2.floor > player.last_collistion + 1:
                layer2.draw()

                if layer2.action and player.rect.colliderect(layer2.collide_point) and layer2.floor == player.last_collistion + 1:
                    shop_menu.pause = True
                    shop_menu.update()

        # Vykreslení nepřítele a kolize s hráčem
        for enemy in enemies:
            enemy.draw()
            enemy.move(player)
            enemy.animation(enemies)
            player.collision_enemy(enemy)

        # pygame.draw.rect(screen, YELLOW, rect)

        pygame.draw.polygon(screen, (255, 0, 0), [
            (WIDTH/2, - PIXELS + 8), (WIDTH + PIXELS, HEIGHT/2), (WIDTH/2, HEIGHT + PIXELS / 2), (-2 * PIXELS + PIXELS, HEIGHT/2)], 2)


class AbstractMoveableObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = block
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_collistion = 2
        self.collide_point = pygame.Rect(
            self.rect.centerx, self.rect.centery - 20, 2, 40)

    def draw(self):
        # Vykreslení objektu
        screen.blit(self.image, self.rect)
        # Bod kolize pro lepší pohyb v patrech mapy
        self.collide_point = pygame.Rect(
            self.rect.centerx, self.rect.centery + 0, 1, 30)

        # Hitbox
        if HITBOX:
            pygame.draw.rect(screen, RED,  self.collide_point)
            pygame.draw.rect(screen, YELLOW, self.rect, 2)

    def collision(self, block):
        # Pohyb mezi patry
        if self.collide_point.colliderect(block.collide_point):
            if block.floor == 0 and self.last_collistion == 1:
                self.last_collistion = block.floor
                self.rect.y += 16
                self.rect.x -= 1

            if block.floor == 1 and self.last_collistion == 0:
                self.last_collistion = block.floor
                self.rect.y -= 16
                self.rect.x += 1

            if block.floor == 1 and self.last_collistion == 2:
                self.last_collistion = block.floor
                self.rect.y += 16
                self.rect.x -= 1

            if block.floor == 2 and self.last_collistion == 1:
                self.last_collistion = block.floor
                self.rect.y -= 16
                self.rect.x += 1

            if block.floor == 2 and self.last_collistion == 3:
                self.last_collistion = block.floor
                self.rect.y += 16
                self.rect.x -= 1

            if block.floor == 3 and self.last_collistion == 2:
                self.last_collistion = block.floor
                self.rect.y -= 16
                self.rect.x += 1


class Player(AbstractMoveableObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.player_walk_down = [player_down1,
                                 player_down2, player_down3, player_down4]
        self.player_walk_up = [player_up1,
                               player_up2, player_up3, player_up4]
        self.player_index = 0
        self.image = self.player_walk_down[self.player_index]
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.direction = ''
        self.step_index = 0

        # Proměnné použité ke střelbě
        self.armed = False
        self.fire = False
        self.shoot_cooldown = 0
        self.ammo = 0

        self.health = 100

        self.coins = 0

        # Vylepseni
        self.add_ammo = 2
        self.add_heal = 10
        self.coin_spawn = 1

    def move(self, direction):
        # Pohyb hráče
        self.direction = direction
        if direction == 'left':
            self.rect.y -= 1
            self.rect.x -= 2
            self.image = pygame.transform.flip(
                self.player_walk_up[int(self.player_index)], True, False)

        if direction == 'right':
            self.rect.y += 1
            self.rect.x += 2
            self.image = self.player_walk_down[int(self.player_index)]

        if direction == 'up':
            self.rect.y -= 1
            self.rect.x += 2
            self.image = self.player_walk_up[int(self.player_index)]

        if direction == 'down':
            self.rect.y += 1
            self.rect.x -= 2
            self.image = pygame.transform.flip(
                self.player_walk_down[int(self.player_index)], True, False)

        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

    def animation(self):
        self.player_index += 0.2
        if self.player_index >= len(self.player_walk_down):
            self.player_index = 0

    def shoot(self, bullets):
        if self.armed and self.fire:
            bullet = Bullet(self.rect.centerx, self.rect.centery)
            bullets.append(bullet)
            self.fire = False
            self.ammo -= 1

        self.shoot_cooldown -= 1

    def collision_fireball(self, fireball):
        if self.rect.x + self.width > fireball.x and self.rect.x < fireball.x + 20 and self.rect.y + self.height > fireball.y and self.rect.y < fireball.y + 20:
            self.health -= DEMAGE

    def collision_enemy(self, enemy):
        if self.rect.colliderect(enemy.rect):
            self.health -= DEMAGE


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.rect = pygame.Rect(self.x, self.y, 5.0, 5.0)
        self.direction = ''

    def move(self, direction):
        # Určení směru střely
        if self.direction == '':
            self.direction = direction

        if self.direction == 'left':
            self.rect.y -= 1 * self.speed
            self.rect.x -= 2 * self.speed

        if self.direction == 'right':
            self.rect.y += 1 * self.speed
            self.rect.x += 2 * self.speed

        if self.direction == 'up':
            self.rect.y -= 1 * self.speed
            self.rect.x += 2 * self.speed

        if self.direction == 'down':
            self.rect.y += 1 * self.speed
            self.rect.x -= 2 * self.speed

    def draw(self):
        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)
        pygame.draw.rect(screen, RED, self.rect)

    def update(self, direction):
        self.draw()
        self.move(direction)


class Enemy(AbstractMoveableObject):
    def __init__(self, x, y, width, height, player):
        super().__init__(x, y, width, height)
        self.enemy_walk_down = [enemy_down1, enemy_down2]
        self.enemy_walk_up = [enemy_up1, enemy_up2]

        self.enemy_death = [enemy_down1, enemy_death1, enemy_death2,
                            enemy_death3, enemy_death4, enemy_death5]

        self.enemy_index = 0
        self.image = self.enemy_walk_down[self.enemy_index]
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.timer = 0

        self.directionx = (player.rect.centerx - self.rect.centerx)
        self.directiony = (player.rect.centery - self.rect.centery)

        self.speedx = 0
        self.speedy = 0

        self.enemy_alive = True

        self.walk_particle = Particle()

    def move(self, player):
        # Pohyb nepřítele (pokud je naživu)
        if self.enemy_alive:
            # Pohyb pouze v určitých intervalech
            if self.timer <= 16:
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                # Přidání partiklů pod nepřítelem
                self.walk_particle.add_particles(
                    self.rect.centerx, self.rect.centery + 15, 7, (0, 5), (-5, 5))

            elif self.timer > ENEMY_SPEED:
                self.timer = 0
                # Určení směru pohybu podle pozice hráče
                self.directionx = (player.rect.centerx - self.rect.centerx)
                self.directiony = (player.rect.centery - self.rect.centery)

                if self.directionx < 0:
                    self.speedx = -2
                    self.image = pygame.transform.flip(
                        self.image, True, False)
                if self.directiony >= 0:
                    self.speedy = 1
                    self.image = self.enemy_walk_down[int(self.enemy_index)]
                if self.directiony < 0:
                    self.speedy = -1
                    self.image = self.enemy_walk_up[int(self.enemy_index)]
                if self.directionx >= 0:
                    self.speedx = 2
                    self.image = pygame.transform.flip(
                        self.image, True, False)

            self.timer += 1
            self.walk_particle.emit(1, [BLACK, GREY])

        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        if HITBOX:
            pygame.draw.line(screen, GREEN, [player.rect.centerx, player.rect.centery], [
                self.rect.centerx, self.rect.centery], 5)

    def bullet_collision(self, bullet, bullets):
        if self.rect.colliderect(bullet.rect):
            self.enemy_alive = False
            self.enemy_index = 0
            if bullet in bullets:
                bullets.remove(bullet)
            # enemies.remove(self)

    def animation(self, enemies):

        if self.enemy_alive:
            self.enemy_index += 0.5
            if self.enemy_index >= len(self.enemy_walk_down):
                self.enemy_index = 0
        else:
            self.enemy_index += 0.1
            if self.enemy_index >= len(self.enemy_death):
                self.enemy_index = len(self.enemy_death) - 1
                enemies.remove(self)

            if self.enemy_index < 1:
                p = Particle()
                p.add_particles(self.rect.centerx,
                                self.rect.centery, 10, (-5, 5), (-5, 5))
                p.emit(0.01, [RED, ORANGE])

            self.image = self.enemy_death[int(self.enemy_index)]
            if self.directionx > 0:
                self.image = pygame.transform.flip(
                    self.image, True, False)


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
        screen.blit(self.image, self.rect)

        if HITBOX:
            pygame.draw.rect(screen, RED, self.rect, 2)

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
            if player.health <= 100 - player.add_heal:
                player.health += player.add_heal
            else:
                player.health = 100
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
            coins.remove(self)
            player.coins += 1


class ObjectSpawner:
    def __init__(self, delay, list):
        self.timer = 0
        self.delay = delay
        self.list = list

        self.delete_timer = 0

    def spawn(self, object):
        if self.timer > self.delay:
            self.list.append(object)
            self.timer = 0

        self.timer += 1

    def delete(self, delay):
        if self.delete_timer > delay:
            self.list.pop(0)
            self.delete_timer = 0
        self.delete_timer += 1


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
                # pygame.draw.circle(screen, choice([WHITE, ORANGE]),
                # particle[0], int(particle[1]))
                rect = pygame.Rect(
                    particle[0][0], particle[0][1], int(particle[1]), int(particle[1]))
                pygame.draw.rect(screen, choice(colors), rect)

                if HITBOX:
                    pygame.draw.rect(screen, RED, rect, 2)

    def add_particles(self, x, y, radius=20, direction_x=(-5, 0), direction_y=(-5, 0)):
        """pos_x = x
        pos_y = y
        radius = radius"""
        direction_x = randint(direction_x[0], direction_x[1])
        direction_y = randint(direction_y[0], direction_y[1])
        particle_circle = [[x, y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [
            particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy


class FireBall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fireball = Particle()
        self.timer = 0

        self.target_x = 0
        self.target_y = 0

    def move(self, player):

        if self.timer < 1 * FPS:
            self.target_x = player.rect.centerx + randint(-1, 1) * PIXELS
            self.target_y = player.rect.centery + randint(-1, 1) * PIXELS
            self.timer += 1

        # else:
            # pygame.draw.circle(screen, RED, (self.target_x, self.target_y), 10)

        self.directionx = (self.target_x - self.x)
        self.directiony = (self.target_y - self.y)

        self.x += 8 if self.directionx >= 0 else -8
        self.y += 4 if self.directiony >= 0 else -4

        self.fireball.add_particles(self.x, self.y)

        if HITBOX:
            pygame.draw.line(screen, BLUE, [self.x, self.y], [
                self.target_x, self.target_y], 5)

    def update(self, player):
        self.move(player)
        self.fireball.emit()


class HealthBar:
    def __init__(self, x, y, max_health):
        self.x = x
        self.y = y
        self.health = max_health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        if ratio < 0:
            ratio = 0
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN,
                         (self.x, self.y, 150 * ratio, 20))


class AbstractUtilities:
    def draw_button(self, x, y, width, height, color, price, type):
        rect = pygame.Rect(x - width/2, y, width, height)
        pygame.draw.rect(screen, YELLOW, rect)
        pygame.draw.rect(screen, color, rect, 10)

        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and price <= self.player.coins:
            print("buy")
            self.player.coins -= price
            if type == 'heal':
                self.player.add_heal += 5
            elif type == 'gun':
                self.player.add_ammo += 1
            elif type == 'coin':
                self.player.coin_spawn += 1

    def draw_text(self, text, color, size, x, y):
        font = pygame.font.Font(font_type, size)
        text = font.render(str(text), False, color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    def draw_image_button(self, x, y, width, image):
        ratio = image.get_height()/image.get_width()
        image = pygame.transform.scale(
            image, (width, int(width*ratio)))
        rect = image.get_rect(center=(x, y))

        screen.blit(image, rect)


class CoinSack(AbstractUtilities):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, player):
        screen.blit(self.image, self.rect)
        self.draw_text(player.coins, YELLOW, 50,
                       self.x + self.width * 1.5, self.y + 30)


class Timer(AbstractUtilities):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.timer = 0
        self.sec = 0

    def draw(self):
        self.minutes, self.seconds = divmod(self.sec, 60)
        self.draw_text(f"{self.minutes}:{self.seconds}",
                       BLUE, 50, self.x, self.y)

    def update(self):
        if self.timer >= 60:
            self.timer = 0
            self.sec += 1

        self.timer += 1
        self.draw()


class Shop(AbstractUtilities):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.pause = False

    def draw(self):
        screen.fill(GREY)

        self.draw_button(WIDTH * 0.2, 80, 200, 300, BLACK, 1, 'heal')
        self.draw_button(WIDTH * 0.5, 80, 200, 300, BLACK, 2, 'gun')
        self.draw_button(WIDTH * 0.8, 80, 200, 300, BLACK, 3, 'coin')

        self.draw_text("Heal", GREEN, 50, WIDTH * 0.2, 300)
        self.draw_text("Gun", GREEN, 50, WIDTH * 0.5, 300)
        self.draw_text("Coin", GREEN, 50, WIDTH * 0.8, 300)

        self.draw_image_button(WIDTH * 0.2, 200, 100,  heal)
        self.draw_image_button(WIDTH * 0.5, 200, 100,  gun)
        self.draw_image_button(WIDTH * 0.8, 200, 100,  coin_4)

    def update(self):
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.player.step_index = 0
                        self.player.rect.x = 614
                        self.player.rect.y = 182
                        self.pause = False

            self.draw()

            pygame.display.update()
            clock.tick(15)


def main():
    # Create Map
    iso_map = IsoMap(MAP, Block)
    iso_map.create_map()

    player = Player(WIDTH / 2 + 5, HEIGHT / 2 - 10, PIXELS - 12, PIXELS - 8)

    enemies = []

    fireballs = []

    health_bar = HealthBar(50, 50, 100)

    direction = ''

    collectable_items = [Gun(
        115, 215, PIXELS - 37, PIXELS - 45, gun), Heal(300, 300, PIXELS - 40, PIXELS - 35, heal)]

    bullets = []

    object_spawner = ObjectSpawner(5 * FPS, collectable_items)
    enemy_spawner = ObjectSpawner(5 * FPS, enemies)
    fireball_spawner = ObjectSpawner(2 * FPS, fireballs)

    shop_menu = Shop(player)

    coin_sack = CoinSack(WIDTH - 200, 20, 50, 50, coin_sack_img)
    timer = Timer(WIDTH / 2, HEIGHT - 50)

    while True:
        screen.fill(GREY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if player.step_index >= 16:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                direction = 'up'
                player.step_index = 0
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                direction = 'down'
                player.step_index = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                direction = 'left'
                player.step_index = 0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction = 'right'
                player.step_index = 0

            if keys[pygame.K_SPACE] and player.shoot_cooldown < 0 and player.armed:
                player.fire = True
                player.shoot_cooldown = 10

        else:
            player.step_index += 1
            player.move(direction)
            player.animation()

        iso_map.draw(player, enemies, shop_menu)

        player.shoot(bullets)

        for item in collectable_items:
            item.update(player, collectable_items)

        # Spawn Guns
        object_spawner.spawn(choice(
            [Gun(0, 0, PIXELS - 37, PIXELS - 45, gun), Heal(0, 0, PIXELS - 40, PIXELS - 35, heal), Coin(0, 0, PIXELS - 20, PIXELS - 30, [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6])]))

        if len(enemies) < 3:
            enemy_spawner.spawn(Enemy(choice([WIDTH / 2, 0, WIDTH]), choice([0, HEIGHT]),
                                      PIXELS - 12, PIXELS - 8, player))

        for bullet in bullets:
            bullet.update(direction)
            for enemy in enemies:
                enemy.bullet_collision(bullet, bullets)

        fireball_spawner.spawn(FireBall(-100, -100))
        for fireball in fireballs:
            fireball.update(player)
            player.collision_fireball(fireball)
            fireball_spawner.delete(10 * FPS)

        health_bar.draw(player.health)

        coin_sack.draw(player)

        timer.update()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
