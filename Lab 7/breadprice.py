import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('bread_prices.csv')

# Clean the data: drop rows with missing values and ensure correct types
df = df.dropna()
df['Year'] = df['Year'].astype(int)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df = df.dropna(subset=['Price'])

# Calculate average price per year
avg_price_per_year = df.groupby('Year')['Price'].mean()

# Plot the results
plt.figure(figsize=(8, 5))
plt.plot(avg_price_per_year.index, avg_price_per_year.values, marker='o')
plt.title('Average Bread Price Per Year')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.grid(True)
plt.tight_layout()
plt.show()