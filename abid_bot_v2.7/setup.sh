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

. params

. $bin/clean_h5folders.sh
. $bin/make_h5folders.sh 


if $bhForms
then
	. $bin/setup_bh.sh
fi

if $fields || $particleTracer
then
	. $bin/setup_seeds.sh
fi

. $bin/setup_cm.sh

. $bin/setup_frames.sh

echo "setup complete!"
