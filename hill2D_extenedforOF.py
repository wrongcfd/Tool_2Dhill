import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to add points based on resolution
def add_points(df, res, n):
    new_points = []
    for index, row in df.iterrows():
        x = row['x']
        y = row['y']
        z = row['z']
        for i in range(1, n+1):
            new_y = y + i * res
            new_points.append({'x': x, 'y': new_y, 'z': z})
    return pd.concat([df, pd.DataFrame(new_points)], ignore_index=True)

# Read data from file into a DataFrame
df = pd.read_csv('hill_2d.pc', sep='\s+', header=None, names=['x', 'y', 'z'])
df['x'] += 27.5
# Find maximum 'y' values for each 'x'
max_y_values = df.groupby('x')['y'].transform('max')

# Filter the DataFrame to keep rows with maximum 'y' values for each 'x'
max_y_data = df[df['y'] == max_y_values]
# Multiply filtered data (x, y, z) by 0.04
max_y_data[['x', 'y', 'z']] *= 0.04
max_y_data[['z']] += 0.04*0.1
# Define resolution and number of points to add
res = 0.2*0.04
n = 5  # Number of points to add in y direction

# Add more points based on resolution and increase y coordinates
extended_data = add_points(max_y_data, res, n)

# Plotting
plt.figure(figsize=(10, 6))

# Original Data
plt.scatter(df['x']*0.04, df['y']*0.04, color='blue', label='Original Data', alpha=0.5)

# Filtered Data
plt.scatter(max_y_data['x'], max_y_data['y'], color='red', label='Filtered Data', marker='x')

# Extended Data
plt.scatter(extended_data['x'], extended_data['y'], color='green', label='Extended Data', marker='o', alpha=0.5)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Original Data, Filtered Data, and Extended Data')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()

# Save the extended data to a new file (e.g., curve_extended.pc)
extended_data.to_csv('curve_extended.pc', sep=' ', header=False, index=False, columns=['x', 'y', 'z'])
