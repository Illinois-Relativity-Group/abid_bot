import numpy as np
import sys
import shutil
import os
from os import listdir
from os.path import isfile
from os.path import join
from gwbot import gw

rootdir = sys.argv[1]
M = float(sys.argv[2])
gwtype = int(sys.argv[3])
gwHflag = int(sys.argv[4])
gw_dt = gw.gw_dt
r_areal = gw.r_areal
rootdir = rootdir if rootdir[-1] == '/' else rootdir + '/'

GWdir = rootdir + "bin/gw_code/VTKdata/" + "2D/" if gwtype == 0 else rootdir + "bin/gw_code/VTKdata/" + "3D/" 
print(GWdir)
fols = []
#past_merger = False
for fol in sorted(os.listdir(rootdir + "xml/")):
	#if fol == merger_fol:
		#past_merger = True
	#if past_merger:
		#fols.append(fol)
	fols.append(fol)

hcrossfiles = []
hplusfiles = []

tempdir = GWdir

print("Renaming and sorting hplus and hcross files")

for dir in listdir(GWdir):
	GWdir += dir + '/'
	hcross = [join(GWdir,f) for f in listdir(GWdir) if isfile(join(GWdir,f)) and f.find("hcross") != -1 ]
	hplus = [join(GWdir,f) for f in listdir(GWdir) if isfile(join(GWdir,f)) and f.find("hplus") != -1 ]
	GWdir = tempdir
	hcrossfiles.extend(hcross)
	hplusfiles.extend(hplus)
hcrossfiles.sort()
hplusfiles.sort()

hcrosstimes = []
hplustimes = []

if gwHflag:

	for i in range(len(hcrossfiles)):
		index = hcrossfiles[i].find("hcross")
		file = hcrossfiles[i][index:]
		time = int(round(int(file[7:-4])*gw_dt/M))
		hcrosstimes.append(int(time - r_areal))
		hcrosstimes.sort()
		
	hcrosstimes = np.array(hcrosstimes)
	print("Moving hcross files into xml directories")
	for fol in fols:
		timelist=[file for file in os.listdir(rootdir + "xml/" + fol) if file.startswith("time_")]
		timelist.sort()
		timelist = [float(time[5:-4]) for time in timelist]
		index = 0
		for i in range(0,len(timelist)):
			closestIndex = np.argmin(np.abs(hcrosstimes - timelist[i]))
			src = hcrossfiles[closestIndex]
			#dst = rootdir + "xml/" + fol + "/hcross_ret_tM_{}_".format(timelist[i]) + str(index).zfill(4) + ".vtk"
			dst = rootdir + "xml/" + fol + "/hcross_" + str(index).zfill(4) + ".vtk"
			os.symlink(src, dst)
			index += 1
			if len(timelist) == 1:
				path = rootdir + "xml/" + fol + "/hcross_0001.vtk"
				shutil.copy(dst, path)
else:	
		
	for i in range(len(hplusfiles)):
		index = hplusfiles[i].find("hplus")
		file = hplusfiles[i][index:]
		time = int(round(int(file[6:-4])*gw_dt/M))
		hplustimes.append(int(time - r_areal))
		hplustimes.sort()

	hplustimes = np.array(hplustimes)
	print("Moving hplus files into xml directories")
	for fol in fols:
		timelist=[file for file in os.listdir(rootdir + "xml/" + fol) if file.startswith("time_")]
		timelist.sort()
		timelist = [float(time[5:-4]) for time in timelist]
		index = 0
		for i in range(0,len(timelist)):
			closestIndex = np.argmin(np.abs(hplustimes - timelist[i]))
			src = hplusfiles[closestIndex]
			#dst = rootdir + "xml/" + fol + "/hplus_ret_tM_{}_".format(timelist[i])  + str(index).zfill(4) + ".vtk"
			dst = rootdir + "xml/" + fol + "/hplus_" + str(index).zfill(4) + ".vtk"
			os.symlink(src, dst)
			index += 1
			if len(timelist) == 1:
				path = rootdir + "xml/" + fol + "/hplus_0001.vtk"
				shutil.copy(dst, path)


