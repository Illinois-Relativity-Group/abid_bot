import sys
from sys import argv
import random
import csv
from os import listdir
from os.path import isfile, join
import shutil

##### parameters ##### TODO:
gw_dt = float(argv[1]) #t1-t0 in 1D
ADM_mass = float(argv[2])
root = argv[3]

# input #############################################################
inputdir = root + "/gwdata/3D/"
savedir = root + "/gwdata/less_3D/"
Timefile = root + "/gwdata/time_list.txt"
logtime = root + "/gwdata/logtime.txt"

#print("Preparing 3D files")
# get the time number of each file ########################################
hcrossfiles = [f for f in listdir(inputdir) if isfile(join(inputdir,f)) and f.find("hcross") != -1 ]
hplusfiles = [f for f in listdir(inputdir) if isfile(join(inputdir,f)) and f.find("hplus") != -1 ]

for i in range(len(hcrossfiles)):
	hcrossfiles[i]=int(hcrossfiles[i][7:-4])

for i in range(len(hplusfiles)):
	hplusfiles[i]=int(hplusfiles[i][6:-4])

hcrossfiles.sort()
hplusfiles.sort()

# get the time number needed ##############################################

timefile = open(Timefile,"r")
time_list = []
for line in timefile:

	line_str = line.split()
	line_time = int(line_str[0])
	time_list.append(line_time)

time_list.sort()

timefile.close()

record_list = []

time_record_list = []

print("Finding corresponding files from time_list.txt and copying to less_3D/...")

#logfile = open("log.txt","w")
log_time = open(logtime,"w")
count = 0
for i in range(len(hcrossfiles)):
	tindex = int(hcrossfiles[i])
	tcur = int(round(hcrossfiles[i]*gw_dt/ADM_mass))
	'''tindex = int(hplusfiles[i])
	tcur = int(round(hplusfiles[i] *gw_dt/ADM_mass))'''
	cross_dst = savedir + "hcross_" + str(tindex) +".vtk"
	cross_src = inputdir + "hcross_" + str(tindex) + ".vtk"

	plus_dst = savedir + "hplus_" + str(tindex)+".vtk"
	plus_src = inputdir + "hplus_" + str(tindex) + ".vtk"
	#print("time = %g" % int(tcur))
	#print("frame = " + str(tindex))
	if (tcur in time_list):
		if tcur not in time_record_list:
			shutil.copy2(cross_src,cross_dst)
			
			#logfile.write( "hcross_" + str(tindex) + " is copied" +"\n")
			
			shutil.copy2(plus_src,plus_dst)
			
			#logfile.write( "hplus_" + str(tindex) + " is copied" + "\n")
			
			time_record_list.append(tcur)
			record_list.append(tindex)

			log_time.write(str(tindex)+"\n")
			count = count + 1			

			if count >=50 and count % int(50) == 0 :
				number = int(count)
				print("\t " + str(int(number))+" hcross and hplus files have been copied")


record_list.sort()
totalnumber = len(record_list) *2
#logfile.write( "copied \t" + str(totalnumber) + " total files" + "\n")
#logfile.write( "copied \t" + str(len(record_list)) + " files for each kind" + "\n")
print("Done copying to less_3D/ \n")
print("Times copied from 3D/")
print(record_list)
print("\t length is " + str(len(record_list)) + "\n")

print("List of times in t/M")
print(time_list)
print("\t length is " + str(len(time_list)) + "\n")

print("Setup complete!")
#logfile.close()

log_time.close()







