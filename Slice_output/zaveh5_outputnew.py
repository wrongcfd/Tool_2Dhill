import numpy as np
import h5py
import os
import glob

# === Step 1: Find the latest output folder ===
output_dirs = sorted(glob.glob("output*"), key=os.path.getmtime, reverse=True)
if not output_dirs:
    raise RuntimeError("No output*/ folder found.")
latest_dir = output_dirs[0]
print(f'Using latest output folder: {latest_dir}')

# Change working directory
os.chdir(latest_dir)

# === Step 2: Locate required files ===
logfile = 'log.log'
h5files = sorted(glob.glob('hdf_*.h5'))
if not os.path.exists(logfile):
    raise RuntimeError(f"log.log not found in {latest_dir}")
if not h5files:
    raise RuntimeError(f"No hdf_*.h5 file found in {latest_dir}")

hdfname = h5files[0]
name = '_finalv2f_zdir_'
Gf = h5py.File(hdfname, 'r')
print(f'Total items in hdf5 file: {len(Gf.keys())}\n')

# === Step 3: Parse log file ===
with open(logfile, 'r') as log:
    lines = log.readlines()
    for line in lines:
        if "Write out frequency" in line:
            frequency = ''.join(i for i in line if i.isdigit())
            q = int(frequency)
            print(f'Output frequency is {q}\n')
        elif "Number of time steps to run" in line:
            totalstep = ''.join(i for i in line if i.isdigit())
            T = int(totalstep)
            print(f'The total time steps is {T}\n')
        elif "Lattice spacing" in line:
            spacing = line.split('=')[-1].strip()
            res = int(1.0 / float(spacing))
            print(f'The resolution is {res}\n')
        elif "Lattice time step" in line:
            time_step = line.split('=')[-1].strip()
            dt = f'{float(time_step):.10g}'
            print(f'The dt is {dt}\n')
        elif "L0 Grid size" in line:
            grid_size = line.split('=')[-1].strip()
            xh, yh, zh = [int(value) for value in grid_size.split('x')]

xh = int(xh / res)
yh = int((yh - 1) / res)
zh = int(zh / res)
print(f'L0 Grid size is xh={xh}, yh={yh}, zh={zh}\n')

DT = int(T / q)
print(f'{DT} vtk-files will be outputted\n')

# === Step 4: Read and process ===
for t in range(DT):
    time = f'Time_{(t + 1) * q}'
    print(f'\ttime step = {time}')

    if t == 0:
        x = Gf['Time_0/XPos'][0, 0, :]
        y = Gf['Time_0/YPos'][0, :, 0]
        z = Gf['Time_0/ZPos'][:, 0, 0]

    Ux = Gf[time + '/Ux']
    Uy = Gf[time + '/Uy']
    Uz = Gf[time + '/Uz']
    Ux_ave = Gf[time + '/Ux_TimeAv']
    Uy_ave = Gf[time + '/Uy_TimeAv']
    Uz_ave = Gf[time + '/Uz_TimeAv']
    UxUx_TimeAv = Gf[time + '/UxUx_TimeAv']

    Ux_z_ave = np.zeros((Ux.shape[1], Ux.shape[2]), dtype=np.float32)
    Uy_z_ave = np.zeros_like(Ux_z_ave)
    Uz_z_ave = np.zeros_like(Ux_z_ave)
    Ux_ave_z_ave = np.zeros_like(Ux_z_ave)
    Uy_ave_z_ave = np.zeros_like(Ux_z_ave)
    Uz_ave_z_ave = np.zeros_like(Ux_z_ave)
    UxUx_TimeAv_z_ave = np.zeros_like(Ux_z_ave)

    for z_slice in range(Ux.shape[0]):
        Ux_z_ave += Ux[z_slice, :, :] / zh
        Uy_z_ave += Uy[z_slice, :, :] / zh
        Uz_z_ave += Uz[z_slice, :, :] / zh
        Ux_ave_z_ave += Ux_ave[z_slice, :, :] / zh
        Uy_ave_z_ave += Uy_ave[z_slice, :, :] / zh
        Uz_ave_z_ave += Uz_ave[z_slice, :, :] / zh
        UxUx_TimeAv_z_ave += UxUx_TimeAv[z_slice, :, :] / zh

    output_file = f'SP_X{xh}_CAON{res}_H{yh}_Z{zh}_dt{dt}{name}{time}_0D.h5'
    with h5py.File(output_file, 'w') as hf:
        hf.create_dataset('Ux_z_ave', data=Ux_z_ave)
        hf.create_dataset('Uy_z_ave', data=Uy_z_ave)
        hf.create_dataset('Uz_z_ave', data=Uz_z_ave)
        hf.create_dataset('Ux_ave_z_ave', data=Ux_ave_z_ave)
        hf.create_dataset('Uy_ave_z_ave', data=Uy_ave_z_ave)
        hf.create_dataset('Uz_ave_z_ave', data=Uz_ave_z_ave)
        hf.create_dataset('UxUx_TimeAv_z_ave', data=UxUx_TimeAv_z_ave)

    print(f'\tFinished {t + 1} / {DT}\n')

Gf.close()
print('Work finished')
