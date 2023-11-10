from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from map import generate_map
import time
import cProfile
import random

colorama_init()

# CONSTANTS
W = '≈'
S = '/'
G = '-'
WALL = 'W'
OUT_OF_BOUNDS = 'x'

# CREATURES
CREATURE = '0'

# PLANTS, TREES
TREE_SPECIES = [
    {
        "name": 'Teak',
        "growth_rate": 0.1,
        "max_age": 50,
        "stages": [
            ".",
            ":",
            "t",
            "T",
        ]
    },
    {
        "name": 'Bak',
        "growth_rate": 0.2,
        "max_age": 30,
        "stages": [
            ".",
            ":",
            "b",
            "B",
        ]
    },
    {
        "name": 'Pine',
        "growth_rate": 0.3,
        "max_age": 20,
        "stages": [
            ".",
            ":",
            "p",
            "P",
        ]
    },
]

# FOOD
F = 'F'

class Tree(object):
    def __init__(self, x, y, species):
        self.MAX_AGE = species['max_age']
        self.GROWTH_RATE = species['growth_rate']
        
        self.x = x
        self.y = y
        self.species = species
        self.growth_stage = 0
        self.symbol = f'{species['name'][0].lower()}'
        self.seeding_counter = 0
        
    def grow(self):
        self.growth_stage += self.GROWTH_RATE
        if self.growth_stage >= 10:
            if self.symbol != self.species['name'][0].upper():
                self.symbol = self.species['name'][0].upper()
            self.seeding_counter += 1
            
    def is_dead(self):
        return self.growth_stage > self.MAX_AGE
        

class Map (object):
    # A grid map for the grid tamagotchi game.
    # Will be used as an environment for the RL agent.
    def __init__ (self):
        self.width = 120
        self.height = 30
        self.map = generate_map(self.height, self.width) 
        self.plants = []

    def generate_new_map (self):
        self.map = map
    
    def print_map(self):
        for row in self.map:
            row_str = ''.join([self.get_tile_color(tile) + tile for tile in row])
            print(row_str + Style.RESET_ALL)
            
    def get_tile_color(self, tile):
        if tile == W:
            return Fore.BLUE
        elif tile == S:
            return Fore.YELLOW
        elif tile == G:
            return Fore.GREEN
        elif tile == F:
            return Fore.RED
        elif tile == CREATURE:
            return Fore.MAGENTA
        elif tile == WALL:
            return Fore.BLACK
        elif tile == OUT_OF_BOUNDS:
            return Fore.WHITE
        else:
            return Fore.WHITE
    
    def get_map(self):
        return self.map
    
    def set_tile(self, x, y, tile):
        self.map[y][x] = tile
        
    def get_tile(self, x, y):
        return self.map[y][x]
    
    def move_tile(self, x, y, new_x, new_y):
        tile = self.get_tile(x, y)
        self.set_tile(x, y, S)
        self.set_tile(new_x, new_y, tile)

    def is_tile_water(self, x, y):
        return self.get_tile(x, y) == W
    
    def is_tile_sand(self, x, y):
        return self.get_tile(x, y) == S
    
    def is_tile_ground(self, x, y):
        return self.get_tile(x, y) == G
    
    def is_tile_occupied(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.is_tile_ground(x, y):
                return False
            else: 
                return True

    def get_observation(self, x, y, vision_range):
            observation = []
            for i in range(-vision_range, vision_range + 1):
                row = []
                for j in range(-vision_range, vision_range + 1):
                    if 0 <= x + j < self.width and 0 <= y + i < self.height:
                        row.append(self.get_tile(x + j, y + i))
                    else:
                        row.append('x')
                observation.append(row)
            return observation

    def print_observation(self, x, y, vision_range):
        observation = self.get_observation(x, y, vision_range)
        for row in observation:
            for tile in row:
                if tile == W:
                    print(Fore.BLUE + tile, end='')
                elif tile == S:
                    print(Fore.YELLOW + tile, end='')
                elif tile == G:
                    print(Fore.GREEN + tile, end='')
                elif tile == F:
                    print(Fore.RED + tile, end='')
                elif tile == CREATURE:
                    print(Fore.MAGENTA + tile, end='')
                else:
                    print(Fore.WHITE + tile, end='')
            print(Style.RESET_ALL)

    def find_all_tiles(self, tile_type):
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                if self.get_tile(x, y) == tile_type:
                    tiles.append((x, y))
        return tiles

    def get_adjacent_tiles(self, x, y):
        tiles = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                tiles.append((x + i, y + j))
        return tiles

    def calculate_distance(self, x1, y1, x2, y2):
        return abs(x2 - x1) + abs(y2 - y1)
    
    def plant_tree(self, x, y, species):
        if 0 <= x < self.width and 0 <= y < self.height:
            new_tree = Tree(x, y, species)
            if self.is_tile_ground(x, y):
                self.set_tile(x, y, new_tree.symbol)
                self.plants.append(new_tree)
                return True
        
        return False
    
    def grow_all_plants(self):
        tile_updates = {}

        for plant in self.plants:
            plant.grow()
            if plant.is_dead():
                tile_updates[(plant.x, plant.y)] = G
            else:
                if self.map[plant.y][plant.x] != plant.symbol:
                    tile_updates[(plant.x, plant.y)] = plant.symbol

        for (x, y), symbol in tile_updates.items():
            self.set_tile(x, y, symbol)

        self.plants = [plant for plant in self.plants if not plant.is_dead()]
            
    def seed_new_trees(self):
            SEEDING_INTERVAL = 5
            SEEDING_CHANCE = 0.1

            for plant in self.plants:
                if plant.growth_stage >= 10 and plant.seeding_counter >= SEEDING_INTERVAL:
                    plant.seeding_counter = 0
                    for adj_x, adj_y in self.get_adjacent_tiles(plant.x, plant.y):
                        if not self.is_tile_occupied(adj_x, adj_y) and random.random() < SEEDING_CHANCE:
                            self.plant_tree(adj_x, adj_y, plant.species)

NUMBER_OF_TREES = 10

def main():
    new_map = Map() 
    for _ in range(NUMBER_OF_TREES):
            successful = False
            while not successful:
                x = random.randint(0, new_map.width - 1)
                y = random.randint(0, new_map.height - 1)
                species = random.choice(TREE_SPECIES)
                successful = new_map.plant_tree(x, y, species)
                if not successful:
                    continue
            
    while True:
        new_map.grow_all_plants()
        new_map.seed_new_trees()
        new_map.print_map()
        time.sleep(.1)
        
if __name__ == '__main__':
    cProfile.run('main()')