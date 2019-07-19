#Use this on your local machine to find particles easily
import numpy as np
from math import sqrt, sin, cos, pi
lines = []


particleFile = "00254.51505379000.dat"
particleFile2 = "00343.96576405000.dat"
outfile = "BHNSseeds.txt"

AllPoints = np.loadtxt(particleFile)

def dist(a,b):
	ret = 0;
	for x,y in zip(a,b):
		ret += (x-y)**2
	return sqrt(ret)

def nearest(x):
	minDist = 100
	minPoint = [0,0,0]
	minIdx = -1
	for i in range(AllPoints.shape[0]):
		newDist = dist(x,AllPoints[i,1:4])
		if newDist < minDist: minDist = newDist; minPoint = AllPoints[i,1:4]; minIdx = i
	lines.append(minIdx)
	return minPoint

zs=[0.40, 0.55]
rs=[0.55, 0.30]
xc=2.56128 #2.680
yc=0.38982 #0.412

with open(outfile, 'w') as out:
	for i in range(10):
		theta = 2*pi*i/10
		for r,z in zip(rs,zs):
			seed = [xc+r*cos(theta), yc+r*sin(theta), z]
			particle = nearest(seed)
			out.write("{}\t{}\t{}\n".format(particle[0],particle[1], particle[2]))
			out.write("{}\t{}\t{}\n".format(particle[0],particle[1],-particle[2]))
lines = list(set(lines))
lines.sort()
print("Found {} lines".format(len(lines)))
print(lines)
