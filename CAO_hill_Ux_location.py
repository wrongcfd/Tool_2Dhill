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
#  ('X20_CAON60_H6_Z6_dt0.001_finalv2g_lu5.0_Time_400000.txt.txt'),
#  ('X25_CAON10_H10_Z6_dt0.005_finalv2g_lu5.0_smag0.01_Time_400000.txt'),
#    ('CPX25_CAON10_H10_Z6_dt0.005_finalv2g_lu5.0_tau1_geo2_Time_400000.txt'),
# ('CPX25_CAON10_H10_Z6_dt0.005_finalv2g_lu5.0_tau1_Time_400000.txt'),
# #    ('CPX25_CAON10_H10_Z6_dt0.005_finalv2g_lu5.0_tau2_geo5_Time_400000.txt'),


#    ('CPX25_CAON10_H10_Z6_dt0.005_finalv2g_lu5.0_tau2_geo10_Time_400000.txt'),

#    ('X30_CAON20_H6_Z6_dt0.002_finalv2f_Time_400000.txt'),
#    ('CPX25_CAON10_H10_Z6_dt0.005_finalv2g_lu5.0_tau2_geo20_Time_400000.txt'),

# ('X25_CAON40_H10_Z6_dt0.001_finalv2g_lu5.0_Time_400000.txt'),
# ('X20_CAON50_H10_Z6_dt0.001_finalv2g_lu5.0_Time_200000.txt'),
# ('X20_CAON60_H6_Z6_dt0.001_finalv2g_lu5.0_Time_200000.txt'),
# ('X20_CAON50_H10_Z6_dt0.001_finalv2g_lu5.0_sem0.1_Time_200000.txt'),
# ('X20_CAON60_H6_Z6_dt0.001_finalv2g_lu5.0_sem0.1_Time_200000.txt'),

]

plt.rc('font', size=14)   
fig = plt.gcf()
fig.subplots_adjust(left=0.1, right=0.9, top=0.6, bottom=0.1)
 ######### Plot SIN hill     ##################################################################
amplitude_xy = 1;frequency_xy = 0.25;length_xy = 2.5
XS = np.linspace(4.5, 9.5, 1000)
sine_hill_YS = amplitude_xy * np.cos(2 * np.pi * frequency_xy * ((XS - 7) / length_xy)) ** 2
plt.plot(XS-4.5, sine_hill_YS, color='black')
# Fill the area under the sine hill curve
plt.fill_between(XS - 4.5, sine_hill_YS, color='lightgrey',zorder=0)
######### Plot SIN hill     ##################################################################

# colors = ['steelblue', 'pink', 'olive', 'black', 'red']
colors = ['olive', 'black', 'violet', 'orange', 'black']
# colors = ['steelblue', 'violet', 'orange', 'violet', 'black']
line_styles = ['--', '--', '--', '--', '--']

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
    # Plot for each j value
    print(f"Dataset {i + 1}: N = {N}, cy = {cy}, dt = {dt}, lu = {lu}")
    du=N*dt
    for j in range(10):
        if lu==2.5:
            ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D-10) * N))] / du
        elif lu==7.5:
            ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D-5) * N))] / du
        elif lu==5.0:
            ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D-7.5) * N))] / du
        else :
            ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D) * N))] / du
        # if j in [0, 4]:
        #      y=np.arange(0, cy, 1/N)-1/N/2*3
        # else:
        #      y=np.arange(0, cy, 1/N) -1/N/2
        y=np.arange(0, cy, 1/N) -1/N/2            
        plt.plot(ux_ave + S * (j - 0) + D, y, linestyle=line_styles[i], linewidth=2.5, color=colors[i], zorder=1)
        # plt.scatter(ux_ave + S * (j - 0) + D, y, color=colors[i], zorder=1)

# ========================add cp region=====
# xg=np.linspace(-2.5,11, 1000)
# yg=1.0
# plt.plot(XS-4.5, sine_hill_YS, color='black')
# plt.fill_between(xg, yg, color='lavenderblush',zorder=0.5)
# plt.fill_between(XS - 4.5, sine_hill_YS+1.0, color='lavenderblush',zorder=0.5)
# ========================Read data from exp========================================
Edata2 = np.loadtxt('EXP2.txt', delimiter=',')
x2 = Edata2[:, 0]+2.5
y2 = Edata2[:, 1] 
plt.scatter(x2, y2, marker='o', c='none',edgecolors='r', s=180, label='Exp.')

# ========================Read data FOR ABL========================================
abldata = np.loadtxt('caouinlet.txt')
xabl = abldata[:, 0]
#yabl = abldata[:, 1] /40
# Plotting the experimental data with various offsets
offsets = np.arange(-1.25, 12.5-1.25, 1.25)
for offset in offsets:
    if offset== 2.5:
        yabl=abldata[:, 1] /40+1
    elif offset== 1.25 or offset== 3.75:
        yabl=abldata[:, 1] /40 +0.5
    else:
        yabl = abldata[:, 1] /40
    # plt.plot(xabl + offset, yabl, linestyle='--', color='blue',label=f'Exp. offset {offset}')
    # plt.scatter(xabl + offset, yabl, marker='o', c='none',edgecolors='blue',s=150)
# ==========================OPENFOAM========================================
h=0.04
x_shift = 1.25
ur=5.66
# Define the folder path
# folder_paths = ['MeshF5_2']
folder_paths = ['Mesh_corase1','Mesh_lowy']
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
        plt.plot(x_shifted, y, label=file_path,color='salmon', linewidth=2, linestyle=':',zorder=1) 
    elif i>=9 and i <18:
        x_shifted = x + (i-9) * x_shift  # Shift x-values for each dataset
        plt.plot(x_shifted, y, label=file_path,color='blue',linestyle=':', linewidth=2,zorder=1) 
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