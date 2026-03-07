import numpy as np
from plotter import *
from h5loader import *
from diagnostics import *
from sys import argv

import matplotlib
matplotlib.use('Agg')
import pylab as plt
from gridder import *
np.seterr(divide='ignore', invalid='ignore')

root = "/home1/07525/tg868241/stbrmt_abid/plotting_tool/" 
h5dir = "/scratch1/07525/tg868241/stbrmt_abid/h5data/"

with open(root + "bin/iters.txt") as f:
	list=f.readlines()

list=[h5dir+x.strip() for x in list]

#for i in list:
#	print(i)

#dit = 384

rl = range(9)
MPI = 128
#rho_code = 3.540501235210654e-4
#rho = 1.356e-3
#rho_max = 2.7e-2
#M_ADM = 2.6
savefolder = root + "plots/"

f=open(savefolder+"avgb2rho"+str(argv[1])+".txt","w+")

for i in range(int(argv[1]),int(argv[2])):	#590
	h5folder=list[i].split(", ")[0]+"/"
	it=list[i].split(", ")[1]
	print(h5folder)
	
		#time, avg=calc_b2_over_2rho(h5folder,it,rl,MPI)
	x_list = np.linspace(0,0,1)
	y_list = np.linspace(0,0,1)
	z_list = np.linspace(0.0, 20.0, 40)
	try:
		density, time = make_xyz_grid(h5folder, "rho_b", it, rl, MPI, x_list,y_list, z_list)
		for i in density:
			print(i)
	except:
		print("error data at "+str(it)+",in "+h5folder+"\n")
	#else:
		#f.write(str(it)+"\t"+str(time)+"\t"+str(avg)+"\n")
	
f.close()
#it = 340992


#plot_T_xy(h5dir, it, rl, MPI, rho_code, rho, M_ADM, savefolder)
#plot_rho_xy(h5dir, it, rl, MPI, rho_max, M_ADM, savefolder, False, 0, 0.5)
#D = Dataset(h5dir, "rho_b", it, 4, MPI)








