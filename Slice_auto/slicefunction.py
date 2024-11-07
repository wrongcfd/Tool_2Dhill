# hdf5_to_txt_converter.py
import numpy as np
import h5py
import os

class HDF5ToTXTConverter:
    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.hdfname = os.path.join(folder, 'hdf_R0N0.h5')
        self.logfile = os.path.join(folder, 'log.log')
        self.q = None
        self.T = None
        self.res = None
        self.dt = None
        self.xh = None
        self.yh = None
        self.zh = None

    def read_log_file(self):
        with open(self.logfile) as log:
            lines = log.readlines()
            for line in lines:
                if "Write out frequency" in line:
                    frequency = ''.join([i for i in line if str.isdigit(i)])
                    self.q = int(frequency)
                elif "Number of time steps to run" in line:
                    totalstep = ''.join([i for i in line if str.isdigit(i)])
                    self.T = int(totalstep)
                elif "Lattice spacing" in line:
                    spacing = float(line.split('=')[-1].strip())
                    self.res = int(1 / spacing)
                elif "Lattice time step" in line:
                    time_step = float(line.split('=')[-1].strip())
                    self.dt = '{:.10g}'.format(time_step)
                elif "L0 Grid size" in line:
                    grid_size = line.split('=')[-1].strip()
                    self.xh, self.yh, self.zh = [int(value) for value in grid_size.split('x')]

            # Adjust grid size by resolution
            self.xh = int(self.xh / self.res)
            self.yh = int((self.yh - 1) / self.res)
            self.zh = int(self.zh / self.res)
        print(f"L0 Grid size is xh={self.xh}, yh={self.yh}, zh={self.zh}")

    def process_data(self):
        with h5py.File(self.hdfname, 'r') as Gf:
            print(f"Total items in hdf5 file: {len(Gf.keys())}\n")
            DT = int(self.T / self.q)
            print(f"{DT} vtk-files will be outputted\n")

            for t in range(DT):
                time = f"Time_{(t + 1) * self.q}"
                print(f"\ttime step = {time}")
                xPos = Gf['Time_0/XPos']
                yPos = Gf['Time_0/YPos']
                zPos = Gf['Time_0/ZPos']
                x = xPos[0, 0, :]
                y = yPos[0, :, 0]
                z = zPos[:, 0, 0]

                # Extract data
                Ux = Gf[time + '/Ux'][:, :, :]
                Uy = Gf[time + '/Uy'][:, :, :]
                Uz = Gf[time + '/Uz'][:, :, :]
                Ux_ave = Gf[time + '/Ux_TimeAv'][:, :, :]
                Uy_ave = Gf[time + '/Uy_TimeAv'][:, :, :]
                Uz_ave = Gf[time + '/Uz_TimeAv'][:, :, :]
                UxUx_TimeAv = Gf[time + '/UxUx_TimeAv'][:, :, :]
                UyUy_TimeAv = Gf[time + '/UyUy_TimeAv'][:, :, :]
                UzUz_TimeAv = Gf[time + '/UzUz_TimeAv'][:, :, :]

                # Average in the z-direction
                Ux_z_ave = np.mean(Ux, axis=0)
                Uy_z_ave = np.mean(Uy, axis=0)
                Uz_z_ave = np.mean(Uz, axis=0)
                Ux_ave_z_ave = np.mean(Ux_ave, axis=0)
                Uy_ave_z_ave = np.mean(Uy_ave, axis=0)
                Uz_ave_z_ave = np.mean(Uz_ave, axis=0)
                UxUx_TimeAv_z_ave = np.mean(UxUx_TimeAv, axis=0)
                UyUy_TimeAv_z_ave = np.mean(UyUy_TimeAv, axis=0)
                UzUz_TimeAv_z_ave = np.mean(UzUz_TimeAv, axis=0)

                # Write to file
                output_file = os.path.join(
                    self.folder,
                    f"ABLSP_X{self.xh}_N{self.res}_H{self.yh}_Z{self.zh}_dt{self.dt}{self.name}{time}.txt"
                )
                with open(output_file, 'w') as f:
                    f.write('Ux_z_ave Uy_z_ave Uz_z_ave Ux_ave_z_ave Uy_ave_z_ave Uz_ave_z_ave UxUx_TimeAv_z_ave UyUy_TimeAv_z_ave UzUz_TimeAv_z_ave\n')
                    np.savetxt(f, np.column_stack((Ux_z_ave, Uy_z_ave, Uz_z_ave, Ux_ave_z_ave, Uy_ave_z_ave, Uz_ave_z_ave, UxUx_TimeAv_z_ave, UyUy_TimeAv_z_ave, UzUz_TimeAv_z_ave)))

                print(f"\tFinished {t + 1} / {DT}\n")
        print("Processing complete")

    def run(self):
        self.read_log_file()
        self.process_data()
