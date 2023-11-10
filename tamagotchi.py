import os
import time
import random

W = '≈'
S = '.'
G = '-'
F = 'x'

LOCATION_OF_CREATURE = (4, 5)

small_map = [
    [W, W, W, W, S, S, G, G, G, W],
    [W, W, W, S, S, G, G, G, G, G],
    [W, W, S, S, G, G, G, G, G, G],
    [W, F, S, G, G, G, G, G, G, G],
    [S, S, G, G, G, G, G, G, G, G],
    [S, G, G, G, G, G, G, G, G, G],
    [F, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G]
]

map = [
    [W, W, W, W, W, W, W, W, S, W, W, W, W, S, S, W, W, W, W, W, W, W, S, S, G, G, S, W, W, W],
    [W, W, W, S, S, G, G, G, G, G, W, W, W, S, S, G, G, G, G, G, W, W, W, S, S, G, W, S, W, G],
    [W, W, S, S, G, G, G, G, G, G, W, W, S, S, G, G, G, G, G, G, W, W, S, S, G, G, G, S, S, G],
    [W, F, S, G, G, G, G, G, G, G, W, F, S, G, G, G, G, G, G, G, W, F, S, G, G, G, G, S, S, S],
    [S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, G],
    [S, G, G, G, G, G, G, G, G, G, S, G, G, G, G, G, G, G, G, G, S, G, G, G, G, G, G, G, G, G],
    [F, G, G, G, G, G, G, G, G, G, F, G, G, G, G, G, G, G, G, G, F, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, S, S, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, S, S, G, G, S, G, G, G],
    [G, G, G, S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, G, S, S, G, G, S, G, G],
    [G, G, S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, S, S, G],
    [G, F, S, G, G, G, G, G, G, G, G, F, S, G, G, G, G, G, G, G, G, F, S, G, G, G, G, S, S, S],
    [S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, G, S, S, G, G, G, G, G, G, G, G],
    [S, G, G, G, G, G, G, G, G, G, S, G, G, G, G, G, G, G, G, G, S, G, G, G, G, G, G, G, G, G],
    [F, G, G, G, G, G, G, G, G, G, F, G, G, G, G, G, G, G, G, G, F, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G],
    [G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G]
]

class Creature():
    def __init__(self, name, hunger, happiness, energy):
        self.name = name
        self.hunger = hunger
        self.happiness = happiness
        self.energy = energy
        self.symbol = '0'

    def feed(self):
        self.hunger += 1
        self.happiness += 1
        self.energy += 1

    def play(self):
        self.hunger += 1
        self.happiness += 1
        self.energy -= 1

    def sleep(self):
        self.hunger += 1
        self.happiness -= 1
        self.energy += 1
    
    def choose_action(self):
        choice = random.choice(['up', 'down', 'left', 'right'])
        self.move(map, choice)
    
    def choose_smart_action(self):
        pass
        
    def move(self, map, direction):
        global LOCATION_OF_CREATURE
        x, y = LOCATION_OF_CREATURE
        if direction == 'up':
            if y == 0:
                print("You can't go up!")
            else:
                map[y][x] = G
                y -= 1
                map[y][x] = self.symbol
        elif direction == 'down':
            if y == len(map) - 1:
                print("You can't go down!")
            else:
                map[y][x] = G
                y += 1
                map[y][x] = self.symbol
        elif direction == 'left':
            if x == 0:
                print("You can't go left!")
            else:
                map[y][x] = G
                x -= 1
                map[y][x] = self.symbol
        elif direction == 'right':
            if x == len(map[0]) - 1:
                print("You can't go right!")
            else:
                map[y][x] = G
                x += 1
                map[y][x] = self.symbol
        LOCATION_OF_CREATURE = (x, y)

    def show_stats(self):
        print(f"""{self.name}'s Stats:
Hunger: {self.hunger}
Happiness: {self.happiness}
Energy: {self.energy}""")


def print_map(map):
    for row in map:
        print(' '.join(row))

def main():
    creature = Creature('Arnold', 0, 0, 0)
    while True:
        time.sleep(0.5)
        os.system('clear')
        creature.show_stats()
        creature.choose_action()
        
        print_map(map)
        
if __name__ == '__main__':
    main()