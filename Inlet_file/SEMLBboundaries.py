import os
# User input: cell size
grid=5
h=13


d = 1.0/grid 
xmin = 0+ d / 2.0
ymin = 0+ 3*d / 2.0
zmin = d / 2.0
# User input: List of the maximum x value (xmax), y value (ymax) and z value (zmax) for each of the GASCANS boundaries. In this example there are 4 boundaries. 
xmax = 0 + d / 2.0
ymax = h + d/2.0
zmax = 6.0 - d / 2.0
# User input: Name of the GASCANS boundaries. The names are used in the file name for each boundary. 
wall_name = f'LB_left{grid}_{h}H'

Nx = int((xmax - xmin) / d + 1.5)
Ny = int((ymax - ymin) / d + 1.5)
Nz = int((zmax - zmin) / d + 1.5)

fcoordname = "GASCANS_dos" + wall_name + ".txt"
real_name= "GASCANS" + wall_name + ".txt"

fcoord = open(fcoordname, "w")

for i in range(0,Nx):
		for j in range(0,Ny):
			for k in range(0,Nz):
				fcoord.write(str(xmin + i*d) + " " + str(ymin + j*d) + " " + str(zmin + k*d) + "\n")

fcoord.close()
# Function to convert DOS to UNIX format
def convert_dos_to_unix(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        content = infile.read()

    content_unix = content.replace('\r\n', '\n')

    with open(output_file, 'w', newline='\n') as outfile:
        outfile.write(content_unix)
            # Remove the original file
    os.remove(input_file)

# Convert the file to UNIX format
convert_dos_to_unix(fcoordname, real_name)


