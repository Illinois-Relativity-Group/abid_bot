import numpy as np
from scipy.special import factorial as fact
from sys import argv
import os
import time
from hphc_module import *


#NOTES ON IMPLMENETATION
#
# write a function that applies the radial time retardation
#   such that r = 0 is the time from the original Psi4 file
#   and for greater r, the time is 'time - r'
# general time retardation
#   the time at r = 0 is the time from the source minus the extraction radius of the Psi4 file
#
# once you have a set of hc and hp at times of the Psi4 file, with time retardation within the grid taken into account
#   have a function that finds the correct hp or hc .vtk file for a given time in the source movie (this step can account for general time retardation)
#   then you can make a list of the .vtk files that correspond to each frame in the source movie
#   and can launch a job to combine the two plots
#   the .vtk file may have to be 'down sized' so that the source's size is exagerrated in the final movie
#
#
# instead of shifting, just gen the .vtk files like old script does, and then rename / move them to match up with source movie

# AbidBot a
def setup_gw(a):
    start_TOT = time.time()

    a.gw.threeD = False; a.gw.twoD = False
    if a.gw.threeD_flag == 1: 
        a.gw.threeD = True
    elif a.gw.threeD_flag == 0: 
        a.gw.twoD = True
    elif a.gw.threeD_flag == 2:
        a.gw.twoD = True; a.gw.threeD = True

    # create grid: 3D
    a.gw.xs_3D, a.gw.sx_3D = np.linspace(-a.gw.xy_max_3D, a.gw.xy_max_3D, num=a.gw.xy_num_3D, retstep=True)  #from low to high
    a.gw.ys_3D, a.gw.sy_3D = np.linspace(-a.gw.xy_max_3D, a.gw.xy_max_3D, num=a.gw.xy_num_3D, retstep=True)
    a.gw.zs_3D, a.gw.sz_3D = np.linspace(a.gw.z_min_3D, a.gw.z_max_3D, num=a.gw.z_num_3D, retstep=True)
    # create grid: 2D
    a.gw.xs_2D, a.gw.sx_2D = np.linspace(-a.gw.xy_max_2D, a.gw.xy_max_2D, num=a.gw.xy_num_2D, retstep=True)
    a.gw.ys_2D, a.gw.sy_2D = np.linspace(-a.gw.xy_max_2D, a.gw.xy_max_2D, num=a.gw.xy_num_2D, retstep=True)
     
    if a.gw.update_lookup == True: #this is slow for a fine grid, also just slow, np-ize it maybe
        if a.gw.threeD == True:
            a.gw.ylm_3D, a.gw.r_3D = get_lookup_3D(a)
            np.savetxt(a.gw.bin_dir + "/ylm_lookup_3D.txt", a.gw.ylm_3D.reshape(a.gw.ylm_3D.shape[0], -1))
            np.savetxt(a.gw.bin_dir + "/r_lookup_3D.txt", a.gw.r_3D.reshape(a.gw.r_3D.shape[0], -1))
        if a.gw.twoD == True:
            a.gw.ylm_2D, a.gw.r_2D = get_lookup_2D(a)
            np.savetxt(a.gw.bin_dir + "/ylm_lookup_2D.txt", a.gw.ylm_2D.reshape(a.gw.ylm_2D.shape[0], -1))
            np.savetxt(a.gw.bin_dir + "/r_lookup_2D.txt", a.gw.r_2D.reshape(a.gw.r_2D.shape[0], -1))
    else:
        if a.gw.threeD:
            a.gw.ylm_3D = np.loadtxt(a.gw.bin_dir + "/ylm_lookup_3D.txt", dtype=complex).reshape(len(a.gw.xs_3D), len(a.gw.ys_3D), len(a.gw.zs_3D), a.gw.num_modes)
            a.gw.r_3D = np.loadtxt(a.gw.bin_dir + "/r_lookup_3D.txt", dtype=float).reshape(len(a.gw.xs_3D), len(a.gw.ys_3D), len(a.gw.zs_3D))
        if a.gw.twoD:
            a.gw.ylm_2D = np.loadtxt(a.gw.bin_dir + "/ylm_lookup_2D.txt", dtype=complex).reshape(len(a.gw.xs_2D), len(a.gw.ys_2D), a.gw.num_modes)
            a.gw.r_2D = np.loadtxt(a.gw.bin_dir + "/r_lookup_2D.txt", dtype=float).reshape(len(a.gw.xs_2D), len(a.gw.ys_2D))

    if a.gw.threeD == False:
        a.gw.ylm_3D = np.zeros((len(a.gw.xs_3D), len(a.gw.ys_3D), len(a.gw.zs_3D), a.gw.num_modes)); a.gw.r_3D = np.zeros((len(a.gw.xs_3D), len(a.gw.ys_3D), len(a.gw.zs_3D)))
    if a.gw.twoD == False:
        a.gw.ylm_2D = np.zeros((len(a.gw.xs_2D), len(a.gw.ys_2D), a.gw.num_modes)); a.gw.r_2D = np.zeros((len(a.gw.xs_2D), len(a.gw.ys_2D)))
    print("done with lookup business")

    if a.gw.test_flag == 1: 
        if a.gw.threeD:
            write_vtk_test_3D(a)
        if a.gw.twoD:
            print("writing 2D_test")
            write_vtk_test_2D(a)
    else:
        # load, reshape, and prepare clm array 
        print(a.gw.ylm_3D.shape); print(a.gw.r_2D.shape)
        print(a.gw.num_modes)
        print("going dark")
        a.gw.clm_file = a.gw.fol_name + "/Clm"
        a.gw.clm_f = np.loadtxt(a.gw.clm_file, dtype=float)
        a.gw.clm_f_reshape = np.reshape(a.gw.clm_f, (a.gw.num_times, a.gw.num_modes, 2))
        a.gw.clm = a.gw.clm_f_reshape[:,:,0] + a.gw.clm_f_reshape[:,:,1]*1j
        gen_data(a)
    end_TOT = time.time()
    print("python done, time taken: " + str(end_TOT - start_TOT))
