import numpy as np

class GridGame:
    def __init__(self, size=4):
        self.size = size
        self.reset()
        
    def reset(self):
        self.grid = np.zeros((self.size, self.size))
        self.player_position = (0, 0)
        self.grid[self.player_position] = 1
        self.goal_position = (self.size - 1, self.size - 1)
        self.grid[self.goal_position] = 9
        self.game_over = False
        return self.grid.flatten()
    
    def move_player(self, action):
        x, y = self.player_position
        if action == 0:  # up
            x = max(0, x - 1)
        elif action == 1:  # right
            y = min(self.size - 1, y + 1)
        elif action == 2:  # down
            x = min(self.size - 1, x + 1)
        elif action == 3:  # left
            y = max(0, y - 1)
        
        self.grid[self.player_position] = 0 
        self.player_position = (x, y)
        self.grid[self.player_position] = 1
        
        reward = 0
        if self.player_position == self.goal_position:
            self.game_over = True
            reward = 1
        
        return self.grid.flatten(), reward, self.game_over
    
    def render(self):
        print(self.grid)


class RandomAgent:
    def __init__(self, action_size):
        self.action_size = action_size
    
    def choose_action(self, state):
        return np.random.choice(self.action_size)


class QLearningModel:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.9):
        self.q_table = np.zeros((state_size, action_size))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
    
    def choose_action(self, state, epsilon):
        if np.random.random() < epsilon:
            return np.random.choice(len(self.q_table[state]))
        else:
            return np.argmax(self.q_table[state])
    
    def update_q_table(self, state, action, reward, next_state, done):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action] * (not done)
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error


epsilon = 0.1
num_episodes = 1000

env = GridGame(size=4)
state_size = env.size ** 2
action_size = 4
model = QLearningModel(state_size, action_size)

# Training the model
for episode in range(num_episodes):
    state = env.reset()
    state_index = np.argmax(state)
    total_reward = 0
    
    while True:
        action = model.choose_action(state_index, epsilon)
        next_state, reward, done = env.move_player(action)
        next_state_index = np.argmax(next_state)
        
        model.update_q_table(state_index, action, reward, next_state_index, done)
        
        state_index = next_state_index
        total_reward += reward
        
        if done:
            break

print("Trained Q-table:")
print(model.q_table)