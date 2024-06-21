import os
import subprocess
from math import pi
# written by eric may '23


# # # for python part
# # # don't end with slash (though i don't think it matters)
root = "/anvil/scratch/x-rnarasimhan/gw_bot/2D_stuff"
test_flag = False    #boolean 0 (false) or 1 (true) (regular run or test source run)
update_lookup =  False   #boolean 0 or 1   only need to update if you change resolution or num modes

# # # START PARAMETERS FOR PSI4 PROCESSING # # #
psi4_dir = "/anvil/scratch/x-rnarasimhan/gw_bot/Psi4_dir_q1"   #folder containing Psi4_rad.mon.#
psi4_num = 3  # the last number # in Psi4_ad.mon.#, corresponds to extraction radius
#M_ADM=0.064923059    #same as M in params
M_ADM = 1.0
cutoff_w = 0.27        # has to be lower than the fundamental freq of gw radiation, ask someone else for this
files_per_folder = 25  #files per vtk folder


# # # WHAT TYPE OF DATA TO GENERATE # # #
# # # code always generates a 1D file with 3 columns: time, hplus, hcross
# # # where the hp and hc are at a fixed phi and theta
phi_1D = 0.0   # azimuthal angle phi
theta_1D = pi/2    #polar angle theta, use bc for float operations

threeD_flag = 2   # 1 to generate 3D .vtk data, 0 to generate 2D .vtk data, 2 for both
# 3D GRID SETTINGS
#    makes the grid like
#        xy = np.linspace(-xy_max, xy_max, xy_num)    <-SQUARE
#        z = np.linspace(z_min, z_max, z_num)
xy_max_3D = 5
xy_num_3D = 5
z_min_3D = -5
z_max_3D = 0
z_num_3D = 5
# 2D GRID SETTINGS  ; only supports xy plane gw data for now
#                   ; to plot a general plane, can keep the below parameters, but x and y are general vectors
#                   ; define a plane with a point and a normal vector, and make x y orthonormal vectors that span the 2D space orthogonal to the normal
#                   ; can do grahm schmidt to get these
#     makes the grid like
#          xy = np.linspace(-xy_max, xy_max, xy_num), z=0   <-SQUARE
xy_max_2D = 5
xy_num_2D = 5




# # # stuff from psi4 and clm
# # # next 4 are set automatically later on but if things go wrong, this should be the first thing to double check
r_areal = 70.0   #extraction radius:  r_areal column in Psi4_file
gw_dt = 0.432     #dt in Psi4 file, not same as dt in regular params, is set automatically after
num_modes = 1 #21   #is num columns of Psi4 - 5 divided by 2, printed out by calc_clm
num_times = 4143 #num rows in Psi4, is changed automatically after, printed out by calc_clm as well

# # # time stuff
all_times = 0    #boolean 0 (false) or 1 (true) (run custom range or run all times)
start_time = 0         #custom range for testing if needed
end_time = 2000   


# # # # # # # # # #
# # # START PARAMETERS FOR ANALYTICAL TEST # # #
# # # uses the same dimensions as Psi4 processing
# # # shouldn't need to touch for normal movies, just keep test_flag=0
test_num_times = 2000
test_dt = 1.0
test_kind = 0  # 0 is rotate, 1 is pulsate, 2 is ring pulsate
test_R = 0.1
test_M = 1.0
test_Om = 0.3


# # # # AUTOMATICALLY SET VARIABLES FROM ABOVE # # #
# # # # shouoldn't need to touch regularly
psi4_f = psi4_dir + "/Psi4_rad.mon." + str(psi4_num) # # # psi4 file
bin_dir = root + "/bin"    # where main scripts are to avoid declutter


# # # # fetching some of the psi4 specific parameters
psi4_f_sorted = bin_dir + "/Psi4_rad.sort"


completed = subprocess.run([bin_dir + "/sort.sh", psi4_f, psi4_f_sorted], capture_output=True, text=True)
out_arr = completed.stdout.strip().split('\n')


num_times = int(out_arr[0])
num_modes = int(out_arr[1])
r_areal = float(out_arr[2])
gw_dt = float(out_arr[3])


grid_params = [xy_max_3D, xy_num_3D, z_min_3D, z_max_3D, z_num_3D, xy_max_2D, xy_num_2D, phi_1D, theta_1D]
psi4_params = [psi4_dir, psi4_num, psi4_f, psi4_f_sorted]
simulation_params = [M_ADM, cutoff_w, r_areal, gw_dt, num_modes, num_times]
test_gw_params = [test_num_times, test_dt, test_kind, test_R, test_M, test_Om]

gw_params = [root, test_flag, update_lookup, files_per_folder, psi4_params, grid_params, simulation_params, all_times, start_time, end_time, bin_dir, test_gw_params, threeD_flag]








