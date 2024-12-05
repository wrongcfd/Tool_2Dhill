import numpy as np
import h5py

name = '_finalv2f_zdir_'
hdfname = 'hdf_R0N0.h5'
Gf = h5py.File(hdfname, 'r')
print('Total items in hdf5 file:', len(Gf.keys()), '\n')

logfile = 'log.log'  # the name of the output log file

# Parse log file for necessary parameters
with open(logfile, 'r') as log:
    lines = log.readlines()
    for line in lines:
        if "Write out frequency" in line:
            frequency = ''.join([i for i in line if i.isdigit()])
            q = int(frequency)
            print('Output frequency is ', q, '\n')
        elif "Number of time steps to run" in line:
            totalstep = ''.join([i for i in line if i.isdigit()])
            T = int(totalstep)
            print('The total time steps is', T, '\n')
        elif "Lattice spacing" in line:
            spacing = line.split('=')[-1].strip()
            res = int(1 / float(spacing))
            print('The resolution is', res, '\n')
        elif "Lattice time step" in line:
            time_step = line.split('=')[-1].strip()
            dt = '{:.10g}'.format(float(time_step))
            print('The dt is', dt, '\n')
        elif "L0 Grid size" in line:
            grid_size = line.split('=')[-1].strip()
            xh, yh, zh = [int(value) for value in grid_size.split('x')]

xh = int(xh / res)
yh = int((yh - 1) / res)
zh = int(zh / res)
print(f'L0 Grid size is xh={xh}, yh={yh}, zh={zh}\n')

# Calculate the time division
DT = int(T / q)
print(DT, 'vtk-files will be outputted', '\n')

# Processing GASCANS data with chunk-wise approach
for t in range(DT):
    time = 'Time_' + str((t + 1) * q)
    print('\ttime step =', time)

    # Load grid positions (only once since they don't change over time)
    if t == 0:
        xPos = Gf['Time_0/XPos']
        yPos = Gf['Time_0/YPos']
        zPos = Gf['Time_0/ZPos']
        x = xPos[0, 0, :]
        y = yPos[0, :, 0]
        z = zPos[:, 0, 0]

    # Chunk-wise processing
    Ux = Gf[time + '/Ux']
    Uy = Gf[time + '/Uy']
    Uz = Gf[time + '/Uz']
    Ux_ave = Gf[time + '/Ux_TimeAv']
    Uy_ave = Gf[time + '/Uy_TimeAv']
    Uz_ave = Gf[time + '/Uz_TimeAv']
    UxUx_TimeAv = Gf[time + '/UxUx_TimeAv']

    # Initialize arrays to store the z-averaged results
    Ux_z_ave = np.zeros((Ux.shape[1], Ux.shape[2]), dtype=np.float32)
    Uy_z_ave = np.zeros_like(Ux_z_ave)
    Uz_z_ave = np.zeros_like(Ux_z_ave)
    Ux_ave_z_ave = np.zeros_like(Ux_z_ave)
    Uy_ave_z_ave = np.zeros_like(Ux_z_ave)
    Uz_ave_z_ave = np.zeros_like(Ux_z_ave)
    UxUx_TimeAv_z_ave = np.zeros_like(Ux_z_ave)

    # Compute z-averages chunk by chunk
    for z_slice in range(Ux.shape[0]):
        Ux_z_ave += Ux[z_slice, :, :] / zh
        Uy_z_ave += Uy[z_slice, :, :] / zh
        Uz_z_ave += Uz[z_slice, :, :] / zh
        Ux_ave_z_ave += Ux_ave[z_slice, :, :] / zh
        Uy_ave_z_ave += Uy_ave[z_slice, :, :] / zh
        Uz_ave_z_ave += Uz_ave[z_slice, :, :] / zh
        UxUx_TimeAv_z_ave += UxUx_TimeAv[z_slice, :, :] / zh

    # Save the 0D data to a .h5 file
    output_file = f'SP_X{xh}_CAON{res}_H{yh}_Z{zh}_dt{dt}{name}{time}_0D.h5'
    with h5py.File(output_file, 'w') as hf:
        hf.create_dataset('Ux_z_ave', data=Ux_z_ave)
        hf.create_dataset('Uy_z_ave', data=Uy_z_ave)
        hf.create_dataset('Uz_z_ave', data=Uz_z_ave)
        hf.create_dataset('Ux_ave_z_ave', data=Ux_ave_z_ave)
        hf.create_dataset('Uy_ave_z_ave', data=Uy_ave_z_ave)
        hf.create_dataset('Uz_ave_z_ave', data=Uz_ave_z_ave)
        hf.create_dataset('UxUx_TimeAv_z_ave', data=UxUx_TimeAv_z_ave)

    print('\tFinished', t + 1, '/', DT, '\n')

Gf.close()
print('Work finished')
