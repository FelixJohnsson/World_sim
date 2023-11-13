import random

# Constants
W = '≈'  # Water
S = '/'  # Sand
G = '-'  # Ground

# Configuration parameters
WATER_CHANCE = 0.005  # Chance to start forming a lake
CHANCE_OF_SAND_NEAR_WATER = 0.5  # Chance to turn a ground tile into sand if it's adjacent to water
EXPAND_WATER_CHANCE = 0.5  # Chance for water to expand and form a lake
MAX_LAKE_SIZE = 25  # Maximum number of tiles a lake can have

def generate_map(height, width):
    game_map = [[G for _ in range(width)] for _ in range(height)]

    # Helper function to count adjacent water tiles
    def count_water_adjacent(y, x):
        water_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= y + i < height and 0 <= x + j < width:
                    if game_map[y + i][x + j] == W:
                        water_count += 1
        return water_count

    # Recursive function to form a lake
    def form_lake(y, x, size=0):
        if 0 <= y < height and 0 <= x < width and game_map[y][x] == G and size < MAX_LAKE_SIZE:
            game_map[y][x] = W
            size += 1
            # Randomly grow the lake in all directions
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dy, dx in directions:
                if random.random() < EXPAND_WATER_CHANCE:
                    form_lake(y + dy, x + dx, size)
                    
    def generate_nutrients_map():
        nutrients_map = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if game_map[y][x] == G:
                    nutrients_map[y][x] = random.random() * 0.5
                    for i in range(-3, 5):
                        for j in range(-3, 5):
                            if 0 <= y + i < height and 0 <= x + j < width:
                                if game_map[y + i][x + j] == W:
                                    nutrients_map[y][x] += 0.1
                elif game_map[y][x] == S:
                    nutrients_map[y][x] = 0.1
                elif game_map[y][x] == W:
                    nutrients_map[y][x] = 0
        return nutrients_map

    # Generate water
    for y in range(height):
        for x in range(width):
            if random.random() < WATER_CHANCE:
                form_lake(y, x)

    # Generate sand around water
    for y in range(height):
        for x in range(width):
            if game_map[y][x] == G and count_water_adjacent(y, x) > 0:
                if random.random() < CHANCE_OF_SAND_NEAR_WATER:
                    game_map[y][x] = S

    return {
        'map': game_map,
        'nutrients_map': generate_nutrients_map()
    }