from os import listdir
from sys import argv
from math import pi

# mode of computing period.
#1. using initial omega file, this may not working if the initial file is not at t=0 (e.g. after regridding)
#2. using a self-defined omega to compute period. You need to input omega manually in the run.sh
dt = float(argv[1])
comp_omega_mode = argv[2]
M= float(argv[3])
ini_time=float(argv[4])
ini_omega = float(argv[5])
def calc_N():
	#N is number of files in a period
	#N=2pi/w(t=0, r=0)/(dtiterationsPerFile)
	if (comp_omega_mode=="1"):
		print ("use period-computing mode 1")
		fil=open("w_data/w_000000.txt",'r')
		line=fil.readline()
		w=float(line.strip().split()[1])
	else:
		print ("using period-computing mode 2")
		w = float(ini_omega)	
	dt=float(argv[1])
	files=listdir("w_data")
	#print ([ i[2:-4] for i in files])
	times=[int((float(i[2:-4])*M-ini_time)/dt) for i in files]
	times.sort(key=int)
	#print (times)
	itStep=int(times[1])-int(times[0])
	print (itStep)
	print(2*pi/w)
	ret=int(2*pi/(w*dt/2)+1)
	return (ret)

N=calc_N()
print(N)
w_files=[]
files_temp=listdir("w_data/")
for i in files_temp:
	if(i[0]!='w'):
		continue
	w_files.append(i)
w_files.sort()
#print(w_files)
#w_files is list of all files
while(len(w_files)>=N):#
	to_ave=w_files[:N]
	w_files=w_files[N:]
	#print("Period Found")
	data={}
	for i in to_ave:
		#print(i)
		fil=open("w_data/"+ i, 'r')
		for line in fil:
			lin=line.strip().split()
			r=lin[0]
			w=lin[1]
			if r in data:
				data[r]+=float(w)
			else:
				data[r]=float(w)
		fil.close()
	r_vals=[i for i in data]
	r_vals.sort(key=float)
	name=to_ave[int(N/2)][2:-4]
	for i in r_vals:
		data[i]/=N
	out_name="w_ave"+str(name)+".dat"
	outfile=open("t_ave/"+out_name, 'w')
	for i in r_vals:
		outfile.write(str(i)+'\t'+str(data[i])+'\n')
	outfile.close()
