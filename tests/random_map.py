import pygame
import sys
import random
pygame.init()

clock = pygame.time.Clock()
display = pygame.display.set_mode((640, 640))


def make_map(size, border):
    grid = []
    chance = random.randrange(0, 3)

    for _ in range(border+1):
        row = []
        grid.append(row)

        for _ in range(border+1):
            chance = random.randrange(0, 10)
            if chance <= 4:
                row.append(0)
            if chance >= 5:
                row.append(1)

    return grid


def load_map(size, grid, tiles):
    y = 0
    for layer in grid:
        x = 0
        for cell in layer:
            display.blit(tiles[cell], (x*size, y*size))
            x += 1
        y += 1


def apply_automation(grid, count, border):
    i = 0
    while i < count:
        y = 0
        for y in range(border):
            x = 0
            for x in range(border):
                one = 0
                zero = 0
                surrounding = [grid[y-1][x], grid[y+1][x], grid[y][x-1],
                               grid[y][x+1], grid[y+1][x+1], grid[y+1][x-1],
                               grid[y-1][x+1], grid[y-1][x-1]]

                for m in surrounding:
                    if m == 0:
                        zero += 1
                    else:
                        one += 1

                if zero > 4:
                    grid[y][x] = 0
                if one > 4:
                    grid[y][x] = random.randint(1, 7)

            x += 1
        y += 1
        i += 1

    return grid


def new_floor(grid):
    first = True
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] >= 1 and first:
                grid[i][j] = 0
                first = False

            elif grid[i][j] == 0 and not first:
                grid[i][j-1] = 0
                first = True

    return grid


def main():

    border = 20
    size = 32
    count = 10
    grid = make_map(size, border)

    mapping = apply_automation(grid, count, border)
    mapping2 = new_floor(mapping)

    black = pygame.Surface((size, size))
    black.fill((0, 0, 0))

    green = pygame.Surface((size, size))
    green.fill((0, 255, 0))

    blue = pygame.Surface((size, size))
    blue.fill((0, 0, 255))

    red = pygame.Surface((size, size))
    red.fill((255, 0, 0))

    yellow = pygame.Surface((size, size))
    yellow.fill((255, 255, 0))

    white = pygame.Surface((size, size))
    white.fill((255, 255, 255))

    lightblue = pygame.Surface((size, size))
    lightblue.fill((0, 255, 255))

    pink = pygame.Surface((size, size))
    pink.fill((255, 0, 255))

    tiles = [black, green, blue, white, lightblue, yellow, pink, red]

    print(mapping)
    print(mapping2)

    while True:

        load_map(size, mapping, tiles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == ord("k"):
                    main()

                if event.key == ord("l"):
                    count += 1
                    apply_automation(grid, count, border)
                    print(count)

        pygame.display.update()
        clock.tick(60)


main()
