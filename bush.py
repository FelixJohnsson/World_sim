class Bush(object):
    def __init__(self, x, y, species):
        self.MAX_AGE = species['max_age']
        self.GROWTH_RATE = species['growth_rate']
        
        self.x = x
        self.y = y
        self.species = species
        self.growth_stage = 0
        self.symbol = species['stages'][0]
        self.seeding_counter = 0
        
    def grow(self, nutrients_level):
        self.growth_stage += self.GROWTH_RATE * nutrients_level
        if self.growth_stage >= 10 and self.growth_stage < 20:
            self.symbol = self.species['stages'][1]
        elif self.growth_stage >= 20 and self.growth_stage < 30:
            self.symbol = self.species['stages'][2]
        elif self.growth_stage >= 30:
            self.symbol = self.species['stages'][3]
                
        self.seeding_counter += 1
            
    def is_dead(self):
        return self.growth_stage > self.MAX_AGE