#!/bin/bash
module load python3

# code for the cpp part of the code
# process Psi4 and create Clm
# also can set the number of modes and numtimes and dt, etc


# # # # # SET VARIABLES # # # # #
# # # for python part
# # # don't end with slash (though i don't think it matters)
root="/scratch1/08211/ericyu3/python_test"
test_flag=0    #boolean 0 or 1
fol_name=$root/gwdata   # # #  where the data is saved
update_lookup=1   #boolean 0 or 1   only need to update if you change resolution or num modes

# # # START PARAMETERS FOR PSI4 PROCESSING # # #
psi4_f=Psi4_rad.mon.3
M_ADM=1.0
cutoff_w=0.05
extraction_r=80.0
files_per_folder=25  #files per vtk folder




# # # stuff from psi4 and clm
dt=0.432
num_modes=30   #is num columns of Psi4 - 5 divided by 2, printed out by calc_clm
num_times=8830
start_num=4000
end_num=4025
# makes the grid like
#    xy = np.linspace(-xy_max, xy_max, xy_num)
#    z = np.linspace(z_min, z_max, z_num)
xy_max=75
xy_num=60
z_min=-75
z_max=0
z_num=25
# # # # # # # # # # 
# # # START PARAMETERS FOR ANALYTICAL TEST # # #
# # # uses the same dimensions as Psi4 processing
test_num_times=20
test_dt=0.25
test_kind=0  # 0 is rotate, 1 is pulsate, 2 is ring pulsate
test_R=1.0  
test_M=1.0
test_Om=2.0

# # # # # # # # # # # # # # # # # # # # # # # # # 
psi4_f_sorted="${psi4_f}.sort"
sed '/NaN/d' ./$psi4_f | sort -k1 -g -u > $psi4_f_sorted
a=($(wc $psi4_f_sorted))
num_times=$((${a[0]}-1))  #num lines in sorted Psi4 minus the comment line

#TEMP COMMENTED
if [ -d $fol_name ]
then
     rm -rf $fol_name
fi
mkdir $fol_name
mkdir $fol_name/3D



export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/lib
echo "Starting calc_clm CPP code"
g++  -I $HOME/usr/include -O2 -fopenmp DataFile.cpp calc_clm.cpp -o calc_clm -L/usr/lib64 -L$HOME/usr/lib -lfftw3 && ./calc_clm $psi4_f_sorted $M_ADM $cutoff_w $fol_name
echo "CPP code finished"


python3 hplus_hcross.py $root $fol_name $dt $num_modes $num_times $xy_max $xy_num $z_min $z_max $z_num $test_flag $test_num_times $test_dt $test_kind $test_R $test_M $test_Om $update_lookup $start_num $end_num



python3 gw_time_lister.py $M_ADM $gw_dt $extraction_r $fol_name
echo "Time list finished"
cur=$PWD
cd $fol_name/3D
numfiles=$(ls *hcross* | wc -l)
folderidx=0
echo "Moving files into new folders"
for i in `seq 0 $(($numfiles - 1))`; do
	curdir=VTK$(printf "%03d" $folderidx)
	if [ ! -d $curdir ]; then
		mkdir $curdir
	fi
	mv *_$(printf "%d" $i).vtk $curdir
	if [ $(( ($i+1) % $files_per_folder)) == 0 -a $i != 0 ]; then
		folderidx=$((folderidx+1))
	fi
done
echo "YIPPPPEEEEEEEEEE DONE XD"
cd $cur



