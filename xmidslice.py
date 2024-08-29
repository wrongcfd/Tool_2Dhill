import numpy as np
import h5py
from pyevtk.hl import VtkFile, VtkRectilinearGrid

name='_finalv2f_re48000_'
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
    x_middle = (len(x) // 2) 

  # Extract the needed data sets at the specified integer indices
    Ux = Gf[time + '/Ux'][:, :, x_middle]
    Uy = Gf[time + '/Uy'][:, :, x_middle]
    Uz = Gf[time + '/Uz'][:, :, x_middle]
    Ux_ave = Gf[time + '/Ux_TimeAv'][:, :, x_middle]
    Uy_ave = Gf[time + '/Uy_TimeAv'][:, :, x_middle]
    Uz_ave = Gf[time + '/Uz_TimeAv'][:, :, x_middle]
    UxUx_TimeAv = Gf[time + '/UxUx_TimeAv'][:, :, x_middle]
    UyUy_TimeAv = Gf[time + '/UyUy_TimeAv'][:, :, x_middle]
    UzUz_TimeAv = Gf[time + '/UzUz_TimeAv'][:, :, x_middle]

    # Save the data to a .txt file with a time-specific name
    output_file = 'ABLSP_X'+ str(xh)+'_CAON'+str(res)+'_H'+str(yh)+'_Z'+str(zh) +'_dt'+str(dt) + name+ time + '.txt'
    with open(output_file, 'w') as f:
        f.write('Ux Uy Uz Ux_ave Uy_ave Uz_ave UxUx_TimeAv UyUy_TimeAv UzUz_TimeAv\n')
        np.savetxt(f, np.column_stack(( Ux, Uy, Uz, Ux_ave, Uy_ave, Uz_ave, UxUx_TimeAv, UyUy_TimeAv, UzUz_TimeAv)))

    print('\tfinishing', t + 1, '/', DT, '\n')
    print( x_middle , '\n')

Gf.close()
print('work finished')





