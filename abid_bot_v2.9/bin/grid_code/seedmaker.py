from math import pi, cos, sin
from os.path import isfile, isdir, basename
from os import makedirs
from shutil import rmtree
from bisect import bisect_left
import numpy as np
from sys import argv

root_dir = argv[1]
dt = float(argv[2])
ahtype = argv[3]
numBfieldPlots = int(argv[4])

grid_code_dir = root_dir + "bin/grid_code/"
bhseed_dir = grid_code_dir + "bhseeds/" 

def make_seed_file(coord):

	time = coord[0]
	xc = coord[1]
	yc = coord[2]
	zc = coord[3]
	fName = str(int(round(time/dt)))
	for i in range(numBfieldPlots):
		with open(bhseed_dir + fName.zfill(7) + "_{}.txt".format(i), 'w') as outfile:

############################################THING TO CHANGE###################################################
# Here you have the ability to modify where the ring of points are going to be above and below the black hole. 
# This section is the only place you should change anything. 

			r = 1.0
			h = r*2.0
			m_steps = 20
			for m in range(m_steps):
				theta = 2*pi*m/m_steps
				x = xc + r*cos(theta)
				y = yc + r*sin(theta)
				z = zc
				outfile.write(str(x) + "\t" + str(y) + "\t" + str(z+h) + "\n")
				outfile.write(str(x) + "\t" + str(y) + "\t" + str(z-h) + "\n")
############################################################################################################
print("removing old seeds...")
if isdir(bhseed_dir):
	rmtree(bhseed_dir)

makedirs(bhseed_dir)

# set up the timeList and cmList arrays from bhcen.txt
print("creating new seeds...")
with open(grid_code_dir + "bhcen" + ahtype + ".txt", 'r') as f:
	coordList = []
	for line in f:
		data = line.split()
		t = float(data[0])
		x = float(data[1])
		y = float(data[2])
		z = float(data[3])

		coordList.append( (t, x, y, z) )

# write seed files 
for coord in coordList:
	make_seed_file(coord)
