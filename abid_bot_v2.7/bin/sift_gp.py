# This sifts the gp files so that only times that are a multiple of the iteration scheme are in the horizon folder

from shutil import copy
from os.path import isfile, join
from os import listdir
from sys import argv

#######################################################################
horizon_dir = argv[1]
iteration = int(argv[2])
ahtype = argv[3]
#######################################################################

all_dir = horizon_dir + "all_horizon/"
time_list = [ f[3:-7] for f in listdir(all_dir) if isfile(join(all_dir,f)) and f.find("h.t")  != -1  and f.find(".ah" + ahtype + ".gp") != -1]

def copy_gp(time):
	gp_file = "h.t" + time + ".ah" + ahtype + ".gp"
	if int(time) % iteration == 0:
		if isfile(join(all_dir, gp_file)):
			copy(join(all_dir,gp_file), join(horizon_dir, gp_file))
		else:
			print("WARNING: missing gp file for it ={}".format(time))

map(copy_gp, time_list)
