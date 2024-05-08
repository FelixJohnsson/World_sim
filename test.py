import matplotlib.pyplot as plt
import numpy as np

# Consolidated data
data = {
    'April 30th': {
        'Grauby': {'Roulette 1': 100},
        'Felix': {'Roulette 1': 100}
    },
    'May 1st': {
        'Grauby': {'Roulette 2': -200},
        'Felix': {'Roulette 2': -100}
    },
    'May 2nd': {
        'Grauby': {'Roulette 3': 363},
        'Felix': {'Roulette 3': 164}
    },
    'May 3rd': {
        'Grauby': {
            'Roulette 4': -100,
            'Roulette 5': -100,
            'Roulette 6': -200,
            'Roulette 7': -100,
            'Blackjack 8': 450,
            'Spin 9': 0
        },
        'Felix': {
            'Roulette 4': -100,
            'Roulette 5': -100,
            'Roulette 6': -200,
            'Roulette 7': -100,
            'Blackjack 8': 450,
            'Spin 9': 0
        }
    },
    'May 7th': {
        'Grauby': {
            'Blackjack 10': -100,
            'Blackjack 11': -150,
            'Blackjack 12': -50,
            'Blackjack 13': -100
        },
        'Felix': {
            'Blackjack 10': 0,
            'Blackjack 11': -150,
            'Blackjack 12': -50,
            'Blackjack 13': 0
        }
    }
}

# Initialize lists for plotting
felix_values = []
grauby_values = []
labels = []

# Extract data into the lists
for day, players in data.items():
    for player, games in players.items():
        for game, result in games.items():
            if player == 'Felix':
                felix_values.append(result)
                if game not in labels:
                    labels.append(game)
            elif player == 'Grauby':
                grauby_values.append(result)

# Calculate cumulative sums and statistical metrics
felix_cumsum = np.cumsum(felix_values)
grauby_cumsum = np.cumsum(grauby_values)
felix_mean = np.mean(felix_values)
grauby_mean = np.mean(grauby_values)
felix_volatility = np.std(felix_values)
grauby_volatility = np.std(grauby_values)

x = np.arange(len(labels))  # Label locations

fig, ax = plt.subplots(figsize=(12, 6))

# Create bars for each set of results
rects1 = ax.bar(x - 0.2, felix_values, width=0.4, label='Felix', color=['green' if v > 0 else 'red' for v in felix_values])
rects2 = ax.bar(x + 0.2, grauby_values, width=0.4, label='Grauby', color=['green' if v > 0 else 'red' for v in grauby_values])

# Add a line graph for cumulative totals
ax2 = ax.twinx()
ax2.plot(x - 0.2, felix_cumsum, label='Felix Total', marker='o', color='blue', linewidth=2, markersize=8)
ax2.plot(x + 0.2, grauby_cumsum, label='Grauby Total', marker='o', color='purple', linewidth=2, markersize=8)

# Set labels and titles
ax.set_xlabel('Games')
ax.set_ylabel('Net Gain/Loss')
ax2.set_ylabel('Total Balance')
ax.set_title('Gambling Results and Cumulative Totals by Game Type')
ax.set_xticks(x)
ax.set_xticklabels(labels)

# Adding dividers between different game types
previous_game_type = ""
for i, label in enumerate(labels):
    game_type = label.split()[0]
    if previous_game_type and game_type != previous_game_type:
        ax.axvline(x=i - 0.5, color='grey', linestyle='--', linewidth=1)
    previous_game_type = game_type

# Function to attach a text label above each bar
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

# Displaying statistical information
ax.annotate(f'Avg: {felix_mean:.2f}, Vol: {felix_volatility:.2f}', xy=(0, 1), xycoords='axes fraction', xytext=(5, -5), textcoords='offset points', ha='left', va='top', color='blue', fontsize=10)
ax.annotate(f'Avg: {grauby_mean:.2f}, Vol: {grauby_volatility:.2f}', xy=(1, 1), xycoords='axes fraction', xytext=(-5, -5), textcoords='offset points', ha='right', va='top', color='purple', fontsize=10)

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
fig.tight_layout()
plt.show()
