from gwbot import gw
import sys, os, shutil, subprocess
sys.path.append(os.path.join(gw.root,'bin'))
from hplus_hcross import setup_gw




# running script for the gw_code
#     there is an old c++ script that does double time integration
#     of psi4 into clm by using fftw; it works and is kinda complicated so i just left it as is
#     the main script is hplus_hcross.py which creates .vtk files that visit can read
#  
# use:
#     set the parameters in gw_params
#     set the name of the folder where data will be output


# set variables in gw_params

# set job name
job_name = "VTKdata"    #folder in root containing data will be named this
fol_name = gw.root + '/' + job_name   # # #  where the data is saved
gw.fol_name = fol_name

if os.path.exists(fol_name): shutil.rmtree(fol_name)

os.mkdir(fol_name)
os.mkdir(fol_name + '/2D')
os.mkdir(fol_name + '/3D')


if gw.test_flag == False:   #need to run cpp code
    print("Staring calc_clm CPP code")
    subprocess.run([gw.bin_dir + "/run_cpp.sh", gw.bin_dir, gw.psi4_f_sorted, str(gw.M_ADM), str(gw.cutoff_w), fol_name])
    print("CPP code finished")


setup_gw(gw)


subprocess.run([gw.bin_dir + "/setup_VTK.sh", gw.fol_name, str(gw.files_per_folder), gw.root])

print("YIPPPPEEEEEEEEEE DONE XD")



