import random
from map import G

# CREATURES
CREATURE = '0'

class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = CREATURE

    def move(self, world):
        # Randomly move the creature in any direction
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        dx, dy = random.choice(directions)
        new_x, new_y = self.x + dx, self.y + dy

        # Check for world boundaries
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            if world.can_move_to(new_x, new_y):
                world.set_tile(self.x, self.y, G)  # Leave the current spot
                world.set_tile(new_x, new_y, self.symbol)  # Move to new spot
                if world.is_tile_edible(new_x, new_y):
                    self.eat(world)
                self.x, self.y = new_x, new_y  # Update creature's position

    def eat(self, world):
        # NOT IMPLEMENTED
        pass