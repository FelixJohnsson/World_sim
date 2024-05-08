import random

# SYMBOLS
W = '≈'
S = '/'
G = '_'
WALL = 'W'
OUT_OF_BOUNDS = 'x'

# TILE TYPES
class WATER:
    def __init__(self):
        self.type = 'water'
        self.nutrients = 0
        self.symbol = W
        self.color = (63, 154, 233)

class SAND:
    def __init__(self):
        self.type = 'sand'
        self.nutrients = round(random.uniform(0, 2) * 0.1, 3)
        self.symbol = S
        self.color = (233, 216, 63)

class GROUND:
    def __init__(self):
        self.type = 'ground'
        self.nutrients = round(random.uniform(0, 1), 3)
        self.symbol = G
        self.color = (33, 192, 21)
        self.plants = []
        self.creatures = []

# Configuration parameters
WATER_CHANCE = 0.001 
CHANCE_OF_SAND_NEAR_WATER = 0.3
EXPAND_WATER_CHANCE = 0.47
MAX_LAKE_SIZE = 300 

def generate_map(height, width):
    game_map = [[GROUND() for _ in range(width)] for _ in range(height)]

    def count_water_adjacent(y, x):
        water_count = 0
        for i in range(-3, 4):
            for j in range(-3, 4):
                if 0 <= y + i < height and 0 <= x + j < width:
                    tile = game_map[y + i][x + j]
                    if tile.type == 'water':
                        water_count += 1
        return water_count

    def form_lake(y, x, size=0):
        if 0 <= y < height and 0 <= x < width:
            tile = game_map[y][x]
            if tile.type == 'ground' and size < MAX_LAKE_SIZE:
                game_map[y][x] = WATER()
                size += 1
                # Randomly grow the lake in all directions
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(directions)
                for dy, dx in directions:
                    if random.random() < EXPAND_WATER_CHANCE:
                        form_lake(y + dy, x + dx, size)
        
                    
    def generate_nutrients_for_tiles():
        for y in range(height):
            for x in range(width):
                tile = game_map[y][x]
                if tile.type == 'ground':
                    water_count = count_water_adjacent(y, x)
                    tile.nutrients += water_count * 0.2
                elif tile.type == 'sand':
                    tile.nutrients = 0.1

    # Generate water
    for y in range(height):
        for x in range(width):
            if random.random() < WATER_CHANCE:
                form_lake(y, x)

    # Generate sand around water
    for y in range(height):
        for x in range(width):
            tile = game_map[y][x]
            if tile.type == 'ground' and count_water_adjacent(y, x) > 0:
                if random.random() < CHANCE_OF_SAND_NEAR_WATER:
                    game_map[y][x] = SAND()
                    
    generate_nutrients_for_tiles()

    return game_map