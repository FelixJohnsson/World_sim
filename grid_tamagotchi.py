from colorama import init as colorama_init
from colorama import Fore, Back, Style
from map import generate_map, W, S, G, WALL, OUT_OF_BOUNDS
from tree import Tree
from bush import Bush

import time
import cProfile
import random

colorama_init(autoreset=True)


# CREATURES
CREATURE = '0'

# PLANTS, TREES
TREE_SPECIES = [
    {
        "name": 'Teak',
        "growth_rate": 0.1,
        "max_age": 70,
        "stages": [
            ".",
            ":",
            "t",
            "T",
        ]
    },
    {
        "name": 'Aak',
        "growth_rate": 0.2,
        "max_age": 55,
        "stages": [
            ".",
            ":",
            "a",
            "A",
        ]
    },
    {
        "name": 'Pine',
        "growth_rate": 0.3,
        "max_age": 40,
        "stages": [
            ".",
            ":",
            "p",
            "P",
        ]
    },
]

BUSH_SPECIES = [
    {
        "name": 'Berry Bush',
        "growth_rate": 0.1,
        "max_age": 70,
        "stages": [
            "-",
            "=",
            "b",
            "B",
        ]
    },
]

# FOOD
F = 'F'


class World (object):
    # A grid map for the grid tamagotchi game.
    # Will be used as an environment for the RL agent.
    def __init__ (self, height, width):
        self.width = width
        self.height = height
        maps = generate_map(self.height, self.width)
        self.map = maps['map']
        self.nutrients_map = maps['nutrients_map']
        self.plants = []

    def print_map(self):
        for y, row in enumerate(self.map):
            row_str = ''.join([self.get_tile_color(tile, x, y) + tile + Style.RESET_ALL for x, tile in enumerate(row)])
            print(row_str + Style.RESET_ALL)
            
    def get_tile_color(self, tile, x, y):
        if tile == W:
            return Back.BLUE + Style.DIM + Fore.WHITE
        elif tile == S:
            return Back.YELLOW + Style.DIM + Fore.WHITE
        elif tile == G:
            nutrient_level = self.nutrients_map[y][x]
            color_intensity = int(255 * nutrient_level / 1)
            return f'\x1b[48;2;{128-color_intensity//2};{255-color_intensity};{128-color_intensity//2}m'
        elif tile == '.':
            return Back.RED + Style.DIM + Fore.WHITE 
        elif tile == ':':
            return Back.RED + Style.DIM + Fore.WHITE
        elif tile == 't':
            return Back.RED + Style.NORMAL + Fore.WHITE
        elif tile == 'T' or tile == 'b' or tile == 'B' or tile == 'p' or tile == 'P':
            return Back.RED + Style.NORMAL + Fore.WHITE
        elif tile == CREATURE:
            return Back.MAGENTA 
        elif tile == WALL:
            return Back.BLACK + Style.DIM + Fore.WHITE
        elif tile == OUT_OF_BOUNDS:
            return Back.WHITE + Style.DIM + Fore.BLACK
        else:
            return Back.WHITE
    
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
            
    def get_tile_nutrients(self, x, y):
        return self.nutrients_map[y][x]

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
    
    def plant_trees(self, number_of_trees):
        for _ in range(number_of_trees):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            species = random.choice(TREE_SPECIES)
            success = self.plant_tree(x, y, species)
            if not success:
                _ -= 1
    
    def plant_bush(self, x, y, species):
        if 0 <= x < self.width and 0 <= y < self.height:
            new_bush = Bush(x, y, species)
            if self.is_tile_ground(x, y):
                self.set_tile(x, y, new_bush.symbol)
                self.plants.append(new_bush)
                return True
        
        return False
    
    def plant_bushes(self, number_of_bushes):
        for _ in range(number_of_bushes):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            species = random.choice(BUSH_SPECIES)
            success = self.plant_bush(x, y, species)
            if not success:
                _ -= 1
    
    def grow_all_plants(self):
        tile_updates = {}

        for plant in self.plants:
            nutrients = self.get_tile_nutrients(plant.x, plant.y)
            plant.grow(nutrients)
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
                            
# GAME LOOP
GAME_LOOP_TIME = .1

NUMBER_OF_TREES = 15
NUMBER_OF_BUSHES = 15

WORLD_WIDTH = 100
WORLD_HEIGHT = 25

def main():
    world = World(WORLD_HEIGHT, WORLD_WIDTH) 
    print(world)
    world.plant_trees(NUMBER_OF_TREES)
    world.plant_bushes(NUMBER_OF_BUSHES)
            
    while True:
        world.grow_all_plants()
        world.seed_new_trees()
        world.print_map()
        time.sleep(GAME_LOOP_TIME)
        
if __name__ == '__main__':
    cProfile.run('main()')