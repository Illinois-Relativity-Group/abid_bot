from os import listdir
from os.path import isfile, join
from sys import argv

gw_file_dir = "gwdata/3D/"
ADM_mass = float(argv[1])
gw_dt = float(argv[2])
extraction_r = float(argv[3])
gw_time_file = "gwdata/gw_time_list.txt"

time_files = [f for f in listdir(gw_file_dir) if isfile(join(gw_file_dir,f)) and f.find("hcross") != -1 ]

fname = open(gw_time_file, "w+")

for i in range(len(time_files)):
	time_files[i]=int(round( (int(time_files[i][7:-4])*gw_dt - extraction_r) / ADM_mass))
	
time_files.sort()
for time in time_files:
	fname.write("{}\n".format(time))

fname.close()
