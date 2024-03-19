import numpy as np
from h5loader import *
from gridder import *
import matplotlib.pyplot as plt
from scipy import interpolate

### i'm so fucking tired

### make sure you have h5py installed
###    pip install h5py

### I'm pretty sure all data from Illinois code uses these parameters ###
MPI = 128
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


### refinement_level_list
###	check by doing 'h5ls' on any of the .h5 files in h5_dir
###     there is a field called 'rl' that will go from 0 to some number
###     this list should be that same range
refinement_level_list = range(10) 






### hdf5 checkpoint file; usually looks like
###   checkpoint.chkpt.it_ITERATION.file_MPI.h5
### here we only need the prefix before _MPI.h5 
h5_dir = "/anvil/scratch/x-ericyu3/SUPERMASSIVExd/ab_IRE2.57/h5data/3d_data_24_02_13_144642/"  #end with forward slash /
h5_file_prefix = h5_dir + "checkpoint.chkpt.it_192321.file_"  # not important here


### iteration from hdf5 file
###
iteration = 381696


### name of variable you want to use, and their prefixes
###     do an h5ls on a checkpoint.h5 file to see all of these (there are a lot)
### here is set up to include all the gravity variables and
matt_prefix  = "MHD_EVOLVE"
matt_names   = ["vx", "vy", "vz"]


prefixes = [matt_prefix]
namess    = [matt_names]
all_names = matt_names

prefix_dict = {}
for prefix, names in zip(prefixes, namess):
    for name in names: prefix_dict[name] = prefix



### your grid you want to extract data from, these can also just be floats instead of float arrays
xy_bdry = 30
xy_N = 30
z_bdry = 200
z_N = 100
x_pts = np.linspace(-xy_bdry, xy_bdry, xy_N)
y_pts = np.linspace(-xy_bdry, xy_bdry, xy_N)
z_pts = np.linspace(0, z_bdry, z_N)


center_x = 0.
center_y = 0.
coefficient = 0.15
tolerance = 1
## try only outputting on z>0 since we reflect
def get_paraboloid_pts(cx, cy, coef, tol, x_pts, y_pts, z_pts):
    X, Y, Z = np.meshgrid(x_pts, y_pts, z_pts, indexing='ij')
    
    # paraboloid = coef*( (X - cx)**2 + (Y - cy)**2 )
    paraboloid =  np.abs(coef*( (X - cx)**2 + (Y - cy)**2 ) - Z)
    # sc = plt.scatter(X[:,xy_N//2,:], Z[:,xy_N//2,:], c=paraboloid[:,xy_N//2,:])
    # plt.colorbar(sc)
    # plt.savefig("test.png")
    indices = np.transpose((paraboloid < tol).nonzero())
    # indices = np.argwhere(paraboloid < tol)
    return indices







### following function found in gridder.py
###     for (x,y,z) indices being (i,j,k), can access the return like data[k][j][i]
###     look in gridder.py for some other functions as well or more info
###     i'm pretty sure this is wildly inefficient but idk



datas = []
for name in all_names:
    prefix = prefix_dict[name]
    data, time_taken = make_xyz_grid(h5_dir, h5_file_prefix, prefix, name, iteration, refinement_level_list, MPI, x_pts, y_pts, z_pts)
    datas.append(np.einsum('kji->ijk', data))
    print("loaded {}; time taken: {}".format(name, str(time_taken)))

##example
#be careful with indexing:
#   note the 'kji->ijk' einsum above and the indexing='ij' in meshgrid below
XX, YY, ZZ = np.meshgrid(x_pts, y_pts, z_pts, indexing='ij')
indices = get_paraboloid_pts(center_x, center_y, coefficient, tolerance, x_pts, y_pts, z_pts)
print(indices.shape)
N_pts = indices.shape[0]
ix = indices[:,0]
iy = indices[:,1]
iz = indices[:,2]

X = XX[ix,iy,iz]
Y = YY[ix,iy,iz]
Z = ZZ[ix,iy,iz]

vx = datas[0][ix,iy,iz]
vy = datas[1][ix,iy,iz]
vz = datas[2][ix,iy,iz]

# plt.scatter(X,Z)
# plt.savefig("test.png")
header1 = "# vtk DataFile Version 2.0\ntest_velocity_paraboloid\nASCII\nDATASET UNSTRUCTURED_GRID\nPOINTS {} float\n".format(N_pts)
out_f = open("test.vtk", "w")
out_f.write(header1)
for i in range(N_pts):
    out_f.write("{} {} {}\n".format(X[i], Y[i], Z[i]))
header2 = "POINT_DATA {}\nVECTORS test float\n".format(N_pts)
out_f.write(header2)
for i in range(N_pts):
    out_f.write("{} {} {}\n".format(vx[i], vy[i], vz[i]))
out_f.close()





