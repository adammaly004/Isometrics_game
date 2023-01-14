
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

            for y in range(self.border):
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

            i += 1

        else:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    chance = random.randint(0, 10)
                    if grid[i][j] == 0 and chance == 10:
                        grid[i][j] = random.choice([7, 8])

                    if i < 6 and j > 15:
                        grid[j][i] = 0

                    if i == 0 or i == 1:
                        grid[i][j] = 0

                    elif i == len(grid)-1 or i == len(grid)-2:
                        grid[i][j] = 0

                    if j == 0 or j == 1:
                        grid[i][j] = 0

                    elif j == len(grid[i])-1 or j == len(grid[i])-2:
                        grid[i][j] = 0

        grid[-5][0] = 9

        return grid

    def new_floor(self, grid):
        first = True
        first1 = True
        for i in range(len(grid)):
            for j in range(len(grid[i])):

                if grid[i][j] >= 1 and first:
                    grid[i][j] = 0
                    first = False

                elif grid[i][j] == 0 and not first:
                    grid[i][j-1] = 0
                    grid[i][j-2] = 0
                    first = True

                if grid[i-1][j] >= 1 and first1:
                    grid[i-1][j] = 0
                    first1 = False

                elif grid[i-1][j] == 0 and not first1:
                    first1 = True

        for j in range(len(grid)):
            for i in range(len(grid[j])):

                if grid[i][j] >= 1 and first:
                    grid[i][j] = 0
                    first = False

                elif grid[i][j] == 0 and not first:
                    grid[i - 1][j] = 0
                    grid[i-2][j] = 0
                    first = True

                if grid[i-1][j] >= 1 and first1:
                    grid[i-1][j] = 0
                    first1 = False

                elif grid[i-1][j] == 0 and not first1:
                    first1 = True

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
        floor1 = self.first_floor()
        old = self.apply_automation(self.grid)
        floor2 = copy.deepcopy(old)
        old2 = self.new_floor(old)
        floor3 = copy.deepcopy(old2)
        floor4 = self.new_floor(old2)

        return [floor1, floor2, floor3, floor4]
