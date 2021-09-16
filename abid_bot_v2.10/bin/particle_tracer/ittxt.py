import h5py
import os
import numpy as np
from h5loader import *

append=0			#If adding new data
old_file="iters.txt.backup"	#Used when append
root="/home1/07525/tg868241/bhdisk_45/h5data"	#root of h5data folder. W/o trailing /
outfile="iters.txt"
rmdupes=0	#NOT suggested to use here. Takes too long. Run inside ptctracer.
rlmax=12	#Used when rmdupes
MPI=128		#Used when rmdupes

outy=open(outfile,"w")
bigtimelist=[]
old_list=np.zeros((1,2))

if append:
	print("Append is on")
	old_list=np.genfromtxt(old_file, dtype='str', delimiter=", ")

for filename in os.listdir(root):
	if append and filename <= old_list[-1,0]:
		continue
	timelist=[]
	#print(filename)
	if filename.startswith("3d_data_") and os.path.isdir(root+"/"+filename):
		#print("here")
		#guy=root+"/"+filename+"By.file_0.h5"
		#print(guy)
		f=h5py.File(root+"/"+filename+"/By.file_0.h5")
		for chunk in list(f.keys()):
			#print(chunk)
			it=chunk.split()[1][3:]
			#print(it)
			if it=="":
				continue
			if int(it) not in timelist:	
				#print("append")
				timelist.append(int(it))
		#timelist.sort()
		for time in timelist:
			#outy.write(filename+ ", "+str(time))
			bigtimelist.append((filename, time))
bigtimelist.sort(key=lambda x: (x[1],x[0]))

dt=99999999
for i in range(0, min(20,len(bigtimelist))-1):
	dt_t=int(bigtimelist[i+1][1])-int(bigtimelist[i][1])
	if dt_t>0: dt=min(dt,dt_t)

print(dt)

#DONT use. If you want to use rmdupes here modify according to your purpose.
if rmdupes:
	i=len(bigtimelist)-1
	t=-1
	while i>=0:
		print("rmdupes:%d" %(i))
		try:
			print(bigtimelist[i])
			D = Dataset(root+"/"+bigtimelist[i][0]+"/", "vx", bigtimelist[i][1], rlmax, MPI)
		except:
			bigtimelist.pop(i)
		#t=bigtimelist[i][1]
		i=i-1

#gap check
for i in range(len(bigtimelist)-1):
	#print("checkh5:%d" %(i))
	if int(bigtimelist[i+1][1])-int(bigtimelist[i][1])!=dt:
		print("gap incorrect: %d: %s  %s" %(i,bigtimelist[i][0],bigtimelist[i+1][0]))

if append and len(bigtimelist):
	bigtimelist=np.concatenate((old_list,bigtimelist))
elif append:
	print("No new data found")
	bigtimelist=old_list
for i in bigtimelist:
	outy.write(i[0]+ ", "+str(i[1])+"\n")	
outy.close()	
		

