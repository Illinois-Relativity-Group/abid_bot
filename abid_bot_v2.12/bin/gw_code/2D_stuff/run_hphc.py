from gw_params import gw_params
from abidbot import AbidBot
import sys
import os
sys.path.append(os.path.abspath("/anvil/scratch/x-rnarasimhan/gw_bot/bin"))
from hplus_hcross import setup_gw

import shutil
import subprocess

params = []
params_fields = []
a = AbidBot(params, params_fields, gw_params)


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
job_name = "gwdata_python_testing"    #folder in root containing data will be named this
fol_name = a.gw.root + '/' + job_name   # # #  where the data is saved
a.gw.fol_name = fol_name

if os.path.exists(fol_name): shutil.rmtree(fol_name)

os.mkdir(fol_name)
os.mkdir(fol_name + '/2D')
os.mkdir(fol_name + '/3D')


if a.gw.test_flag == False:   #need to run cpp code
    print("Staring calc_clm CPP code")
    subprocess.run([a.gw.bin_dir + "/run_cpp.sh", a.gw.bin_dir, a.gw.psi4_f_sorted, str(a.gw.M_ADM), str(a.gw.cutoff_w), fol_name])
    print("CPP code finished")


setup_gw(a)


subprocess.run([a.gw.bin_dir + "/setup_VTK.sh", a.gw.fol_name, str(a.gw.files_per_folder), a.gw.root])

print("YIPPPPEEEEEEEEEE DONE XD")



