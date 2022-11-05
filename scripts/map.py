import pygame
from scripts.constants import *
from scripts.assets import *

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
        # Vytvoření posunu všech bloků
        off_set = NUMBER_OF_BLOCKS * \
            (NUMBER_OF_BLOCKS / 2 / NUMBER_OF_BLOCKS) * \
            self.width - self.width / 2

        # Upravování pozice na základě obdržené pozice (x, y)
        self.rect.x = (self.x * 1 + self.y * -1) * self.width / 2 + off_set
        self.rect.y = (self.x * 0.5 + self.y * 0.5) * self.height / 2

        # Zobrazení bloku
        SCREEN.blit(self.image, self.rect)
        self.collide_point = pygame.Rect(
            self.rect.centerx - 5, self.rect.centery - 10, 15, 1)

        # Bod kolize
        if HITBOX:
            pygame.draw.rect(SCREEN, RED,  self.collide_point)

        # pygame.draw.polygon(SCREEN, (255, 255, 255), [
            # (self.rect.x + 32, self.rect.y + 8), (self.rect.x + 64, self.rect.y + 24), (self.rect.x + 32, self.rect.y + 40), (self.rect.x, self.rect.y + 24)])


class IsoMap:
    def __init__(self, map):
        self.map = map
        self.blocks = []

    def create_map(self):
        # Vytvoření herní mapy
        for floor in range(len(self.map)):
            for i in range(len(self.map[floor])):
                for j in range(len(self.map[floor])):
                    if self.map[floor][i][j] == 0:
                        continue
                    elif self.map[floor][i][j] == 1:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, grass, floor))
                    elif self.map[floor][i][j] == 2:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, grass1, floor))
                    elif self.map[floor][i][j] == 3:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, grass2, floor))
                    elif self.map[floor][i][j] == 4:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, stone, floor))
                    elif self.map[floor][i][j] == 5:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, stone1, floor))
                    elif self.map[floor][i][j] == 6:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, water, floor))
                    elif self.map[floor][i][j] == 7:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, bush, floor))
                    elif self.map[floor][i][j] == 8:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, PIXELS, PIXELS, flower, floor))
                    elif self.map[floor][i][j] == 9:
                        self.blocks.append(
                            Block(i - floor * 0.5, j - floor * 0.5, 180, 140, shop, floor, True))

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

                # Kolize s obchodem a nasledný vstup do obchodu
                if layer2.action and player.rect.colliderect(layer2.collide_point) and layer2.floor == player.last_collistion + 1:
                    shop_menu.pause = True
                    shop_menu.update()

        # Vykreslení nepřítele a kolize s hráčem
        for enemy in enemies:
            enemy.draw()
            enemy.move(player)
            enemy.animation(enemies)
            player.collision_enemy(enemy)

        # pygame.draw.polygon(SCREEN, (255, 0, 0), [
            # (WIDTH/2, - PIXELS + 8), (WIDTH + PIXELS, HEIGHT/2), (WIDTH/2, HEIGHT + PIXELS / 2), (-2 * PIXELS + PIXELS, HEIGHT/2)], 2)
