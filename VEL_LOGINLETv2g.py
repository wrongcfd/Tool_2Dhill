import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math
import os

exp2001 = np.loadtxt('caouinlet.txt')
u2001=exp2001[:, 0];y2001=exp2001[:, 1] /40
# Load data for Ruu, Rvv, and Rww

# Parameters


cy =10
numPoints =40
wall_name = f'{numPoints}_{cy}Hv2g'

semname = "inlet_VEL_dos" + wall_name + ".txt"
real_name= "inlet_VEL" + wall_name + ".txt"
cz = 6.0
resolution = 1.0 / float(numPoints)
# Generating values for y from 0 to 3.0 with a step of 0.02
y2 = np.arange(0, cy+resolution, resolution)
# Initialize arrays to store  values for Ruu, Rvv, and Rww
outputFile = semname


u_star =0.1926
z0=0.000004
f = open(outputFile, "w")

f.write("velocity\n")
f.write("u v w\n")
h=6.2
a = 0.1004097650430536
b = 0.7984478664757343       
for j in range(1, int(cy * numPoints)+1):
    for k in range(0, int(cz * numPoints)):
        if j <2 :
            ux = 0
            f.write(str(ux) + " " + str(0) + " " + str(0) +"\n")
        else:
            z_values=(j-1.5)/ numPoints*0.04
            ux =u_star/0.4*np.log((z_values+z0)/z0) /5.66
            k=(ux*0.03)**2*1.5
            ep=(0.09**0.75)*(k**(1.5))
            if j> 6.2*numPoints:
                newy=int (6.2*numPoints)
                # z_values=(6.2*numPoints-1.5)/ numPoints*0.04
                # ux =u_star/0.4*np.log((z_values+z0)/z0) /5.66
                # k=(ux*0.03)**2*1.5
                # ep=(0.09**0.75)*(k**(1.5))
            f.write(str(ux) + " " + str(0) + " " + str(0) +"\n")

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
