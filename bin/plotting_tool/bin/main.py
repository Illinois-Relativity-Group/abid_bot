import numpy as np
from plotter import *
from h5loader import *
from diagnostics import *
from sys import argv


'''
rho_max = 0.000354050123521
#rho_max = 0.0000726893218551901

rank = int(argv[1])
frames_per_rank = 10

out_freq = 512
MPI = 48
M_ADM = 1.0
list_txt = "/u/sciteam/skhan/scratch/BHBH_disk/plotting_tool/bin/list_sorted.txt"
savefolder = '/u/sciteam/skhan/scratch/BHBH_disk/plotting_tool/plots/'
cm_txt = "/u/sciteam/skhan/scratch/BHBH_disk/plotting_tool/bin/cm.txt"

it_start = rank*frames_per_rank*out_freq
it_end   = it_start + frames_per_rank*out_freq

rl = range(9)
for i in range(frames_per_rank):
	it = (frames_per_rank*rank + i)*out_freq
	try:
		print ""
		h5dir = get_h5folder(list_txt, it)
		print it, h5dir
		#plot_b2_over_2rho(h5dir, it, rl, MPI, M_ADM, savefolder)
		plot_rho_xy(h5dir, it, rl, MPI, rho_max, M_ADM, savefolder)
		print "done"
		print ""
	except:
		print ""
		print "error with it=", it
		print ""

it_list = [373760, 374272, 374784, 375296]
rl_list = range(8)
h5dir = "/home/abid/Dropbox/dump/smallb2/"
MPI = 48
out_freq = 512
M_ADM = 0.99
savefolder = "/home/abid/Desktop/"
#calculate_total_mass(it, rl_list, h5dir, MPI, out_freq)
for it in it_list:
	plot_b2(h5dir, it, rl_list, MPI, M_ADM, savefolder)
'''
h5dir = "/scratch1/07525/tg868241/stbrmt_abid/h5data/3d_data_201912191260/"
#h5dir = "/home/abid/17_08_26_155927/"
it = 226560
#it = 340992
rl = range(8)
MPI = 48
rho_code = 3.540501235210654e-4
rho = 1.356e-3
rho_max = 1.356e-3
M_ADM = 2.6
savefolder = "/scratch1/07525/tg868241/stbrmt_abid/plotting_tool/plots/"

#plot_T_xy(h5dir, it, rl, MPI, rho_code, rho, M_ADM, savefolder)
plot_rho_xy(h5dir, it, rl, MPI, rho_max, M_ADM, savefolder, False, 0, 0.5)
#D = Dataset(h5dir, "rho_b", it, 4, MPI)








