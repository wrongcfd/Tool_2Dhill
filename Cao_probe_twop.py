import numpy as np
import matplotlib.pyplot as plt

# Load data from the file
data = np.loadtxt('probe.out')
# data2 = np.loadtxt('probe2.out')
# Extract data from data[20:, ]

# ds2 = data2[1:, :]
data_subset = data[1:, :]
a=0
uc=1
# Extract columns from the subset
time_steps = data_subset[:, 0]
# p1 = data_subset[:, 1+a] /uc
# p2 = data_subset[:, 5+a] /uc
# p3 = data_subset[:, 3+a] /uc
# p4 = data_subset[:, 7+a] /uc

p1 = data_subset[:, 1+a] /uc
p2 = data_subset[:, 5+a] /uc
p3 = data_subset[:, 3+a] /uc
p4 = data_subset[:, 7+a] /uc
# t2=ds2[:, 5+a] /uc
# Define the time step intervals
time_interval = 1000

# Calculate the corresponding x-axis values
x_values = np.arange(len(time_steps)) * time_interval

# Create subplots
fig, ((ax1, ax3), (ax5, ax6)) = plt.subplots(2, 2, figsize=(12, 16), sharex=True)

# Plot data in each subplot
ax1.plot(x_values, p1, label='uX_1', linestyle='-')

ax1.set_ylabel('Ux1')
ax1.legend()

ax3.plot(x_values, p2, label='Ux2', linestyle='-')

ax3.set_ylabel('Ux2')
ax3.legend()

# Plot original uX_Tave2
ax5.plot(x_values, p3, label='fX_1', linestyle='-')
ax5.set_xlabel('Time Steps')
ax5.set_ylabel('fx1')
ax5.legend()

# Plot original uX_Tave2
ax6.plot(x_values, p4, label='fX_2', linestyle='-')
ax6.set_xlabel('Time Steps')
ax6.set_ylabel('fx2')
ax6.legend()

# Set common title
plt.suptitle('Probe Data and Residuals over Time Steps (Each Point Represents 1000 Time Steps)')
plt.get_current_fig_manager().window.state('zoomed')
plt.show()
