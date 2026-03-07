# This sifts the gp files so that only times that are a multiple of the iteration scheme are in the horizon folder

from shutil import copy
from os.path import isfile, join
from os import listdir
from sys import argv
import numpy as np
#######################################################################
horizon_dir = argv[1]
iter = int(argv[2])
ahtype = argv[3]
#######################################################################

all_dir = horizon_dir + "all_horizon/"
time_list = [ int(f[3:-7]) for f in listdir(all_dir) if isfile(join(all_dir,f)) and\
	      f.find("h.t")  != -1  and f.find(".ah" + ahtype + ".gp") != -1 ]
min_time, max_time = float(min(time_list)), float(max(time_list))
first_time, last_time = int(round(min_time/iter,0)*iter), int(round(max_time/iter,0)*iter)


for time in range(first_time, last_time+iter, iter):
	np_times     = np.array(time_list)
	closest_idx  = np.abs(np_times - time).argmin()
	closest_time = int(np_times[closest_idx])
	gp_file_all  = "h.t" + str(closest_time) + ".ah" + ahtype + ".gp"
	gp_file_iter = "h.t" + str(time) 	 + ".ah" + ahtype + ".gp"
	copy(join(all_dir,gp_file_all), join(horizon_dir, gp_file_iter))
	#print("Old time: {}; New time: {}".format(closest_time, time))




def copy_gp(time):
	gp_file = "h.t" + time + ".ah" + ahtype + ".gp"
	if int(time) % iteration == 0:
		if isfile(join(all_dir, gp_file)):
			copy(join(all_dir,gp_file), join(horizon_dir, gp_file))
		else:
			print("WARNING: missing gp file for it ={}".format(time))

#map(copy_gp, time_list)
