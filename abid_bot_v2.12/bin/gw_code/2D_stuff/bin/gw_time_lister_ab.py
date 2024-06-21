from os import listdir
from os.path import isfile, join
from sys import argv


def gw_time_lister(a):
    ADM_mass = a.gw.M_ADM
    gw_dt = a.gw.gw_dt
    extraction_r = a.gw.(r_areal)
    gw_file_dir = a.gw.fol_name



$M_ADM $dt $r_areal $fol_name
gw_file_dir = 
ADM_mass = 
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
