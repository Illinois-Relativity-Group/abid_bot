from os import listdir
from sys import argv
from math import pi

# mode of computing period.
#####comp_omega_mode is useless now###
dt=float(argv[1])
comp_omega_mode = argv[2]
M= float(argv[3])
ini_time=float(argv[4])
start_time=float(argv[5])

w_files=[]
files_temp=listdir("w_data/")
for i in files_temp:
	if(i[0]!='w'):
		continue
	w_files.append(i)
w_files.sort()
print('w_file[0]:',w_files[0])
def calc_N():
	#N is number of files in a period
	#N=2pi/w(t=0, r=0)/(dtiterationsPerFile)
	print ("use period-computing mode 1")
	fil=open('w_data/'+w_files[0],'r')
	line=fil.readline()
	w=float(line.strip().split()[1])
	
	times=[int((float(i[2:-4])*M-ini_time)/dt) for i in w_files]
	print ('times',times)
	itStep=int(times[1])-int(times[0])
	print ("itstep: ",itStep)
	ret=int(2*pi/(w*dt*itStep)+1)
	print("N=",ret)
	return (ret)

N=calc_N()
#print(w_files)
#w_files is list of all files
while(len(w_files)>=N):#
	to_ave=w_files[:N]
	w_files=w_files[N:]
	print("Period Found")
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
	r_vals.sort()
	name=to_ave[int(N/2)][2:-4]
	for i in r_vals:
		data[i]/=N
	out_name="w_ave"+str(name)+".dat"
	outfile=open("t_ave/"+out_name, 'w')
	for i in r_vals:
		outfile.write(str(i)+'\t'+str(data[i])+'\n')
	outfile.close()
