import numpy as np
from shutil import copy
from sys import argv

#This finds the particle data closest to each time we have data for and moves that file to a different folder.  Other files will be deleted
#Similiar to sifting black holes
root = argv[1]
t_start = float(argv[2])
dt = float(argv[3])
dat_file = root + "bin/particle_code/misc/files.txt"
dst = root + "bin/particle_code/misc/dat_shortened/"
dat = open(dat_file, 'r')


time_list = []
dict = {}
for line in dat:
	t = float(line[:-5])
	time_list.append(t)
	dict[t] = line[:-1]
dat.close()

time_array = np.asarray(time_list)
while t_start <= time_list[-1]:
	pos = (np.abs(time_array -  t_start)).argmin()
	dat_name = dict[time_array[pos]]
	copy(root + "bin/particle_code/misc/dat/" + dat_name, dst + dat_name)
	t_start += dt

	


	
	
	



