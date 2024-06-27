# Writes the coordinates inside the defined cube in a text file in the format
# (x y z)
# (x y z)
# ...

# User input : cell size
d = 1.0/5.0
h=0.04
# User input : List of the minium x value ( xmin ), y value ( ymin ) and z value ( zmin ) for
xmin =20 + d / 2.0 +d -5#  20 + d / 2.0 
zmin = 0 + d / 2.0
ymin =  d / 2.0 
# User input : List of the maximum x value ( xmax ), y value ( ymax ) and z value ( zmax ) for
xmax =  40- d / 2.0 +5 #40- d / 2.0 
zmax = d*7- d / 2.0 
ymax =  6.0 - d / 2.0 
# User input : Name of the GASCANS boundaries . The names are used in the file name for
wall_name ='LB_bottom '

Nx = int (( xmax - xmin) / d + 1.5)
Ny = int (( zmax - zmin) / d + 1.5)
Nz = int (( ymax - ymin) / d + 1.5)
print(f"Dataset  NY= {Ny}  Nx= {Nx} ")

fname = " sampleDictCoord " + wall_name
f = open ( fname , "w")

for i in range (0 , Nx ) : 
    if i <= (Nx/2)-2.5/d +1 or i >= (Nx/2)+2.5/d -3: 
        st = int (Ny/2)+1 -2 +3
     #   print(f"Dataset st={st}, NY= {Ny} ")
        for j in range (0 , st ) :
                for k in range (0 , Nz ) :
                    f.write ("( " + str ( h*(xmin  + i*d)) + " " + str (h*(ymin  + k*d) )+ " " +  str( h*(zmin + j *d))  + " )\n")         

# File to append
curve_file = "curve_extended.pc"
with open(fname, "a") as f:
    with open(curve_file, "r") as curve_f:
        for line in curve_f:
            # Split the line into coordinates
            coords = line.strip().split()
            # Exchange column 2 and 3 (indexing from 0)
            coords[1], coords[2] = coords[2], coords[1]
            # Write the modified line to fname
            f.write("( " + " ".join(coords) + " )\n")

f.close ()
