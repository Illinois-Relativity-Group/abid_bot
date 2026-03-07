#This code extends data in all the files listed in filesOrigin.txt
#TODO change dst to a folder you want to place your new dat files.
#com.txt is a file containing the center of mass of the sytem at all times.
from os import makedirs
from os.path import basename, isdir
import os
from shutil import rmtree
import numpy as np
from sys import argv

root = argv[1]
misc_dir = root + "bin/particle_code/misc/"

dst = misc_dir + "extended/"
if isdir(dst):
	rmtree(dst)
makedirs(dst)
os.system('chmod 770 {}'.format(dst))
	
cmFile = open(root + "h5data/bhns.xon", 'r')
cmFile.readline()

timeList = []
cmList = []
for line in cmFile:
	data = line.split()

	t = float(data[0])
	x = (float(data[1]) + float(data[3]))/2
	y = (float(data[2]) + float(data[4]))/2
	z = 0.0

	timeList.append(t)
	cmList.append( [x, y, z] )
cmFile.close()

datList = open(misc_dir + "files.txt", 'r')
for line in datList:
	line = line[:-1]
	fileName = basename(line)
	myTime = fileName[:-4]
	myTime = float(myTime)

	timeArray = np.asarray(timeList)
	pos = (np.abs(timeArray -  myTime)).argmin()

	xc = cmList[pos][0]
	yc = cmList[pos][1]
	zc = cmList[pos][2]
	
	datFile = open(misc_dir + "dat/" + line, 'r')
	datNewFile = open(dst + fileName, 'w')
	for datLine in datFile:
		dat = datLine.split()
		t = float(dat[0])
		x = float(dat[1])
		y = float(dat[2])
		z = float(dat[3])
		u = float(dat[4])

		ti = t
		xi = 2*xc - x
		yi = 2*yc - y
		zi = z
		ui = u
		
		l1 = str(t) + "\t" + str(x) + "\t" + str(y) + "\t" + str(z) + "\t" + str(u) + "\n"
		l2 = str(ti) + "\t" + str(xi) + "\t" + str(yi) + "\t" + str(zi) + "\t" + str(ui) + "\n"
		datNewFile.write(l1)
		datNewFile.write(l2)
	datNewFile.close()
	datFile.close()
	
	timeList = timeList[pos:]
	cmList = cmList[pos:]
datList.close()
