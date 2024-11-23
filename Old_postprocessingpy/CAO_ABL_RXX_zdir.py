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
            # if char == 'H' and part[i+1:].isdigit():
            if char == 'H' and i < len(part) - 1 and part[i+1:].replace('.', '').isdigit():
                cy = float(part[i+1:])
            if char == 't' and i < len(part) - 1 and part[i+1:].replace('.', '').isdigit():
                dt = float(part[i+1:])
    return X_l, N, cy,dt


dataset_files = [   
        # ('ABL_X30_CAON20_H13_Z6_dt0.002_finalv2f_Time_200000.txt'),
        # ('ABLSP_X25_CAON20_H6_Z6_dt0.002_finalv2f_Time_200000.txt'),
          ('ABLSP_X25_CAON20_H6_Z6_dt0.002_finalv2f_re6000_Time_200000.txt'),
        ('ABLSP_X25_CAON20_H6_Z6_dt0.002_finalv2f_re48000_Time_200000.txt'),
        # ('ABL_X30_CAON40_H13_Z6_dt0.001_finalv2f_smag_0.0064_Time_200000.txt'),
] 

plt.rc('font', size=14)   
fig = plt.gcf()
fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

colors = ['steelblue', 'pink', 'olive', 'black', 'orange']
# colors = ['olive', 'blue', 'violet', 'orange', 'black']
# colors = ['steelblue', 'violet', 'orange', 'violet', 'black']
line_styles = ['-', '--', '--', '--', ':']

for i, (dataset_file) in enumerate(dataset_files):
    X_l, N, cy, dt = read_N_and_H_from_filename(dataset_file) 
    ny=int(cy*N)   
    du=N*dt
    data = np.loadtxt(dataset_file, skiprows=1)
    new_shape = (120, 9, ny+1)
    # new_shape = (1+cy*N, 9, X_l*N)
    data = data.reshape(new_shape)
    # y = np.arange(0, cy, 1/N) -1/N/2
    D = 0
    S =0.5
    a=0
    ux_ave = data[:,3+a,:]
    uux_ave = data[:,6+a,:]
    Ru=np.sqrt((uux_ave-ux_ave**2))
        # Calculate the average of Ru over the first dimension
    aveRuu = np.mean(Ru, axis=0) /du
    aveRuu = aveRuu[0:ny]
    y=np.arange(0, cy, 1/N) -1/N/2  
    # Plot for each j value

    for j in range(1):
        ux_ave = Ru[(int((3 * S+D) * N)), 0: (ny)] /du
        # for line in one X 
        plt.plot(ux_ave, y, linestyle='--', linewidth=2.5, zorder=1)
    plt.plot(aveRuu, y,  zorder=1)
# ========================Read data from exp========================================
Edata_Ruu = np.loadtxt('Ruu.txt', delimiter=',')
Edata_Rvv = np.loadtxt('Rww.txt', delimiter=',')
Edata_Rww = np.loadtxt('Rvv.txt', delimiter=',')

u_prime = Edata_Ruu[:, 0]
y_u = Edata_Ruu[:, 1]
uup = u_prime**2
plt.scatter(np.sqrt(uup), y_u, label='$\sigma_u$ - Exp.', color='steelblue')


# plt.xticks(np.arange(-2.5, 12.5, 1.25))
plt.xlim(0, 0.25)
plt.ylim(0,4)
plt.xlabel('x/H+u/$U_{ref}$')  #$U_{\infty}$
plt.ylabel('y/H')
# Get only the handles and labels for solid and dashed lines
plt.savefig('LBM_hill.png', bbox_inches='tight')
plt.get_current_fig_manager().window.state('zoomed')
plt.show()
plt.close()