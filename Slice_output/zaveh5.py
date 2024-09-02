import numpy as np
import h5py
from pyevtk.hl import VtkFile, VtkRectilinearGrid

name='_finalv2f_zdir_'
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
        print('The resolution is', res, '\n')
    elif("Lattice time step" in line):
        time_step =line.split('=')[-1].strip()
        dt = '{:.10g}'.format(float(time_step))
        print('The dt is', dt, '\n')  
    elif "L0 Grid size" in line:
        grid_size = line.split('=')[-1].strip()
        xh, yh, zh = [int(value) for value in grid_size.split('x')]           
log.close()

xh = int(xh / res)
yh = int((yh - 1) / res)
zh = int(zh / res)
print(f'L0 Grid size is xh={xh}, yh={yh}, zh={zh}\n') 
# calculate the time division
DT = int(T/q)
print(DT, 'vtk-files will be outputed', '\n')

# processing GASCANS data
for t in range(DT ):

    # time step to process
    time = 'Time_' + str((t+1) * q)
    print('\ttime step =', time)
    # Find the index 
    xPos = Gf['Time_0/XPos']
    yPos = Gf['Time_0/YPos']
    zPos = Gf['Time_0/ZPos']
    x = xPos[0, 0, :]
    y = yPos[0, :, 0]
    z = zPos[:, 0, 0]

    # Calculate the middle index for X and Z as integers
    #x_middle = (len(x) // 2)
    # x_middle = (1)


  # Extract the needed data sets at the specified integer indices
    Ux = Gf[time + '/Ux'][:, :, :]
    Uy = Gf[time + '/Uy'][:, :, :]
    Uz = Gf[time + '/Uz'][:, :, :]
    Ux_ave = Gf[time + '/Ux_TimeAv'][:, :, :]
    Uy_ave = Gf[time + '/Uy_TimeAv'][:, :, :]
    Uz_ave = Gf[time + '/Uz_TimeAv'][:, :, :]
    UxUx_TimeAv = Gf[time + '/UxUx_TimeAv'][:, :, :]
    UyUy_TimeAv = Gf[time + '/UyUy_TimeAv'][:, :, :]
    UzUz_TimeAv = Gf[time + '/UzUz_TimeAv'][:, :, :]

    # Average in the z-direction (axis=0, the third dimension)
    Ux_z_ave = np.mean(Ux, axis=0)
    Uy_z_ave = np.mean(Uy, axis=0)
    Uz_z_ave = np.mean(Uz, axis=0)
    Ux_ave_z_ave = np.mean(Ux_ave, axis=0)
    Uy_ave_z_ave = np.mean(Uy_ave, axis=0)
    Uz_ave_z_ave = np.mean(Uz_ave, axis=0)
    UxUx_TimeAv_z_ave = np.mean(UxUx_TimeAv, axis=0)
    UyUy_TimeAv_z_ave = np.mean(UyUy_TimeAv, axis=0)
    UzUz_TimeAv_z_ave = np.mean(UzUz_TimeAv, axis=0)

    # Save the 0D data to a .h5 file
    output_file = 'SP_X'+ str(xh)+'_CAON'+str(res)+'_H'+str(yh)+'_Z'+str(zh) +'_dt'+str(dt) + name+ time + '_0D.h5'
    with h5py.File(output_file, 'w') as hf:
        hf.create_dataset('Ux_z_ave', data=Ux_z_ave)
        hf.create_dataset('Uy_z_ave', data=Uy_z_ave)
        hf.create_dataset('Uz_z_ave', data=Uz_z_ave)
        hf.create_dataset('Ux_ave_z_ave', data=Ux_ave_z_ave)
        hf.create_dataset('Uy_ave_z_ave', data=Uy_ave_z_ave)
        hf.create_dataset('Uz_ave_z_ave', data=Uz_ave_z_ave)
        hf.create_dataset('UxUx_TimeAv_z_ave', data=UxUx_TimeAv_z_ave)
        hf.create_dataset('UyUy_TimeAv_z_ave', data=UyUy_TimeAv_z_ave)
        hf.create_dataset('UzUz_TimeAv_z_ave', data=UzUz_TimeAv_z_ave)
    
    print('\tfinishing', t + 1, '/', DT, '\n')

Gf.close()
print('work finished')





