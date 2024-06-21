import os
import subprocess
from math import pi
import sys
# written by eric may '23

root = sys.argv[1]

print("Running params_gw.py")
# # # for python part
# # # don't end with slash (though i don't think it matters)
gw_dir = root + "/bin/gw_code"
test_flag = False     #boolean 0 (false) or 1 (true) (regular run or test source run)
update_lookup = True   #boolean 0 or 1   only need to update if you change resolution or num modes

# # # START PARAMETERS FOR PSI4 PROCESSING # # #
psi4_dir = root + "/bin/gw_code/psi4_dir"   #folder containing Psi4_rad.mon.#
psi4_num = 3  # the last number # in Psi4_ad.mon.#, corresponds to extraction radius
plot_all_modes = True #plots the sum of all the modes if true
modes_to_plot = [0,4]   #if above is false, then plots only this mode; must be a number 0,1,...,num_modes-1
                       # mode 0 is (2,2), 1 is (2,1), 2 is (2,0), 3 is (2,-1), 4 is (2,-2), 5 is (3,3), etc..


M_ADM = 2.51
cutoff_w = 0.027      # has to be lower than the fundamental freq of gw radiation, ask someone else for this
files_per_folder = 25  #files per vtk folder


# # # WHAT TYPE OF DATA TO GENERATE # # #
# # # code always generates a 1D file with 3 columns: time, hplus, hcross
# # # where the hp and hc are at a fixed phi and theta
phi_1D = 0.0   # azimuthal angle phi
theta_1D = pi/2    #polar angle theta, use bc for float operations

threeD_flag = 0   # 1 to generate 3D .vtk data, 0 to generate 2D .vtk data, 2 for both
# 3D GRID SETTINGS
#    makes the grid like
#        xy = np.linspace(-xy_max, xy_max, xy_num)    <-SQUARE
#        z = np.linspace(z_min, z_max, z_num)
xy_max_3D = 500
xy_num_3D = 175
z_min_3D = -500
z_max_3D = -.1
z_num_3D = 75
# 2D GRID SETTINGS  ; only supports xy plane gw data for now
#                   ; to plot a general plane, can keep the below parameters, but x and y are general vectors
#                   ; define a plane with a point and a normal vector, and make x y orthonormal vectors that span the 2D space orthogonal to the normal
#                   ; can do grahm schmidt to get these
#     makes the grid like
#          xy = np.linspace(-xy_max, xy_max, xy_num), z=0   <-SQUARE
xy_max_2D = 1000
xy_num_2D = 500

# 2D PLANE SETTINGS ; option to pick on which plane 2D data is generated on
#                   ; you may want to visualize other 'direcitons' if the system being studied is not axisymmetric
#                  
#   choose_plane (boolean): if False, then plots on the xy plane
#                           if True, then plots on the plane centered at (0,0,0) with normal vector plane_norm
#   plane_norm (3-tuple of float): defines a plane centered at (0,0,0) with specified norm vec
#                       e.g. plane_norm=(1.0,0.0,0.0) specifies the yz plane                               
choose_plane = False
plane_norm = (0., 0., 1.)



# # # stuff from psi4 and clm
# # # next 4 are set automatically later on but if things go wrong, this should be the first thing to double check
r_areal = 3.0257539560E+02   #extraction radius:  r_areal column in Psi4_file
gw_dt = 3.5303225806E+00     #dt in Psi4 file, not same as dt in regular params, is set automatically after
num_modes = 1 #21   #is num columns of Psi4 - 5 divided by 2, printed out by calc_clm
num_times = 4143 #num rows in Psi4, is changed automatically after, printed out by calc_clm as well

# # # time stuff
all_times = 1    #boolean 0 (false) or 1 (true) (run custom range or run all times)
start_time = 0         #custom range for testing if needed
end_time = 1000   


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

###################################################################################################

# # # # AUTOMATICALLY SET VARIABLES FROM ABOVE # # #
# # # # shouoldn't need to touch regularly
psi4_f = psi4_dir + "/Psi4_rad.mon." + str(psi4_num) # # # psi4 file
bin_dir = gw_dir + "/bin"    # where main scripts are to avoid declutter


# # # # fetching some of the psi4 specific parameters
psi4_f_sorted = bin_dir + "/Psi4_rad.sort"


completed = subprocess.run([bin_dir + "/sort.sh", psi4_f, psi4_f_sorted], capture_output=True, text=True)
out_arr = completed.stdout.strip().split('\n')


num_times = int(out_arr[0])
num_modes = int(out_arr[1])
r_areal = float(out_arr[2])
gw_dt = float(out_arr[3])

###################################################################################################

generalGWSettings = [gw_dir, test_flag, update_lookup, files_per_folder, threeD_flag, all_times, start_time, end_time]
psi4Settings = [psi4_dir, psi4_num, psi4_f, psi4_f_sorted, bin_dir]
gridSettings = [xy_max_3D, xy_num_3D, z_min_3D, z_max_3D, z_num_3D, xy_max_2D, xy_num_2D, phi_1D, theta_1D, choose_plane, plane_norm]
simulationSettings = [M_ADM, cutoff_w, r_areal, gw_dt, num_modes, num_times, plot_all_modes, modes_to_plot]
testGWSettings = [test_num_times, test_dt, test_kind, test_R, test_M, test_Om]

params_gw = [generalGWSettings, psi4Settings, gridSettings, simulationSettings, testGWSettings]




