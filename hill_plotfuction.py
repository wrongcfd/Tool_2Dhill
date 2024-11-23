import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os

def hillplot_Ux(dataset_files, line_styles, colors, llabel=None):
    solidhill()
    for i, (dataset_file) in enumerate(dataset_files):
        lu, X_l, N, cy, dt = read_N_and_H_from_filename(dataset_file) 
        ny=int(cy*N)   
        data = np.loadtxt(dataset_file, skiprows=1)
        new_shape = (ny+2, 9, X_l*N)
        # new_shape = (1+cy*N, 9, X_l*N)
        data = data.reshape(new_shape)
        # y = np.arange(0, cy, 1/N) -1/N/2
        D = -1.25
        S =1.25
        # Plot for each j value
        print(f"Dataset {i + 1}: N = {N}, cy = {cy}, dt = {dt}, lu = {lu}")
        du=N*dt
        # du=data[ny, 3, (int(1* N))]
        for j in range(10):
            if lu==2.5:
                ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D-10) * N))] / du
            elif lu==7.5:
                ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D-5) * N))] / du
            elif lu==10:
                ux_ave = data[0:(ny), 3, (int((j * S+7.5+5+D-2.5) * N))] / du
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
    
    Uxexp()
    OFux()
    plt.xlabel('x/H+u/$U_{ref}$')  #$U_{\infty}$
    plt.ylabel('y/H')


def hillplot_Ruu(dataset_files, line_styles, colors, llabel=None):
    solidhill()
    for i, (dataset_file) in enumerate(dataset_files):
        lu, X_l, N, cy, dt = read_N_and_H_from_filename(dataset_file) 
        ny=int(cy*N)   
        data = np.loadtxt(dataset_file, skiprows=1)
        new_shape = (ny+2, 9, X_l*N)
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
            elif lu==10:
                ux_ave = Ru[0: (ny),(int((j * S+7.5+5+D-2.5) * N))] /du /0.2
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
    Ruuexp()
    OFRuu()
    plt.xlabel('x/H+Ruu/$U_{ref}$')  #$U_{\infty}$
    plt.ylabel('y/H')


#  function for UX
def Uxexp():
    Edata2 = np.loadtxt('EXP2.txt', delimiter=',')
    x2 = Edata2[:, 0]+2.5
    y2 = Edata2[:, 1] 
    plt.scatter(x2, y2, marker='o', c='none',edgecolors='r', s=180, label='Exp.')
def OFux():
    # ==========================OPENFOAM========================================
    h=0.04
    x_shift = 1.25
    ur=5.66
    # Define the folder path
    # folder_paths = ['MeshF5_2']
    folder_paths = ['Mesh_lowy10']
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
            plt.plot(x_shifted, y, label=file_path,color='pink',linestyle=':', linewidth=2,zorder=1) 
        elif i>=18 and i<27:
            x_shifted = x + (i-18) * x_shift  # Shift x-values for each dataset
            plt.plot(x_shifted, y, label=file_path,color='purple',linestyle='-.', linewidth=2,zorder=1) 
        elif i>=27:
            x_shifted = x + (i-27) * x_shift  # Shift x-values for each dataset
            plt.plot(x_shifted, y, label=file_path,color='olive',linestyle=':', linewidth=2,zorder=1)     
    #=======================================================
#  function for Ruu
def Ruuexp():
    Ruic = np.loadtxt('sigmaU.txt', delimiter=',')
    xru= Ruic[:, 0]+2.5; yru= Ruic[:, 1]
    plt.scatter(xru, yru, marker='o', c='none', edgecolors='r', s=50, label='exp_u')
def OFRuu():
    h=0.04
    x_shift = 1.25
    ur=5.66
    # Define the folder path
    # folder_paths = ['MeshF5_2']
    folder_paths = ['Mesh_corase1']
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

######### Plot SIN hill     ##################################
def solidhill():   
    amplitude_xy = 1;frequency_xy = 0.25;length_xy = 2.5
    XS = np.linspace(4.5, 9.5, 1000)
    sine_hill_YS = amplitude_xy * np.cos(2 * np.pi * frequency_xy * ((XS - 7) / length_xy)) ** 2
    plt.plot(XS-4.5, sine_hill_YS, color='black')
    # Fill the area under the sine hill curve
    plt.fill_between(XS - 4.5, sine_hill_YS, color='lightgrey',zorder=0)

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

