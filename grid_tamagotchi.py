from colorama import init as colorama_init
from colorama import Fore, Back, Style
from map import generate_map, W, S, G, WALL, OUT_OF_BOUNDS, GROUND, WATER, SAND
from tree import Tree
from bush import Bush
from creature import CREATURE, Creature
import pygame

import time
import cProfile
import random

colorama_init(autoreset=True)

OCEAN_BLUE = (21, 84, 192)
DESERT_YELLOW = (233, 216, 63)
FOREST_GREEN = (33, 192, 21)
CREATURE_RED = (249, 15, 15)
WALL_WHITE = (255, 255, 255)
OUT_OF_BOUNDS_BLACK = (0, 0, 0)

# PLANTS, TREES
TREE_SPECIES = [
    {
        "name": 'Teak',
        "growth_rate": 0.1,
        "max_age": 70,
        "color": [(178, 255, 102), (178, 255, 102), (178, 255, 102), (178, 255, 102)],
        "stages": [
            ".",
            ":",
            "t",
            "T",
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
        self.nutrients_map = None
        self.all_plants = []
        
        self.creature = Creature(random.randrange(self.width), random.randrange(self.height))
        
    def update_creature(self):
        self.creature.move(self)

    def print_map(self):
        pass
            
    def get_tile_color(self, tile, x, y):
        if tile.type == 'water':
            return OCEAN_BLUE
        elif tile.type == 'sand':
            return DESERT_YELLOW
        elif tile.type == 'ground':
            return FOREST_GREEN
        elif tile.type == 'creature':
            return CREATURE_RED
        elif tile.type == 'wall':
            return WALL_WHITE
        elif tile.type == 'out_of_bounds':
            return OUT_OF_BOUNDS_BLACK
    
    def get_map(self):
        return self.map
    
    def set_tile(self, x, y, tile):
        self.map[y][x] = tile
    
    def plant_at(self, x, y, plant):
        # Should always be a ground tile
        tile = self.get_tile(x, y)
        tile.plants.append(plant)
        self.all_plants.append(plant)
        
    def get_tile(self, x, y):
        return self.map[y][x]
    
    def move_tile(self, x, y, new_x, new_y):
        tile = self.get_tile(x, y)
        self.set_tile(x, y, S)
        self.set_tile(new_x, new_y, tile)

    def is_tile_water(self, x, y):
        return self.get_tile(x, y) == W

    def is_tile_edible(self, x, y):
        tile = self.get_tile(x, y)
        return tile != G and tile != W and tile != WALL and tile != OUT_OF_BOUNDS and tile != CREATURE
    
    def is_tile_sand(self, x, y):
        return self.get_tile(x, y).type == 'sand'
    
    def is_tile_ground(self, x, y):
        return self.get_tile(x, y).type == 'ground'
    
    def is_tile_occupied(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.is_tile_ground(x, y):
                return False
            else: 
                return True
            
    def can_move_to(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.is_tile_ground(x, y) or self.is_tile_sand(x, y):
                return True
            elif self.is_tile_edible(x, y):
                return True
            else:
                return False
            
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
        pass

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
    
    def within_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def plant_tree(self, x, y, species):
        if self.within_map(x, y):
            new_tree = Tree(x, y, species)
            if self.is_tile_ground(x, y):
                self.plant_at(x, y, new_tree)
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
    
    def grow_all_plants(self):
        tile_updates = {}

        for plant in self.all_plants:
            #nutrients = self.get_tile_nutrients(plant.x, plant.y)
            plant.grow(1)
            if plant.is_dead():
                tile_updates[(plant.x, plant.y)] = GROUND()

        self.all_plants = [plant for plant in self.all_plants if not plant.is_dead()]
            
    def seed_new_trees(self):
            SEEDING_INTERVAL = 5
            SEEDING_CHANCE = 0.1

            for plant in self.all_plants:
                if plant.growth_stage >= 10 and plant.seeding_counter >= SEEDING_INTERVAL:
                    plant.seeding_counter = 0
                    for adj_x, adj_y in self.get_adjacent_tiles(plant.x, plant.y):
                        if not self.is_tile_occupied(adj_x, adj_y) and random.random() < SEEDING_CHANCE:
                            self.plant_tree(adj_x, adj_y, plant.species)

    def draw_pygame_map(self, map_data, win, TILE_SIZE):
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                color = self.get_tile_color(tile, x, y)
                if tile.type == 'ground' and len(tile.plants) > 0:
                    color = tile.plants[0].color
                    pygame.draw.rect(win, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    circle_center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                    pygame.draw.circle(win, (249, 15, 15), circle_center, TILE_SIZE // 4)
                else:
                    pygame.draw.rect(win, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# GAME LOOP
GAME_LOOP_TIME = .1

NUMBER_OF_TREES = 15
NUMBER_OF_BUSHES = 15

WORLD_WIDTH = 100
WORLD_HEIGHT = 100

PYGAME_ENABLED = True
PYGAME_WIDTH = 800
PYGAME_HEIGHT = 800

def main():
    world = World(WORLD_HEIGHT, WORLD_WIDTH) 
    world.plant_trees(NUMBER_OF_TREES)
    #world.plant_bushes(NUMBER_OF_BUSHES)
    #world.seed_new_trees()
    #world.update_creature()
    if PYGAME_ENABLED:
        # Initialize Pygame
        pygame.init()
        win = pygame.display.set_mode((PYGAME_WIDTH, PYGAME_HEIGHT))
        pygame.display.set_caption("Map Display")
        TILE_SIZE = PYGAME_WIDTH // WORLD_WIDTH
    
        # Dont close the window immediately
        running = True
        while running:
            pygame.time.delay(100)
            world.grow_all_plants()
            world.draw_pygame_map(world.map, win, TILE_SIZE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
    else:
        world.print_map()
        
if __name__ == '__main__':
    main()
    cProfile.run('main()')