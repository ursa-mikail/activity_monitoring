import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Sample Data: Generate N random scores between -50 and 100
#N = 100  # Set the number of days
#scores = np.random.randint(-50, 101, N)

# 1. Intensity Histogram: Create a histogram of the scores (frequency of scores)
intensity_histogram = Counter(scores)
intensity_values = list(intensity_histogram.values())  # Frequencies of each score
intensity_labels = list(intensity_histogram.keys())    # The scores themselves

# 2. Frequency Histogram: Get the histogram of how many scores appear with certain frequencies
frequency_histogram = Counter(intensity_values)  # Frequency of frequency counts
frequency_values = list(frequency_histogram.keys())  # Different frequency values
frequency_counts = list(frequency_histogram.values())  # How many times each frequency occurs

# Plot the Intensity Histogram
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(intensity_labels, intensity_values, color='blue', edgecolor='black')
plt.title('Intensity Histogram')
plt.xlabel('Scores')
plt.ylabel('Frequency')
plt.xticks(rotation=45)

# Plot the Frequency Histogram
plt.subplot(1, 2, 2)
plt.bar(frequency_values, frequency_counts, color='green', edgecolor='black')
plt.title('Frequency Histogram')
plt.xlabel('Frequency of Scores')
plt.ylabel('Count of Scores with that Frequency')

# Display the plots
plt.tight_layout()
plt.show()

