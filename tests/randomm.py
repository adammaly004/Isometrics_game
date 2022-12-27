
import copy
import random


class CreateMap:
    def __init__(self, border, size, count):
        self.border = border
        self.size = size
        self.count = count
        self.grid = self.make_map()

        self.map = []

    def make_map(self):
        grid = []
        chance = random.randrange(0, 3)

        for _ in range(self.border+1):
            row = []
            grid.append(row)

            for _ in range(self.border+1):
                chance = random.randrange(0, 10)
                if chance <= 4:
                    row.append(0)
                if chance >= 5:
                    row.append(1)

        return grid

    def apply_automation(self, grid):
        i = 0
        while i < self.count:
            y = 0
            for y in range(self.border):
                x = 0
                for x in range(self.border):
                    one = 0
                    zero = 0
                    surrounding = [grid[y-1][x], grid[y+1][x],
                                   grid[y][x-1], grid[y][x+1],
                                   grid[y + 1][x+1], grid[y+1][x-1],
                                   grid[y-1][x+1], grid[y-1][x-1]]

                    for m in surrounding:
                        if m == 0:
                            zero += 1
                        else:
                            one += 1

                    if zero > 4:
                        grid[y][x] = 0
                    if one > 4:
                        grid[y][x] = random.randint(1, 5)

                x += 1
            y += 1
            i += 1

        return grid

    def new_floor(self, grid):
        first = True
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] >= 1 and first:
                    grid[i][j] = 0
                    first = False

                if grid[i-1][j] >= 1 and first:
                    grid[i][j] = 0
                    first = False

                elif grid[i][j] == 0 and not first:
                    grid[i][j-1] = 0
                    first = True

        return grid

    def first_floor(self):
        grid = []
        for _ in range(self.border+1):
            row = []
            grid.append(row)
            for _ in range(self.border+1):
                row.append(random.randint(1, 5))

        return grid

    def create(self):
        map = []
        floor1 = self.first_floor()
        old = self.apply_automation(self.grid)
        floor2 = copy.deepcopy(old)
        old2 = self.new_floor(old)
        floor3 = copy.deepcopy(old2)
        floor4 = self.new_floor(old2)

        map.append(floor1)
        map.append(floor2)
        map.append(floor3)
        map.append(floor4)
        return map


create_map = CreateMap(19, 32, 10)


MAP = create_map.create()
print(MAP)
"""old = create_map.apply_automation(create_map.grid)
new = copy.deepcopy(old)
floor3 = create_map.new_floor(old)


print(old)
print(new)
print(floor3)"""

# MAP.append(FLOOR3)


"""border = 19
size = 32
count = 10
grid = make_map(size, border)

mapping = apply_automation(grid, count, border)
print(mapping)
mapping2 = new_floor(mapping)
print(mapping2)"""
