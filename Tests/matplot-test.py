import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
y2 = np.cos(x)
categories = ['A', 'B', 'C', 'D']
values = [4, 7, 1, 8]
hist_data = np.random.randn(1000)
pie_data = [15, 30, 45, 10]

# Create a figure with multiple subplots
fig, axs = plt.subplots(3, 2, figsize=(12, 12))

# Line Plot
axs[0, 0].plot(x, y, label='sin(x)', color='blue')
axs[0, 0].plot(x, y2, label='cos(x)', color='orange')
axs[0, 0].set_title('Line Plot')
axs[0, 0].legend()

# Scatter Plot
axs[0, 1].scatter(x, y, color='green', alpha=0.5)
axs[0, 1].set_title('Scatter Plot')

# Bar Chart
axs[1, 0].bar(categories, values, color='purple')
axs[1, 0].set_title('Bar Chart')

# Histogram
axs[1, 1].hist(hist_data, bins=30, color='cyan', alpha=0.7)
axs[1, 1].set_title('Histogram')

# Pie Chart
axs[2, 0].pie(pie_data, labels=['Category 1', 'Category 2', 'Category 3', 'Category 4'], autopct='%1.1f%%')
axs[2, 0].set_title('Pie Chart')

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
