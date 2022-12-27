import pygame

from scripts.constants import *
from scripts.assets import *


class AbstractUtilities:
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
        if len(str(seconds)) < 2:
            seconds = "0" + str(seconds)
        self.draw_text(f"{minutes}:{seconds}",
                       BLUE, 200, WIDTH/2, 200)

    def update(self):
        self.draw_text("@Adam", BLACK, 50, WIDTH-70, HEIGHT - 20)
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
        self.price = 0
        self.delay = 0

    def exit(self):
        rect = button_exit.get_rect(topleft=(10, 10))
        SCREEN.blit(button_exit, rect)

        if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.player.step_index = 20
            self.player.rect.x = 614
            self.player.rect.y = 182
            self.pause = False

    def draw_btn(self, x, y, width, height, image, color, color_active, price, type):
        COLOR = color
        image = pygame.transform.scale(
            image, (width, height))
        rect = image.get_rect(topleft=(x, y))

        if self.delay <= 1:
            self.delay += 1

        if rect.collidepoint(pygame.mouse.get_pos()) and self.delay > 1:
            color = color_active
            if pygame.mouse.get_pressed()[0] and price + self.price <= self.player.coins:
                self.player.coins -= price + self.price
                self.price += price
                self.delay = 0
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
        self.draw_text(f'price: {self.price + price}', YELLOW,
                       30, x + width/2, y + height-30)

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
        self.draw_text("@Adam", BLACK, 50, WIDTH-70, HEIGHT - 20)

    def update(self):
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.player.step_index = 20
                        self.player.rect.x = 611
                        self.player.rect.y = 70
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
        self.draw_text("@Adam", BLACK, 50, WIDTH-70, HEIGHT - 20)
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


class Pause(AbstractUtilities):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            image, (80, 80))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.pause = False
        self.delay = 0

        self.resume_image = pygame.transform.scale(
            button_resume, (300, 110))
        self.resume_rect = self.resume_image.get_rect(center=(WIDTH/2, 230))

        self.restart_image = pygame.transform.scale(
            button_restart, (300, 110))
        self.restart_rect = self.restart_image.get_rect(center=(WIDTH/2, 350))

    def draw(self):
        self.draw_text("@Adam", BLACK, 50, WIDTH-70, HEIGHT - 20)
        SCREEN.blit(self.image, self.rect)

    def update(self, restart):
        self.draw()

        if self.delay <= 1:
            self.delay += 1
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.delay > 1:
            self.pause = not self.pause
            self.delay = 0

        if self.pause:
            if self.resume_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.delay > 1:
                self.pause = not self.pause
                self.delay = 0
            if self.restart_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.delay > 1:
                restart()
                self.pause = not self.pause
                self.delay = 0

    def run(self, restart):
        while self.pause:
            SCREEN.fill(GREY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = False

            self.update(restart)
            SCREEN.blit(self.resume_image, self.resume_rect)
            SCREEN.blit(self.restart_image, self.restart_rect)

            pygame.display.update()
            CLOCK.tick(15)


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
