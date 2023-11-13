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
        self.nutrients = 0.1
        self.symbol = S
        self.color = (233, 216, 63)

class GROUND:
    def __init__(self):
        self.type = 'ground'
        self.nutrients = 0.5
        self.symbol = G
        self.color = (33, 192, 21)
        self.plants = []
        self.creatures = []

# Configuration parameters
WATER_CHANCE = 0.001  # Chance to start forming a lake
CHANCE_OF_SAND_NEAR_WATER = 0.3  # Chance to turn a ground tile into sand if it's adjacent to water
EXPAND_WATER_CHANCE = 0.47  # Chance for water to expand and form a lake
MAX_LAKE_SIZE = 300  # Maximum number of tiles a lake can have

def generate_map(height, width):
    game_map = [[GROUND() for _ in range(width)] for _ in range(height)]

    def count_water_adjacent(y, x):
        water_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
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
        
                    
    def generate_nutrients_map():
        pass

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

    return {
        'map': game_map,
    }