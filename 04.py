import os
from aoc_utils import Grid2d, Vector2, ALL_DIRECTIONS, DOWN_LEFT, DOWN_RIGHT, UP_LEFT, UP_RIGHT
from collections import defaultdict

with open(f"./inp/{os.path.basename(__file__).split('.')[0]}.txt") as f:
    grid = Grid2d('.', f.read().split('\n'))

maxes = grid.get_bounds()[1]

# Part A
xmases = 0
for y in range(maxes.y + 1):
    for x in range(maxes.x + 1):
        
        curr = Vector2(x, y)   #  Starting point
        
        for direction in ALL_DIRECTIONS: # Check all directions to look for "xmas"
            if grid[curr] == 'X' and grid[curr + direction] == 'M' and grid[curr + (direction * 2)] == 'A' and grid[curr + (direction * 3)] == 'S':
                xmases += 1
                
print(xmases)

# Part B
xmases = 0
all_as = [k for k, v in grid.items() if grid[k] == 'A']
opposites = defaultdict(lambda: 0, {"M": "S", "S": "M"})
for a in all_as:
    up_left = grid[a + UP_LEFT]
    up_right = grid[a + UP_RIGHT]
    down_left = grid[a + DOWN_LEFT]
    down_right = grid[a + DOWN_RIGHT]
    
    if up_left in opposites.keys() and down_right == opposites[up_left] and down_left in opposites.keys() and up_right == opposites[down_left]:
        xmases += 1
        
print(xmases)