import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math
import os

exp2001 = np.loadtxt('caouinlet.txt')
u2001=exp2001[:, 0];y2001=exp2001[:, 1] /40
# Load data for Ruu, Rvv, and Rww
Edata_Ruu = np.loadtxt('Ruu.txt', delimiter=',')
Edata_Rvv = np.loadtxt('Rvv.txt', delimiter=',')
Edata_Rww = np.loadtxt('Rww.txt', delimiter=',')
# Edata_Ruu[:, 0] = Edata_Ruu[:, 0] *0.03
# Edata_Ruu[:, 1] = Edata_Ruu[:, 1] *6.25
# Edata_Rww[:, 0] = Edata_Rww[:, 0] *0.03
# Edata_Rww[:, 1] = Edata_Rww[:, 1] *6.25
# Parameters
cy = 13
numPoints =5
wall_name = f'{numPoints}_{cy}Hv2b'

semname = "inlet_SEM_dos" + wall_name + ".txt"
real_name= "inlet_SEM" + wall_name + ".txt"
cz = 6.0
resolution = 1.0 / float(numPoints)
# Generating values for y from 0 to 3.0 with a step of 0.02
y2 = np.arange(0, cy+resolution, resolution)
# Initialize arrays to store  values for Ruu, Rvv, and Rww
Ruu = np.zeros_like(y2)
Rvv = np.zeros_like(y2)
Rww = np.zeros_like(y2)
# Loop for each variable (Ruu, Rvv, Rww)
for data, _variable in zip([Edata_Ruu, Edata_Rvv, Edata_Rww], [Ruu, Rvv, Rww]):
    # Extracting data
    u_data = data[:, 0] ** 2
    y_data = data[:, 1]
    # Create an interpolation function
    interpolating_function = interp1d(y_data, u_data, kind='linear', fill_value='extrapolate')
    # Interpolating values for the new y values
    _variable[:] = interpolating_function(y2)
outputFile = semname


u_star =0.1926
z0=0.000004
f = open(outputFile, "w")

f.write("SEM\n")
f.write("U V W uu uv uw vv vw ww epsilon\n")
h=30
a = 0.1004097650430536
b = 0.7984478664757343       
for j in range(1, int(cy * numPoints)+1):
    for k in range(0, int(cz * numPoints)):
        if j <2 :
            ux = 0
            f.write(str(ux) + " " + str(0) + " " + str(0) + " " + str(Ruu[j])+ " " + str(0)+ " " + str(0)+ " " + str(Rww[j])+ " " + str(0)+ " " + str(Rvv[j])  + " " + str(0) +"\n")
        elif j> 30*numPoints:
            #ux = a * math.log( (6*numPoints+0)/ numPoints) + b

            k=(ux*0.05)**2*1.5
            ep=(0.09**0.75)*(k**(1.5))
            f.write(str(ux) + " " + str(0) + " " + str(0) + " " + str(Ruu[h])+ " " + str(0)+ " " + str(0)+ " " + str(Rww[h])+ " " + str(0)+ " " + str(Rvv[h])  + " " + str(ep) +"\n")
        else:
            z_values=(j-1.5)/ numPoints*0.04
            ux =u_star/0.4*np.log((z_values+z0)/z0) /5.66
            k=(ux*0.03)**2*1.5
            ep=(0.09**0.75)*(k**(1.5))
            if Ruu[j]<0:
                Ruu[j]=0
            if Rvv[j]<0:
                Rvv[j]=0
            if Rww[j]<0:
                Rww[j]=0
            if ux>1.0:
                ux=1.0
            f.write(str(ux) + " " + str(0) + " " + str(0) + " " + str(Ruu[j])+ " " + str(0)+ " " + str(0)+ " " + str(Rww[j])+ " " + str(0)+ " " + str(Rvv[j])  + " " + str(ep) +"\n")

f.close()
# Specify the input and output file names
def convert_dos_to_unix(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        content = infile.read()

    content_unix = content.replace('\r\n', '\n')

    with open(output_file, 'w', newline='\n') as outfile:
        outfile.write(content_unix)
            # Remove the original file
    os.remove(input_file)

# Convert the file to UNIX format
convert_dos_to_unix(semname, real_name)



# Plotting the original data and the interpolated curve
# plt.scatter(u2001, y2001, marker='*',  color='red', label='exp_2006')
# j = np.linspace(2, 10*5, 10*5-2)
# z_values=(j-1.5)/ 5
# ux =u_star/0.4*np.log((z_values*0.04+z0)/z0) /5.66

# ux2 = a * np.log(z_values) + b
# plt.xlim(0, 1.2)

# plt.plot(ux, z_values, color='red', label='log')
# plt.plot(ux2, z_values, color='pink', label='Interpolated Curve')
# # plt.legend()
# plt.show()
# plt.close()
# # Plotting the original data and the interpolated curve for Ruu
# plt.scatter(Edata_Ruu[:, 0], Edata_Ruu[:, 1], marker='o', color='blue', label='Original Data (Ruu)')
# plt.scatter( np.sqrt(Ruu),y2, color='red', label='Interpolated Curve (Ruu)')
# plt.xlim(0, 0.25)
# plt.xlabel('y')
# plt.ylabel('Ruu')
# plt.legend()
# plt.show()
# plt.close()
