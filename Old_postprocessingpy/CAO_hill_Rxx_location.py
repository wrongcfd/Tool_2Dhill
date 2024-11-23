import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
def read_N_and_H_from_filename(filename):
    lu= None
    X_l = None
    N = None
    cy= None
    dt = None
    for part in filename.split('_'):
        for i, char in enumerate(part):
            if 'lu' in part and part.split('lu')[-1].replace('.', '', 1).isdigit():
                lu = float(part.split('lu')[-1])
            if char == 'X' and part[i+1:].isdigit():
                X_l = int(part[i+1:])
            if char == 'N' and part[i+1:].isdigit():
                N = int(part[i+1:])
            # if char == 'H' and part[i+1:].isdigit():
            if char == 'H' and i < len(part) - 1 and part[i+1:].replace('.', '').isdigit():
                cy = float(part[i+1:])
            if char == 't' and i < len(part) - 1 and part[i+1:].replace('.', '').isdigit():
                dt = float(part[i+1:])
    return lu, X_l, N, cy,dt


dataset_files = [   

] 

plt.rc('font', size=14)   
fig = plt.gcf()
fig.subplots_adjust(left=0.1, right=0.9, top=0.6, bottom=0.1)
######### Plotexp   ########
Ruic = np.loadtxt('sigmaU.txt', delimiter=',')
xru= Ruic[:, 0]+2.5; yru= Ruic[:, 1]
plt.scatter(xru, yru, marker='o', c='none', edgecolors='r', s=50, label='exp_u')

 ######### Plot SIN hill     ##################################################################
amplitude_xy = 1;frequency_xy = 0.25;length_xy = 2.5
XS = np.linspace(4.5, 9.5, 1000)
sine_hill_YS = amplitude_xy * np.cos(2 * np.pi * frequency_xy * ((XS - 7) / length_xy)) ** 2
plt.plot(XS-4.5, sine_hill_YS, color='black')
# Fill the area under the sine hill curve
plt.fill_between(XS - 4.5, sine_hill_YS, color='lightgrey',zorder=0)
######### Plot SIN hill     ##################################################################
colors = ['steelblue', 'pink', 'olive', 'black', 'red']
# colors = ['olive', 'blue', 'violet', 'orange', 'black']
# colors = ['steelblue', 'violet', 'orange', 'violet', 'black']
line_styles = ['-', '--', '--', ':', '--']

for i, (dataset_file) in enumerate(dataset_files):
    lu, X_l, N, cy, dt = read_N_and_H_from_filename(dataset_file) 
    ny=int(cy*N)   
    data = np.loadtxt(dataset_file, skiprows=1)
    new_shape = (ny+1, 9, X_l*N)
    # new_shape = (1+cy*N, 9, X_l*N)
    data = data.reshape(new_shape)
    # y = np.arange(0, cy, 1/N) -1/N/2
    D = -1.25 
    S =1.25
    a=0
    ux_ave = data[:,3+a,:]
    uux_ave = data[:,6+a,:]
    Ru=np.sqrt((uux_ave-ux_ave**2))
    # Plot for each j value
    print(f"Dataset {i + 1}: N = {N}, cy = {cy}, dt = {dt}")
    du=N*dt
    for j in range(10):
        if lu==2.5:
            ux_ave = Ru[0: (ny),(int((j * S+7.5+5+D-10) * N))] /du /0.2
        elif lu==7.5:
            ux_ave = Ru[0: (ny),(int((j * S+7.5+5+D-5.0) * N))] / du/0.2
        elif lu==5.0:
            ux_ave = Ru[0: (ny),(int((j * S+7.5+5+D-7.5) * N))] / du/0.2
        else :
            # ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D) * N))] / du
            #RUU
            ux_ave = Ru[0: (ny),(int((j * S+7.5+5+D) * N))] /du /0.2
        # if j in [0, 4]:
        #      y=np.arange(0, cy, 1/N)-1/N/2*3
        # else:
        #      y=np.arange(0, cy, 1/N) -1/N/2
        y=np.arange(0, cy, 1/N) -1/N/2            
        plt.plot(ux_ave + S * (j - 0) + D, y, linestyle=line_styles[i], linewidth=2.5, color=colors[i], zorder=1)

# ========================add cp region=====
# xg=np.linspace(-2.5,11, 1000)
# yg=1.0
# plt.plot(XS-4.5, sine_hill_YS, color='black')
# plt.fill_between(xg, yg, color='lavenderblush',zorder=0.5)
# plt.fill_between(XS - 4.5, sine_hill_YS+1.0, color='lavenderblush',zorder=0.5)
# ========================Read data from exp========================================
# Edata2 = np.loadtxt('EXP2.txt', delimiter=',')
# x2 = Edata2[:, 0]+2.5
# y2 = Edata2[:, 1] 
# plt.scatter(x2, y2, marker='o', c='none',edgecolors='r', s=180, label='Exp.')

# ========================Read data FOR ABL========================================
# abldata = np.loadtxt('caouinlet.txt')
# xabl = abldata[:, 0]
# #yabl = abldata[:, 1] /40
# # Plotting the experimental data with various offsets
# offsets = np.arange(-1.25, 12.5, 1.25)
# for offset in offsets:
#     if offset== 2.5:
#         yabl=abldata[:, 1] /40+1
#     elif offset== 1.25 or offset== 3.75:
#         yabl=abldata[:, 1] /40 +0.5
#     else:
#         yabl = abldata[:, 1] /40
#     plt.plot(xabl + offset, yabl, linestyle='--', color='blue',label=f'Exp. offset {offset}')

# ==========================OPENFOAM========================================
h=0.04
x_shift = 1.25
ur=5.66
# Define the folder path
# folder_paths = ['MeshF5_2']
folder_paths = ['Mesh_corase1','MeshF2']
# Define a function to read data from a file
def read_data(file_path):
    data = np.loadtxt(file_path)  
    return np.sqrt(2/3*data[:, 1] /ur/0.2),  data[:, 0]/h 

# Define file paths for each dataset
file_names = ['x_-2.5_k_nut_epsilon.xy', 'x_-1.25_k_nut_epsilon.xy', 'x_0_k_nut_epsilon.xy', 'x_1.25_k_nut_epsilon.xy', 'x_2.5_k_nut_epsilon.xy', 'x_3.75_k_nut_epsilon.xy', 'x_5_k_nut_epsilon.xy','x_6.25_k_nut_epsilon.xy','x_7.5_k_nut_epsilon.xy']
all_file_paths = []
for folder_path in folder_paths:
    all_file_paths.extend([os.path.join(folder_path, file_name) for file_name in file_names])

# Iterate over each file, read the data, and plot it
for i, file_path in enumerate(all_file_paths):
    x, y = read_data(file_path)
    if i <9:
        x_shifted = x + i * x_shift
        plt.plot(x_shifted, y, label=file_path,color='salmon', linewidth=2, linestyle=':',zorder=1) 
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

plt.xticks(np.arange(-2.5, 12.5, 1.25))
# plt.xlim(-1.25, 12)
plt.ylim(0,5)
plt.xlabel('x/H+u/$U_{ref}$')  #$U_{\infty}$
plt.ylabel('y/H')
# Get only the handles and labels for solid and dashed lines
plt.savefig('LBM_hill.png', bbox_inches='tight')
plt.get_current_fig_manager().window.state('zoomed')
plt.show()
plt.close()