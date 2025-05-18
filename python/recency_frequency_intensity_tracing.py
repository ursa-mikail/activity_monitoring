import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Step 1: Generate N random scores between -50 and 100
N = 100  # Set the number of days
scores = np.random.randint(-50, 101, N)

Kismet = [ 50, 50, 50, 0, 0, 0, 0, 0, 50, 75, 75, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 0, 0, 10, 0, 0, -50, -50, -50, 0, 0, 0, 75, 10, 0, 10, 0, 25, 0, 10, 10, 0, 0, 10, 0, 25, 10, 0, 10, 0, 10, 25, 0, 50, 10, 0, 0, 20, 0, 0, 0, 0, -50, 0, 10, 0, 10, 35, 0, 0]
Psyche = [ 50, 50, 10, 0, 50, 0, 0, 50, 0, 50, 0, 0, 0, 50, 50, 0, 0, 50, 0, 100, 0, 0, 0, 50, 50, 50, 50, 50, 50, 0, 50, 0, 0, 0, 100, 0, 0, 0, 0, 50, 0, 50, 0, 0, 50, 50, 50, 10, 0, 0, 100, 0, 50, 0, 0, 0, 0, 0, 10, 0, 100, 10, 0, 0, 0, 10, 0, 0, 0, -50, 0, 50, 0, 0, 10, 0]
Soma = [50, 100, 50, 0, 0, 0, 100, 100, 100, 100, 100, 0, 0, 100, -50, 0, 0, 100, 0, 50, 100, 100, 0, 0, 100, 0, 0, -50, -50, -50, 50, 100, -50, -50, -50, -50, -50, 200, 100, 0, 0, 0, 0, -50, 175, -50, 0, -50, 150, 0, -50, -50, -50, -50, -50, 150, 0, 110, -50, 0, 60, -50, 50, 50, 50, 50, 0, 100, 0, 0, -50, 0, 0, 0, 50, -25, 10]
Pneuma = [ 50, 50, 50, 0, 0, 0, 100, 0, 0, 50, 50, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 100, 50, 50, 0, 0, 50, 0, 0, 0, -50, -50, 0, 0, 0, 150, 0, 0, 0, 0, 50, 0, 0, 10, 0, 0, 0, -50, 0, 0, 0, 25, 0, 0, 10, 50, 10, 10, 10, 0, 0, 10, 0, 10, 10, -50, 0, 10, 0, 0, 35, 0, 0]
Opus = [ 50, 50, 50, 150, 50, 0, 100, 100, 0, 150, 50, 0, 0, 0, 100, 75, 50, 50, 0, 75,  100, 50, 50, 50, 100, 100, 100, 75, 50, 50, 100, 0, 100, -50, 0, 0, 0, 0, 50, 250, 50, 0, 0, -50, 10, 10, 100, 50, 10, 0, 0, 50, 50, 100, 10, 60, 10, 60, 100, 50, 20, 110, 30, 0, 10, 0, 0, 50, 0, 50, 0, 0, 0, 0, 50, 0, 0]

score_list = [Kismet, Psyche, Soma, Pneuma, Opus]
scores = score_list[0]

N = len(scores)

# Step 2: Recency - Get the N most recent scores (last N entries)
# recent_scores = scores[-N:]

# Step 3: Intensity - Create histogram of scores and get highest count (frequency) for highest and lowest scores
#intensity_histogram = Counter(recent_scores)
intensity_histogram = Counter(scores)

# Get the highest and lowest frequency counts
highest_score_count = max(intensity_histogram.values())
lowest_score_count = min(intensity_histogram.values())

# Find the scores with the highest and lowest frequency counts
intensity_max_high = [score for score, count in intensity_histogram.items() if count == highest_score_count]
intensity_max_low = [score for score, count in intensity_histogram.items() if count == lowest_score_count]

# Print the results
print(f"intensity_histogram: {intensity_histogram}")
print(f"intensity_histogram: {intensity_histogram.keys()}")
print(f"intensity_histogram: {intensity_histogram.values()}")

print(f"highest_score_count: {highest_score_count}")
print(f"lowest_score_count: {lowest_score_count}")
print(f"Score(s) with highest frequency: {intensity_max_high}")
print(f"Score(s) with lowest frequency: {intensity_max_low}")
# in case of more than 1 value
"""
intensity_bounds = []
intensity_bounds.append(max(intensity_max_high))
intensity_bounds.append(min(intensity_max_high))
intensity_bounds.append(max(intensity_max_low))
intensity_bounds.append(min(intensity_max_low))
intensity_max_high = max(intensity_bounds)
intensity_max_low = min(intensity_bounds)
"""
intensity_max_high = max(intensity_max_high)
intensity_max_low = min(intensity_max_low)
print(f"intensity_max_high: {intensity_max_high}")
print(f"intensity_max_low: {intensity_max_low}")

if (intensity_max_high < intensity_max_low):  # swap
  intensity_max_high, intensity_max_low = intensity_max_low, intensity_max_high

# Step 4: Plotting time series with the min-max line for intensity and frequency
plt.figure(figsize=(12, 6))

# Plot time series
plt.plot(range(N), scores, label='Scores over Time', color='blue')

# Draw red lines for min-max of intensity and frequency
plt.axhline(y=intensity_max_high, color='green', linestyle='--', label=f'Intensity Max for Highest Score: {intensity_max_high}')
plt.axhline(y=intensity_max_low, color='green', linestyle='--', label=f'Intensity Min for Lowest Score: {intensity_max_low}')

# Draw lines for overall min and max of the scores
score_min = min(scores)
score_max = max(scores)

print(f"score_max: {score_max}")
print(f"score_min: {score_min}")
plt.axhline(y=score_max, color='purple', linestyle='-', label=f'Overall Max: {score_max}')
plt.axhline(y=score_min, color='purple', linestyle='-', label=f'Overall Min: {score_min}')

# Show the plot with labels
plt.xlabel('Days')
plt.ylabel('Scores')
plt.title('Scores Over Time with Intensity and Frequency Min-Max')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

""" chosen: Kismet
intensity_histogram: Counter({0: 44, 10: 12, 50: 9, -50: 4, 75: 3, 25: 3, 20: 1, 35: 1})
intensity_histogram: dict_keys([50, 0, 75, 10, -50, 25, 20, 35])
intensity_histogram: dict_values([9, 44, 3, 12, 4, 3, 1, 1])
highest_score_count: 44
lowest_score_count: 1
Score(s) with highest frequency: [0]
Score(s) with lowest frequency: [20, 35]
intensity_max_high: 0
intensity_max_low: 20
score_max: 75
score_min: -50
"""