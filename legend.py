import matplotlib.pyplot as plt
plt.rc('font', size=14) 
# Define the colors, line styles, and labels
# colors = ['steelblue', 'purple', 'olive', 'blue', 'black']
# line_styles = ['-', '-', '--', '--', ':']
# labels = ['log 6H', 'exp 6H', 'exp 10H', 'expfixedUx 10H','log 10H']

colors =  ['steelblue', 'pink', 'olive', 'black']
line_styles = ['-', '--','--',':']
labels = ['Y=6.25H','Y=8H','Y=13H','Y=15H']
# Create the plot for each data series with custom colors, line styles, and labels for the legend
for color, line_style, label in zip(colors, line_styles, labels):
    plt.plot([], [], color=color, linestyle=line_style, label=label)

# Add a legend
plt.legend()
# Show the plot
plt.show()
