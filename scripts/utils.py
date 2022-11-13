from turtle import width
import pygame

from scripts.constants import *
from scripts.assets import *


class AbstractUtilities:
    def draw_button(self, x, y, width, height, color, price, type):
        rect = pygame.Rect(x - width/2, y, width, height)
        pygame.draw.rect(SCREEN, YELLOW, rect)
        pygame.draw.rect(SCREEN, color, rect, 10)

        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and price <= self.player.coins:
            self.player.coins -= price
            if type == 'heal':
                self.player.add_heal += 5
            elif type == 'gun':
                self.player.add_ammo += 1
            elif type == 'coin':
                self.player.coin_spawn += 1

    def draw_btn(self, x, y, width, height, image, color, color_active, price, type):
        COLOR = color
        image = pygame.transform.scale(
            image, (width, height))
        rect = image.get_rect(topleft=(x, y))

        if rect.collidepoint(pygame.mouse.get_pos()):
            color = color_active
            if pygame.mouse.get_pressed()[0] and price <= self.player.coins:
                self.player.coins -= price
                if type == 'heal':
                    self.player.add_heal += 5
                elif type == 'gun':
                    self.player.add_ammo += 1
                elif type == 'coin':
                    self.player.coin_spawn += 1
        else:
            color = COLOR
        pygame.draw.rect(SCREEN, color, rect)
        SCREEN.blit(image, rect)

    def draw_text(self, text, color, size, x, y):
        font = pygame.font.Font(font_type, size)
        text = font.render(str(text), False, color)
        text_rect = text.get_rect(center=(x, y))
        SCREEN.blit(text, text_rect)

    def draw_image_button(self, x, y, width, image):
        ratio = image.get_height()/image.get_width()
        image = pygame.transform.scale(
            image, (width, int(width*ratio)))
        rect = image.get_rect(center=(x, y))

        SCREEN.blit(image, rect)


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
        SCREEN.blit(self.image, self.rect)
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
        minutes, seconds = divmod(self.sec, 60)

        if len(str(seconds)) < 2:
            seconds = "0" + str(seconds)

        self.draw_text(f"{minutes}:{seconds}",
                       BLUE, 50, self.x, self.y)

    def draw_final(self):
        minutes, seconds = divmod(self.sec, 60)

        self.draw_text(f"{minutes}:{seconds}",
                       BLUE, 200, WIDTH/2, 200)

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
        self.coin_sack = CoinSack(WIDTH - 150, 20, 50, 50, coin_sack_img)
        self.pause = False

    def exit(self):
        """rect = pygame.Rect(10, 10, 100, 50)
        pygame.draw.rect(SCREEN, RED, rect)
        pygame.draw.rect(SCREEN, BLACK, rect, 10)
        self.draw_text("Exit", GREEN, 50, 60, 40)"""
        rect = button_exit.get_rect(topleft=(10, 10))
        SCREEN.blit(button_exit, rect)

        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.player.step_index = 20
            self.player.rect.x = 614
            self.player.rect.y = 182
            self.pause = False

    def draw(self):
        SCREEN.fill(GREY)
        SCREEN.blit(shop_inside, (50, -20))
        self.draw_btn(WIDTH * 0.2+50, 300, 200, 300,
                      button_heal, (238, 70, 44), (255, 34, 0), 1, 'heal')
        self.draw_btn(WIDTH * 0.4+50, 300, 200, 300,
                      button_gun, (179, 202, 190), (0, 255, 122), 2, 'gun')
        self.draw_btn(WIDTH * 0.6+50, 300, 200, 300,
                      button_coin, (255, 168, 0), (255, 214, 0), 3, 'coin')
        self.exit()
        self.coin_sack.draw(self.player)

    def update(self):
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.player.step_index = 20
                        self.player.rect.x = 614
                        self.player.rect.y = 182
                        self.pause = False

            self.draw()

            pygame.display.update()
            CLOCK.tick(15)


class MainMenu(AbstractUtilities):
    def __init__(self):
        super().__init__()
        self.main_menu = True
        self.y = 0
        self.dy = 1
        self.vy = 0
        self.rect = button_start.get_rect(topleft=(500, self.y+300))

    def draw(self):
        # self.draw_text("Welcome to my Iso Game", RED, 100, WIDTH/2, 100)
        # self.draw_text("Press space to start the game...",
        # GREEN, 70, WIDTH/2, 200)
        SCREEN.blit(thumbnail, (0, self.y))
        SCREEN.blit(button_start, (500, self.y+300))

    def update(self):
        self.vy += self.dy
        if self.vy > 2 or self.vy < -2:
            self.dy *= -1
        self.y += self.vy

        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.main_menu = False

    def run(self):
        while self.main_menu:
            SCREEN.fill(GREY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.main_menu = False

            self.draw()
            self.update()

            pygame.display.update()
            CLOCK.tick(15)


class Pause:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            image, (80, 80))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.pause = False

    def draw(self):
        SCREEN.blit(self.image, self.rect)

    def update(self):
        self.draw()
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.pause = True

    def run(self):
        while self.pause:
            SCREEN.fill(GREY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = False

            self.update()

            pygame.display.update()
            CLOCK.tick(15)


"""class HealthBar:
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
        pygame.draw.rect(SCREEN, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(SCREEN, GREEN,
                         (self.x, self.y, 150 * ratio, 20))"""


class Heart:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.heart_index = 0
        self.hearts = [heart1, heart2, heart3, heart4, heart5]
        self.image = pygame.transform.scale(
            self.hearts[self.heart_index], (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        self.image = pygame.transform.scale(
            self.hearts[self.heart_index], (self.width, self.height))
        SCREEN.blit(self.image, self.rect)


class HeartBar:
    def __init__(self, max_health):
        self.health = max_health
        self.max_health = max_health
        self.hearts = [Heart(30, 30, 30, 30), Heart(60, 30, 30, 30), Heart(
            90, 30, 30, 30), Heart(120, 30, 30, 30), Heart(150, 30, 30, 30)]

        self.health_index = 0

    def draw(self):
        for heart in self.hearts:
            heart.draw()

    def update(self, health):
        self.draw()
        if health > 0:
            self.health_index = int(health / 25)
            if self.health_index < 5:
                index = int(((self.max_health - health-1) -
                             (5 - self.health_index)*25) / 5)
                if index == 0:
                    index = -1
                self.hearts[self.health_index].heart_index = index

            for i in range(self.health_index):
                self.hearts[i].heart_index = 0


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
