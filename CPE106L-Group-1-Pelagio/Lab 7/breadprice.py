import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('breadprice.csv')

# Calculate the average price for each year (across all months)
# Exclude the 'Year' column when calculating the mean
df['AveragePrice'] = df.loc[:, 'Jan':'Dec'].mean(axis=1, skipna=True)

# Drop years where average price could not be calculated (all months missing)
df = df.dropna(subset=['AveragePrice'])

# Plot the results
plt.figure(figsize=(8, 5))
plt.plot(df['Year'], df['AveragePrice'], marker='o')
plt.title('Average Bread Price Per Year')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.grid(True)
plt.tight_layout()
plt.show()