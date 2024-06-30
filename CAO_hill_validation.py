import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
def read_N_and_H_from_filename(filename):
    X_l = None
    N = None
    cy= None
    dt = None
    for part in filename.split('_'):
        for i, char in enumerate(part):
            if char == 'X' and part[i+1:].isdigit():
                X_l = int(part[i+1:])
            if char == 'N' and part[i+1:].isdigit():
                N = int(part[i+1:])
            if char == 'H' and part[i+1:].isdigit():
                cy = int(part[i+1:])
            if char == 't' and i < len(part) - 1 and part[i+1:].replace('.', '').isdigit():
                dt = float(part[i+1:])
    return X_l, N, cy,dt

dataset_files = [   
       
('X30_CAON5_H6_Z6_dt0.01_Time_400000.txt', 'LBM N5'),
# ('X30_CAON5_H6_Z6_dt0.01_CPtau1e_Time_400000.txt', 'LBM N5'),
('X30_CAON5_H6_Z6_dt0.01_CPtau0.5c_Time_400000.txt', 'LBM N5'),
('X30_CAON5_H6_Z6_dt0.01_CPtau0.5ctest_Time_400000.txt', 'LBM N5'),
('X30_CAON5_H6_Z6_dt0.01_CPtau0.5ctestb_Time_400000.txt', 'LBM N5'),

# ('X30_CAON5_H6_Z6_dt0.01_CPtau0.3e_Time_400000.txt', 'LBM N5'),



    #   ('X30_CAON3_H6_Z6_dt0.02_Time_400000.txt', 'LBM N3'),
    #    ('X30_CAON3_H6_Z6_dt0.02_CPtau5b_Time_400000.txt', 'LBM N3'),
    #  ('X30_CAON3_H6_Z6_dt0.02_CPtau0.5e_Time_1600000.txt', 'LBM N3'),
    #    ('X30_CAON3_H6_Z6_dt0.02_CPtau1e_Time_400000.txt', 'LBM N3'),
    #     ('X30_CAON3_H6_Z6_dt0.02_CPtau1_Time_400000.txt', 'LBM N3'),
    #   ('X30_CAON5_H6_Z6_dt0.01_Time_400000.txt', 'LBM N5'),
   #    ('X30_CAON3_H6_Z6_dt0.02_CPtau2_Time_400000.txt', 'LBM N=3 cp'),
        # ('X30_CAON3_H6_Z6_dt0.02_CPtau5_Time_400000.txt', 'LBM N=3 cp'),
        #   ('X30_CAON5_H6_Z6_dt0.01_Time_200000.txt', 'LBM N5 1'),
    #    ('X30_CAON5_H6_Z6_dt0.01_Time_200000.txt', 'LBM N=5'),
    #       ('X30_CAON10_H6_Z6_dt0.005_Time_200000.txt', 'LBM N=10'), 
        #    ('X30_CAON20_H6_Z6_dt0.002_Time_200000.txt', 'LBM N=20'),    
        #   ('X30_CPCAON10_H6_Z6_dt0.005_tau40_1h_Time_200000.txt', 'cp N10'),                           
  
]

plt.rc('font', size=14)   
fig = plt.gcf()
# Adjust the position of the subplot
fig.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.3)
 ######### Plot SIN hill     ##################################################################
amplitude_xy = 1;frequency_xy = 0.25;length_xy = 2.5
XS = np.linspace(4.5, 9.5, 1000)
sine_hill_YS = amplitude_xy * np.cos(2 * np.pi * frequency_xy * ((XS - 7) / length_xy)) ** 2

######### Plot SIN hill     ##################################################################
# Process and plot each dataset
for i, (dataset_file, label) in enumerate(dataset_files):
    X_l, N, cy, dt = read_N_and_H_from_filename(dataset_file)    
    data = np.loadtxt(dataset_file, skiprows=1)
    new_shape = (1+cy*N, 9, X_l*N)
    # new_shape = (1+cy*N, 9, X_l*N)
    data = data.reshape(new_shape)
    # y = np.arange(0, cy, 1/N) -1/N/2
    D = 0
    S =1.25
    # Plot for each j value
    print(f"Dataset {i + 1}: N = {N}, cy = {cy}, dt = {dt}")
    du=N*dt
    for j in range(9):
        ux_ave = data[0:(N*cy), 3, (int((j * S+7.5+5+D) * N))] / du
        # if j in [0, 4]:
        #      y=np.arange(0, cy, 1/N)-1/N/2*3
        # else:
        #      y=np.arange(0, cy, 1/N) -1/N/2
        y=np.arange(0, cy, 1/N) -1/N/2            
        if i == 0:
            plt.plot(ux_ave + S * (j - 0) + D, y, linestyle='-', linewidth=2.5, color='steelblue',zorder=1)
            plt.scatter(ux_ave + S * (j - 0) + D, y, marker='o', color='steelblue',  s=50)
        elif i == 1:
        #    plt.plot(ux_ave + S * (j - 0) - D, y, linestyle='--', linewidth=2, color='gold')
           plt.plot(ux_ave + S * (j - 0) + D, y, linestyle='-', linewidth=2.5, color='purple',zorder=1)
        #    plt.scatter(ux_ave + S * (j - 0) + D, y, marker='o', color='purple',  s=50)
        #    plt.scatter(ux_ave + S * (j - 0) + D, y, marker='o', color='purple',  s=50)
        elif i == 2:
            plt.plot(ux_ave + S * (j - 0) + D, y, linestyle='-.', linewidth=2.5, color='olive',zorder=1)
        elif i == 3:
            plt.plot(ux_ave + S * (j - 0) + D, y, linestyle='--', linewidth=2, color='blue')
plt.plot(XS-4.5, sine_hill_YS, color='black')
# Fill the area under the sine hill curve
plt.fill_between(XS - 4.5, sine_hill_YS, color='lightgrey',zorder=0)

# plt.plot(XS-4.5, sine_hill_YS, color='black')
# plt.fill_between(XS - 4.5, sine_hill_YS+0.3, color='lavenderblush',zorder=1)
# ========================Read data from exp========================================
Edata2 = np.loadtxt('EXP2.txt', delimiter=',')
x2 = Edata2[:, 0]+2.5
y2 = Edata2[:, 1] 
plt.scatter(x2, y2, marker='o', c='none',edgecolors='r', s=50, label='Exp.')
# ==========================OPENFOAM========================================
h=0.04
x_shift = 1.25
ur=5.66
# Define the folder path
# folder_paths = ['MeshF5_2']
folder_paths = ['MeshF2']
# Define a function to read data from a file
def read_data(file_path):
    data = np.loadtxt(file_path)  
    return data[:, 1] /ur,  data[:, 0]/h 

# Define file paths for each dataset
file_names = ['x_-2.5_U.xy', 'x_-1.25_U.xy', 'x_0_U.xy', 'x_1.25_U.xy', 'x_2.5_U.xy', 'x_3.75_U.xy', 'x_5_U.xy','x_6.25_U.xy','x_7.5_U.xy']
all_file_paths = []
for folder_path in folder_paths:
    all_file_paths.extend([os.path.join(folder_path, file_name) for file_name in file_names])

# Iterate over each file, read the data, and plot it
for i, file_path in enumerate(all_file_paths):
    x, y = read_data(file_path)
    
    if i <9:
        x_shifted = x + i * x_shift
        plt.plot(x_shifted, y, label=file_path,color='salmon', linewidth=2, linestyle='--',zorder=1) 
    elif i>=9 and i <18:
        x_shifted = x + (i-9) * x_shift  # Shift x-values for each dataset
        plt.plot(x_shifted, y, label=file_path,color='blue',linestyle='--', linewidth=2,zorder=1) 
    elif i>=18 and i<27:
        x_shifted = x + (i-18) * x_shift  # Shift x-values for each dataset
        plt.plot(x_shifted, y, label=file_path,color='gold',linestyle='-.', linewidth=2,zorder=1) 
    elif i>=27:
        x_shifted = x + (i-27) * x_shift  # Shift x-values for each dataset
        plt.plot(x_shifted, y, label=file_path,color='olive',linestyle=':', linewidth=2,zorder=1)     
#=======================================================

plt.xticks(np.arange(0, 12.5, 1.25))
# plt.xlim(-10, 12)
plt.ylim(0,2)
plt.xlabel('x/H+u/$U_{ref}$')  #$U_{\infty}$
plt.ylabel('y/H')
# Get only the handles and labels for solid and dashed lines
plt.savefig('LBM_hill.png', bbox_inches='tight')
plt.get_current_fig_manager().window.state('zoomed')
plt.show()
plt.close()