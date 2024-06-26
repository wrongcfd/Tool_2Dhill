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
    # for j in range(0,Ny):
	#     for k in range(0,Nz):
    #               f.write ("( " + str ( h*(xmin + i*d)) + " " + str (h*(ymin+ k*d) )+ " " +  str( h*(zmin+ j *d))  + " )\n")     
    if i < (Nx/2)-2.5/d or i >= (Nx/2)+2.5/d -1: 
        st = int (Ny/2)+1 -1 -1
     #   print(f"Dataset st={st}, NY= {Ny} ")
        for j in range (1 , st ) :
                for k in range (0 , Nz ) :
                    f.write ("( " + str ( h*(xmin  + i*d)) + " " + str (h*(ymin  + k*d) )+ " " +  str( h*(zmin + j *d))  + " )\n") 
    else:
        for j in range (1 , Ny ) :
                for k in range (0 , Nz ) :
                    # print(f"Dataset st={st}, NY= {Ny} ")
                    f.write ("( " + str ( h*(xmin + i*d)) + " " + str (h*(ymin+ k*d) )+ " " +  str(h*(zmin + j *d) ) + " )\n")            
f.close ()
