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
        self.player = Player(1091, 310, PIXELS - 12, PIXELS - 8)

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
        self.player.rect.x, self.player.rect.y = 1091, 310
        self.player.last_collistion = 0

        self.player.health = 125
        for heart in self.heart_bar.hearts:
            heart.heart_index = 0

        self.shop_menu.price = 0
        self.player.add_ammo = 2
        self.player.add_heal = 5
        self.player.coin_spawn = 1
        self.player.ammo = 0
        self.player.armed = False
        self.player.coins = 0
        self.player.image = pygame.transform.scale(
            self.player.player_walk_down[int(self.player.player_index)], (self.player.width, self.player.height))

        # Resetovani casomiry
        self.timer.score = 0

    def draw(self):
        self.iso_map.draw(self.player, self.enemies, self.shop_menu)
        self.coin_sack.draw(self.player)

    def update(self):
        self.draw()

        self.heart_bar.update(self.player.health)

        self.player.update()

        if self.player.health > 0:
            self.player.shoot(self.bullets)

            for item in self.collectable_items:
                item.update(self.player, self.collectable_items)

            # Spawn Guns
            self.object_spawner.spawn(choice(
                [Gun(0, 0, PIXELS - 37, PIXELS - 45, gun), Heal(0, 0, PIXELS - 40, PIXELS - 35, heal), Coin(0, 0, PIXELS - 20, PIXELS - 30, [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6])]))

            if len(self.enemies) < self.difficulty:
                pos = choice([[611, 582], [613, -58], [1219, 278], [-1, 280]])
                self.enemy_spawner.spawn(Enemy(pos[0], pos[1],
                                               PIXELS - 12, PIXELS - 8, self.player))

            for bullet in self.bullets:
                bullet.update(self.player.direction)
                for enemy in self.enemies:
                    if enemy.bullet_collision(bullet, self.bullets):
                        self.timer.score += 1000

            self.fireball_spawner.spawn(FireBall(-100, -100))
            for fireball in self.fireballs:
                fireball.update(self.player)
                self.player.collision_fireball(fireball)
                self.fireball_spawner.delete(10 * FPS)

            if self.player.health > 0:
                self.timer.update()

            if len(str(self.timer.score)[:-3]) == 0:
                self.difficulty = 3
            else:
                self.difficulty = int(str(self.timer.score)[:-3])

        else:
            self.timer.draw_final()
        # if self.timer.score > 1000:
            #self.difficulty += 1

        self.pause.update(self.restart)

    def run(self):
        # bg_music.play(loops=-1)
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

            self.main_menu.run()
            self.pause.run(self.restart)
            self.update()

            pygame.display.update()
            CLOCK.tick(FPS)
