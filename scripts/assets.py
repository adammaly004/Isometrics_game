import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 640))

# Assets
grass1 = pygame.image.load('assets/img/blocks/grass1.png').convert_alpha()
grass2 = pygame.image.load('assets/img/blocks/grass2.png').convert_alpha()
grass = pygame.image.load('assets/img/blocks/grass.png').convert_alpha()
stone = pygame.image.load('assets/img/blocks/stone.png').convert_alpha()
stone1 = pygame.image.load('assets/img/blocks/stone1.png').convert_alpha()
bush = pygame.image.load('assets/img/blocks/bush.png').convert_alpha()
flower = pygame.image.load('assets/img/blocks/flower.png').convert_alpha()
water = pygame.image.load('assets/img/blocks/water.png').convert_alpha()

player_up2 = pygame.image.load('assets/img/player/up2.png').convert_alpha()
player_up3 = pygame.image.load('assets/img/player/up3.png').convert_alpha()
player_up4 = pygame.image.load('assets/img/player/up4.png').convert_alpha()
player_up1 = pygame.image.load('assets/img/player/up1.png').convert_alpha()

player_down1 = pygame.image.load('assets/img/player/down1.png').convert_alpha()
player_down2 = pygame.image.load('assets/img/player/down2.png').convert_alpha()
player_down3 = pygame.image.load('assets/img/player/down3.png').convert_alpha()
player_down4 = pygame.image.load('assets/img/player/down4.png').convert_alpha()

player_death1 = pygame.image.load(
    'assets/img/player/death1.png').convert_alpha()
player_death2 = pygame.image.load(
    'assets/img/player/death2.png').convert_alpha()
player_death3 = pygame.image.load(
    'assets/img/player/death3.png').convert_alpha()
player_death4 = pygame.image.load(
    'assets/img/player/death4.png').convert_alpha()

enemy_down1 = pygame.image.load('assets/img/enemy/down1.png').convert_alpha()
enemy_down2 = pygame.image.load('assets/img/enemy/down2.png').convert_alpha()

enemy_up1 = pygame.image.load('assets/img/enemy/up1.png').convert_alpha()
enemy_up2 = pygame.image.load('assets/img/enemy/up2.png').convert_alpha()

enemy_death1 = pygame.image.load('assets/img/enemy/death1.png').convert_alpha()
enemy_death2 = pygame.image.load('assets/img/enemy/death2.png').convert_alpha()
enemy_death3 = pygame.image.load('assets/img/enemy/death3.png').convert_alpha()
enemy_death4 = pygame.image.load('assets/img/enemy/death4.png').convert_alpha()
enemy_death5 = pygame.image.load('assets/img/enemy/death5.png').convert_alpha()

gun = pygame.image.load('assets/img/items/shot_side.png').convert_alpha()
heal = pygame.image.load('assets/img/items/heal.png').convert_alpha()

coin_1 = pygame.image.load('assets/img/items/coin/coin_1.png').convert_alpha()
coin_2 = pygame.image.load('assets/img/items/coin/coin_2.png').convert_alpha()
coin_3 = pygame.image.load('assets/img/items/coin/coin_3.png').convert_alpha()
coin_4 = pygame.image.load('assets/img/items/coin/coin_4.png').convert_alpha()
coin_5 = pygame.image.load('assets/img/items/coin/coin_5.png').convert_alpha()
coin_6 = pygame.image.load('assets/img/items/coin/coin_6.png').convert_alpha()


coin_sack_img = pygame.image.load(
    'assets/img/items/coin_sack.png').convert_alpha()

button_heal = pygame.image.load(
    'assets/img/buttons/button_heal1.png').convert_alpha()
button_gun = pygame.image.load(
    'assets/img/buttons/button_gun.png').convert_alpha()
button_coin = pygame.image.load(
    'assets/img/buttons/button_coin.png').convert_alpha()
button_exit = pygame.image.load(
    'assets/img/buttons/button_exit.png').convert_alpha()
button_start = pygame.image.load(
    'assets/img/buttons/button_start.png').convert_alpha()

shop_inside = pygame.image.load(
    'assets/img/shop/shop_inside.png').convert_alpha()
shop = pygame.image.load('assets/img/shop/shop.png').convert_alpha()

thumbnail = pygame.image.load('assets/img/game/main_menu.png').convert_alpha()

border = pygame.image.load('assets/img/game/border.png').convert_alpha()

# Load fonts
font_type = 'assets/Pixeltype.ttf'
