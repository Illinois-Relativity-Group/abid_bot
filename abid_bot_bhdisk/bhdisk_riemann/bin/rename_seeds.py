from sys import argv

from os.path import isfile, join

from os import listdir, rename



root_dir = argv[1]

dt = float(argv[2])



seed_dir = root_dir + "seeds/"



if len(argv) == 4:

	print("renaming " + argv[3])

	seed_dir = root_dir + argv[3]



time_list = [ f[:-4] for f in listdir(seed_dir) if isfile(join(seed_dir, f)) and f.find(".txt") != -1 ]



def rename_file(f):

	t = str(int(round(float(f[:-2])/dt)))

	rename(seed_dir + f + ".txt", seed_dir + t.zfill(7) + "_{}.txt".format(f[-1]))



for f in time_list:

	rename_file(f)
