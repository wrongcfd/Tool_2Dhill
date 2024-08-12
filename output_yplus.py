import numpy as np
import math
import h5py
import matplotlib.pyplot as plt
from pyevtk.hl import VtkFile, VtkRectilinearGrid

# hdf5 file to be converted
hdfname = 'hdf_R0N0.h5'
Gf = h5py.File(hdfname, 'r')
print('Total items in hdf5 file:', len(Gf.keys()), '\n')
# read in log.log file to get the necessary information
logfile = 'log.log' # the name of the output log file
log = open(logfile)
lines = log.readlines()
for line in lines:
    if("Write out frequency" in line):
        frequency = [i for i in line if str.isdigit(i)]
        frequency = ''.join(frequency)
        q = int(frequency)
        print('Output frequency is ', q, '\n')
    elif("Number of time steps to run" in line):
        totalstep = [i for i in line if str.isdigit(i)]
        totalstep = ''.join(totalstep)
        T = int(totalstep)
        print('The total time steps is', T, '\n')
    elif("Lattice spacing" in line):
        spacing =line.split('=')[-1].strip()
        res = int(1/float(spacing))
        print('The resolution is',res, '\n')
    elif " Lattice viscosity" in line:
        viscosity = line.split('=')[-1].strip()
        nu = float(viscosity)  # Convert viscosity to float here
        print('The nu is', nu, '\n')
    elif "L0 Grid size" in line:
        grid_size = line.split('=')[-1].strip()
        xh, yh, zh = [int(value) for value in grid_size.split('x')]  
log.close()
N=yh
cy = int((yh - 1) / res)
# calculate the time division
DT = int(T/q)
print(DT, 'vtk-files will be outputed', '\n')
# processing GASCANS data
# processing GASCANS data
for t in range(DT):

    # time step to process
    time = 'Time_' + str((t+1) * q)
    print('\ttime step =', time)

    # extract the needed data sets.
    print('\treading hdf5')
    # Find the index 
    xPos = Gf['Time_0/XPos']
    yPos = Gf['Time_0/YPos']
    zPos = Gf['Time_0/ZPos']
    x = xPos[0, 0, :]
    y = yPos[0, :, 0]
    z = zPos[:, 0, 0]

    # Calculate the middle index for X and Z as integers
    #x_middle = (len(x) // 2)
    z_middle = (len(z) // 2)
    x_middle = (len(x) // 10)

  # Extract the needed data sets at the specified integer indices
    Ux = Gf[time + '/Ux'][z_middle - 1, :, x_middle - 1]
    Uy = Gf[time + '/Uy'][z_middle - 1, :, x_middle - 1]
    Uz = Gf[time + '/Uz'][z_middle - 1, :, x_middle - 1]
    Ux_ave = Gf[time + '/Ux_TimeAv'][z_middle - 1, :, x_middle - 1]
    Uy_ave = Gf[time + '/Uy_TimeAv'][z_middle - 1, :, x_middle - 1]
    Uz_ave = Gf[time + '/Uz_TimeAv'][z_middle - 1, :, x_middle - 1]
    UxUx_TimeAv = Gf[time + '/UxUx_TimeAv'][z_middle - 1, :, x_middle - 1]
    UyUy_TimeAv = Gf[time + '/UyUy_TimeAv'][z_middle - 1, :, x_middle - 1]
    UzUz_TimeAv = Gf[time + '/UzUz_TimeAv'][z_middle - 1, :, x_middle - 1]

    # Save the data to a .txt file with a time-specific name
    output_file = 'yplusline_' + time + '.txt'
    with open(output_file, 'w') as f:
        f.write('Ux Uy Uz Ux_ave Uy_ave Uz_ave UxUx_TimeAv UyUy_TimeAv UzUz_TimeAv\n')
        np.savetxt(f, np.column_stack((Ux, Uy, Uz, Ux_ave, Uy_ave, Uz_ave, UxUx_TimeAv, UyUy_TimeAv, UzUz_TimeAv)))

    print('\tfinishing', t + 1, '/', DT, '\n')

Gf.close()
print('work finished')

# Define the dataset files
dataset_file = output_file
data = np.loadtxt(dataset_file, skiprows=1)
# Extract data
x = np.arange(0.5, N-1, 1)  # grids in Y
ux = data[1:N, 0]

u_ave = data[1:N, 3]
v_ave = data[1:N, 4]
w_ave = data[1:N, 5]

uu_ave = data[1:N, 6]
vv_ave = data[1:N, 7]
ww_ave = data[1:N, 8]
# Print the values of u_ave[0] and nu
print("u_ave[0] =", u_ave[0])
print("u_ave[0] =", x[0])
print("nu =", nu)
# Calculate u+, y+, and add 0, 0
u_tau = math.sqrt(u_ave[0] / 0.5 * nu)
u_plus = u_ave / u_tau
y_plus = u_tau * x / nu

# Print the first and second values of y_plus
print("u_tau =", u_tau)
print("First value of y_plus:", y_plus[0])
print("Second value of y_plus:", y_plus[1])

plt.plot(y_plus, u_plus, label=f'U+ ({N})', color='skyblue', linewidth=2)
plt.xscale('log')
plt.xlim(0.1, 10000)

#print(y_plus[0])
plt.xlabel('y+')
plt.ylabel('U+')
plt.legend()

# Save the figure
plt.savefig('y+.png')
plt.close()