from sys import argv
import os


v_file=argv[1]
direction=str(argv[2])
M=float(argv[3])
starttime=float(argv[4])
dt=float(argv[5])


t=-1
outfile=open(".tmp.txt", 'w')
with open(v_file, 'r') as infile:
	for line in infile:
		#print(len(line))
		#print(line[0])
		if (line=='\n' or ('#' in line)):
			continue
		data=line.strip().split()
		#print(data)
		#print(len(data))
		if (int(data[0])<starttime*M/dt):
			continue
		if (int(data[0])!=t):
			outfile.close()
			t= int(data[0])
			print(t)
			#t=int(int(data[0])*dt/M+ float(ini_time)/M)
			outname="vel_data_iter2/v"+direction+"."+str(t).zfill(6)+".txt"
			outfile=open(outname,'a')
		#print(checkset)
		outfile.write('\t'.join(data)+'\n')
		#print(data)
	outfile.close()



'''
print "changing names..."


def changing_name (dir):
	for file in os.listdir(dir):
		iter=file[3:-4]
		time=int((float(iter)*dt+float(ini_time))/M)
		path = os.path.join(dir,file)
		dst = path.replace(str(file[3:-4]),str(time))
		os.rename(path, dst)
	return

changing_name("vel_data")



directory = "vel_data"


for file in os.listdir(directory):
	iter=file[3:-4]
	time=int((float(iter)*dt+float(ini_time))/M)
       	path = os.path.join(directory,file)
       	dst = path.replace(str(file[3:-4]),str(time))
       	os.rename(path, dst)
'''

