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

#thing to change for tilted case
is_tilted=0 #1 for tilted case in bhdisk
spinfile=root_dir+"h5data/bhns_BHspin.mon" #set this for tilded case
#auto generated parts:
spindata=[]
xmltimelist=[]

def binsearch(listu,target,begin=0,end=-1,tol=0.01):       #end excluded
    n=len(listu)
    if end==-1:
        end=n
    if end-begin<=0:
        #print("target %e not found" % target)
        return -1
    mid=int((begin+end)/2)
    if abs(listu[mid]-target)<tol:
        return mid
    elif listu[mid]>target:
        return binsearch(listu,target,begin,mid)
    else:
        return binsearch(listu,target,mid+1,end)

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

			r = 1.0 #0.008 for bhdisk?
			h = r*2.0
			m_steps = 20 #10 for bhdisk?
			
			if not is_tilted:
				for m in range(m_steps):
					theta = 2*pi*m/m_steps
					x = xc + r*cos(theta)
					y = yc + r*sin(theta)
					z = zc
					outfile.write(str(x) + "\t" + str(y) + "\t" + str(z+h) + "\n")
					outfile.write(str(x) + "\t" + str(y) + "\t" + str(z-h) + "\n")
			else:
				idx=binsearch(xmltimelist,time,tol=0.03)
				normvec=spindata[idx,1:]
				normvec /= np.linalg.norm(normvec)
				cenvec=[xc,yc,zc]
				pointvec=np.random.randn(3)
				pointvec -= pointvec.dot(normvec) * normvec
				pointvec /= np.linalg.norm(pointvec)

				steplen=2*pi*r/m_steps

				for m in range(m_steps+1):
					p1=cenvec+pointvec*r+normvec*h
					p2=cenvec+pointvec*r-normvec*h
					outfile.write(str(p1[0]) + "\t" + str(p1[1]) + "\t" + str(p1[2]) + "\n")
					outfile.write(str(p2[0]) + "\t" + str(p2[1]) + "\t" + str(p2[2]) + "\n")

					#calc next pointvec
					shiftvec=np.cross(normvec,pointvec)
					shiftvec=shiftvec/np.linalg.norm(shiftvec)*steplen
					pointvec+=shiftvec
					pointvec /= np.linalg.norm(pointvec)

############################################################################################################
print("removing old seeds...")
if isdir(bhseed_dir):
	rmtree(bhseed_dir)

makedirs(bhseed_dir)

# set up the timeList and cmList arrays from bhcen.txt
print("creating new seeds...")
if is_tilted:
	spindata=np.loadtxt(spinfile,comments=['#'])
	xmltimelist=spindata[:,0]

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
