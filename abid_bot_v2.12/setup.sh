#!/bin/bash
#
#Created by Abid Khan 05/31/17
#
#
#Given a system's h5data and/or horizon data, this script sets up everthing and makes a movie if 
#desired. It requires the parameters to be filled out below.
#
#This script works for all kinds of systems like NSNS, BHNS, BHBH, and SMS. There is no code in this 
#script that needs to be changed depending on the system, only the parameters. You may, however, need 
#to update the following scripts:
#	
#	bw_many_folder_scripts/setmovie.py
#	bw_many_folder_scripts/run_many_movie_ranks.py
#	particle_code/particlePicker.py
#	grid_code/seedmaker.py
#
#In the root folder, you must have a folder called h5data/. In it should be 3d_data folders and a 
#folder called horizon/. In the horizon/ folder, there should be a folder called all_horizon/ and in 
#that should be a a bunch of *.gp files. also in the root folder, there must be a file called 
#"bhns.xon". If your simulation requires field lines, then you must also have the file "particles.mon"
#in your h5data folder as well. 
#
#ONE FINAL NOTE: this code is pretty general for all cases, but it may not be general enough. If you 
#find a case that is not covered in this code, then I would encourage you to generalize the code to 
#include that case. This is mainly done through "if" statements and such.

# Remember to run params, then bin/link_h5data.sh to set up your data folders
module load python

setN=$1

if [[ -f "params$setN" ]];then
	#echo "using params$setN"
	. params$setN
else
	echo "params$setN not found. using params"
	. params
fi

. $bin/clean_h5folders.sh $setN
. $bin/make_h5folders.sh $setN

if [ "$bhForms" = false ] && [ -d bhdata ]; 
then
  rm -r bhdata
fi

if $bhForms
then
	. $bin/setup_bh.sh
fi

if $fields || $particleTracer
then
	. $bin/setup_seeds.sh
fi

. $bin/setup_cm.sh

if $updateGWdata;then
	cd $gwdir
	python3 setup_gw.py $root >&setup_progress.txt&
	cd $root
	echo "Creating the VTK files needed for gravitational waves takes a long time, so I'm running it in the background"
	echo "You will need to rerun setup.sh"
	echo "Run this command after some time: tail -n 1 $gwdir/setup_progress.txt"
	echo "If the output is YIPPPPEEEEEEEEEE DONE XD, set updateGWdata=false in params and rerun setup.sh"
fi

. $bin/setup_frames.sh $setN

spinf=$root/h5data/bhns_BHspin.mon
if [[ -f "$spinf" ]];then
	python3 $bin/setup_spinvtk.py $root $M $setN
fi



#. particle_file_cleaner.sh
#. stream1_maker.sh
#. grid_seed_maker.sh
#. xml_file_remover.sh

echo "setup complete!"
