import pygame

from scripts.constants import *
from scripts.assets import *
from scripts.particle import Particle


class AbstractMoveableObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = player_down1
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.last_collistion = 2
        self.collide_point = pygame.Rect(
            self.rect.centerx, self.rect.centery - 20, 2, 40)

    def draw(self):
        # Vykreslení objektu
        SCREEN.blit(self.image, self.rect)
        # Bod kolize pro lepší pohyb v patrech mapy
        self.collide_point = pygame.Rect(
            self.rect.centerx, self.rect.centery + 0, 1, 30)

        # Hitbox
        if HITBOX:
            pygame.draw.rect(SCREEN, RED,  self.collide_point)
            pygame.draw.rect(SCREEN, YELLOW, self.rect, 2)

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

        self.player_death = [player_death1,
                             player_death2, player_death3, player_death4]
        self.player_index = 0
        self.image = self.player_walk_down[self.player_index]
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.direction = ''
        self.step_index = 0
        self.speedx = 0
        self.speedy = 0

        # Proměnné použité ke střelbě
        self.armed = False
        self.fire = False
        self.shoot_cooldown = 0
        self.ammo = 0

        self.health = 125

        self.coins = 0

        # Vylepseni
        self.add_ammo = 2
        self.add_heal = 0
        self.coin_spawn = 1

        # Herni prostor
        self.border_rect = border.get_rect(topleft=(-3, 0))
        self.border_mask = pygame.mask.from_surface(border)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):

        # Pohyb hráče

        if self.health > 0:
            if self.direction == 'left':
                self.speedy = -1
                self.speedx = -2
                self.image = pygame.transform.flip(
                    self.player_walk_up[int(self.player_index)], True, False)

            if self.direction == 'right':
                self.speedy = 1
                self.speedx = 2
                self.image = self.player_walk_down[int(self.player_index)]

            if self.direction == 'up':
                self.speedy = -1
                self.speedx = 2
                self.image = self.player_walk_up[int(self.player_index)]

            if self.direction == 'down':
                self.speedy = 1
                self.speedx = -2
                self.image = pygame.transform.flip(
                    self.player_walk_down[int(self.player_index)], True, False)

            self.rect.x += self.speedx
            self.rect.y += self.speedy

        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

    def animation(self):
        if self.health > 0:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk_down):
                self.player_index = 0

        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk_down):
                self.player_index = len(self.player_walk_down) - 1

            self.image = self.player_death[int(self.player_index)]
            self.image = pygame.transform.scale(
                self.image, (self.width, self.height))

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

    def update(self):
        # SCREEN.blit(border, self.border_rect)

        offset_x, offset_y = (
            self.border_rect.x-self.rect.x), (self.border_rect.y-self.rect.y)

        keys = pygame.key.get_pressed()
        if self.step_index >= 16:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction = 'up'
                self.step_index = 0
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction = 'down'
                self.step_index = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction = 'left'
                self.step_index = 0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction = 'right'
                self.step_index = 0

            if keys[pygame.K_SPACE] and self.shoot_cooldown < 0 and self.armed:
                self.fire = True
                self.shoot_cooldown = 10

        else:
            self.step_index += 1
            self.move()
            self.animation()

        if not self.mask.overlap(self.border_mask, (offset_x, offset_y)):
            self.health -= 1


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
            pygame.draw.line(SCREEN, GREEN, [player.rect.centerx, player.rect.centery], [
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
