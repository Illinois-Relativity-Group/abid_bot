import numpy as np
from scipy.special import factorial as fact
from sys import argv
import os
import time
from hphc_module import *
from hphc_test_module import *


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
def setup_gw(gw):
    start_TOT = time.time()

    gw.threeD = False; gw.twoD = False
    if gw.threeD_flag == 1: 
        gw.threeD = True
    elif gw.threeD_flag == 0: 
        gw.twoD = True
    elif gw.threeD_flag == 2:
        gw.twoD = True; gw.threeD = True

    # create grid: 3D
    gw.xs_3D, gw.sx_3D = np.linspace(-gw.xy_max_3D, gw.xy_max_3D, num=gw.xy_num_3D, retstep=True)  #from low to high
    gw.ys_3D, gw.sy_3D = np.linspace(-gw.xy_max_3D, gw.xy_max_3D, num=gw.xy_num_3D, retstep=True)
    gw.zs_3D, gw.sz_3D = np.linspace(gw.z_min_3D, gw.z_max_3D, num=gw.z_num_3D, retstep=True)
    # create grid: 2D
    gw.xs_2D, gw.sx_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=gw.xy_num_2D, retstep=True)
    gw.ys_2D, gw.sy_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=gw.xy_num_2D, retstep=True)
     
    if gw.update_lookup == True: #this is slow for a fine grid, also just slow, np-ize it maybe
        if gw.threeD == True:
            gw.ylm_3D, gw.r_3D = get_lookup_3D(gw)
            np.savetxt(gw.bin_dir + "/ylm_lookup_3D.txt", gw.ylm_3D.reshape(gw.ylm_3D.shape[0], -1))
            np.savetxt(gw.bin_dir + "/r_lookup_3D.txt", gw.r_3D.reshape(gw.r_3D.shape[0], -1))
        if gw.twoD == True:
            gw.ylm_2D, gw.r_2D = get_lookup_2D(gw)
            np.savetxt(gw.bin_dir + "/ylm_lookup_2D.txt", gw.ylm_2D.reshape(gw.ylm_2D.shape[0], -1))
            np.savetxt(gw.bin_dir + "/r_lookup_2D.txt", gw.r_2D.reshape(gw.r_2D.shape[0], -1))
    else:
        if gw.threeD:
            gw.ylm_3D = np.loadtxt(gw.bin_dir + "/ylm_lookup_3D.txt", dtype=complex).reshape(len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D), gw.num_modes)
            gw.r_3D = np.loadtxt(gw.bin_dir + "/r_lookup_3D.txt", dtype=float).reshape(len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D))
        if gw.twoD:
            gw.ylm_2D = np.loadtxt(gw.bin_dir + "/ylm_lookup_2D.txt", dtype=complex).reshape(len(gw.xs_2D), len(gw.ys_2D), gw.num_modes)
            gw.r_2D = np.loadtxt(gw.bin_dir + "/r_lookup_2D.txt", dtype=float).reshape(len(gw.xs_2D), len(gw.ys_2D))

    if gw.threeD == False:
        gw.ylm_3D = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D), gw.num_modes)); gw.r_3D = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D)))
    if gw.twoD == False:
        gw.ylm_2D = np.zeros((len(gw.xs_2D), len(gw.ys_2D), gw.num_modes)); gw.r_2D = np.zeros((len(gw.xs_2D), len(gw.ys_2D)))
    print("done with lookup business")

    if gw.test_flag == 1: 
        if gw.threeD:
            write_vtk_test_3D(gw)
        if gw.twoD:
            print("writing 2D_test")
            write_vtk_test_2D(gw)
    else:
        # load, reshape, and prepare clm array 
        print("going dark")
        gw.clm_file = gw.fol_name + "/Clm"
        gw.clm_f = np.loadtxt(gw.clm_file, dtype=float)
        gw.clm_f_reshape = np.reshape(gw.clm_f, (gw.num_times, gw.num_modes, 2))
        gw.clm_f_reshape[:int(gw.r_areal/gw.gw_dt), :, :] = 0 

        gw.clm = gw.clm_f_reshape[:,:,0] + gw.clm_f_reshape[:,:,1]*1j
        np.savetxt(gw.fol_name + "/Clm_1D.txt",  np.einsum('ijk->ik', gw.clm_f_reshape)  )
        gen_data(gw)
    end_TOT = time.time()
    print("python done, time taken: " + str(end_TOT - start_TOT))
