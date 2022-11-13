import pygame
from sys import exit
from random import choice

from scripts.constants import *
from scripts.assets import *
from scripts.items import Gun, Heal, Coin
from scripts.particle import FireBall
from scripts.map import IsoMap
from scripts.utils import HeartBar, MainMenu, Shop, Timer, CoinSack, ObjectSpawner, Pause
from scripts.moveable import Player, Enemy

# Start pygame
pygame.init()
pygame.display.set_caption(NAME)


class Game():
    def __init__(self):
        # Vytvoreni mapy
        self.iso_map = IsoMap(MAP)
        self.iso_map.create_map()

        # Hlavni menu hry
        self.main_menu = MainMenu()
        self.pause = Pause(WIDTH-70, 5, button_pause)

        # Vytvorecni hrace
        self.player = Player(WIDTH / 2 + 5, HEIGHT / 2 -
                             10, PIXELS - 12, PIXELS - 8)

        # Vytvoreni pomocnych ukazatelu
        self.shop_menu = Shop(self.player)
        self.coin_sack = CoinSack(WIDTH - 150, 20, 50, 50, coin_sack_img)
        self.timer = Timer(WIDTH / 2, HEIGHT - 50)
        # self.health_bar = HealthBar(50, 50, 125)
        self.heart_bar = HeartBar(125)

        # Vytvoreni listu pro objekty
        self.enemies = []
        self.fireballs = []
        self.collectable_items = []
        self.bullets = []

        # Vytvoreni autovaticky se objevujicich objektu
        self.object_spawner = ObjectSpawner(5 * FPS, self.collectable_items)
        self.enemy_spawner = ObjectSpawner(5 * FPS, self.enemies)
        self.fireball_spawner = ObjectSpawner(2 * FPS, self.fireballs)

        self.difficulty = 1

    def restart(self):
        # Vycisteni listu
        self.enemies.clear()
        self.fireballs.clear()
        self.collectable_items.clear()
        self.bullets.clear()

        # Resotovani pozice hrace
        self.player.rect.x, self.player.rect.y = WIDTH / 2 + 5, HEIGHT / 2 - 10
        self.player.last_collistion = 2

        self.player.health = 125
        for heart in self.heart_bar.hearts:
            heart.heart_index = 0

        self.shop_menu.price = 0
        self.player.add_ammo = 2
        self.player.add_heal = 5
        self.player.coin_spawn = 1
        self.player.ammo = 0
        self.player.coins = 0
        self.player.image = pygame.transform.scale(
            self.player.player_walk_down[int(self.player.player_index)], (self.player.width, self.player.height))

        # Resetovani casomiry
        self.timer.sec = 0

    def draw(self):
        self.iso_map.draw(self.player, self.enemies, self.shop_menu)
        # self.health_bar.draw(self.player.health)
        self.coin_sack.draw(self.player)

    def update(self):
        self.draw()

        self.heart_bar.update(self.player.health)

        self.player.update()
        self.player.shoot(self.bullets)

        for item in self.collectable_items:
            item.update(self.player, self.collectable_items)

        # Spawn Guns
        self.object_spawner.spawn(choice(
            [Gun(0, 0, PIXELS - 37, PIXELS - 45, gun), Heal(0, 0, PIXELS - 40, PIXELS - 35, heal), Coin(0, 0, PIXELS - 20, PIXELS - 30, [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6])]))

        if len(self.enemies) < self.difficulty:
            self.enemy_spawner.spawn(Enemy(choice([WIDTH / 2, 0, WIDTH]), choice([0, HEIGHT]),
                                           PIXELS - 12, PIXELS - 8, self.player))

        for bullet in self.bullets:
            bullet.update(self.player.direction)
            for enemy in self.enemies:
                enemy.bullet_collision(bullet, self.bullets)

        self.fireball_spawner.spawn(FireBall(-100, -100))
        for fireball in self.fireballs:
            fireball.update(self.player)
            self.player.collision_fireball(fireball)
            self.fireball_spawner.delete(10 * FPS)

        if self.player.health > 0:
            self.timer.update()
        else:
            self.timer.draw_final()

        if self.timer.timer >= 60 and self.timer.sec % 30 == 0:
            self.difficulty += 1

        self.pause.update()

    def run(self):
        bg_music.play(loops=-1)
        while True:
            SCREEN.fill(GREY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause.pause = True

                    if event.key == pygame.K_r:
                        self.restart()

                    if event.key == pygame.K_o:
                        self.player.health += 1

                    if event.key == pygame.K_p:
                        self.player.health -= 1

            self.main_menu.run()
            self.pause.run()
            self.update()

            pygame.display.update()
            CLOCK.tick(FPS)
