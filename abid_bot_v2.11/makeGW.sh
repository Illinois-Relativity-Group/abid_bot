#!/bin/bash
#
#Created by Eric Connelly 6/6/17
#
#Note: You *must* run setup.sh before running this script for the first time. Specifically, you need the xml folder in order to generate time_list.txt.
#
#First produce a data folder called 3D using hplus_hcross.cpp on your local machine. You'll need Psi_rad.mon.x, where x is some extraction level and the extraction radius at that level. 5 is a good starting point. The extraction radii can be found in the .par file for your case. You'll have to find an appropriate cutoff frequency for the inverse Fourier transform in hplus_hcross.cpp. It should be around half of the initial frequency of the system, though results have varied. Default to 0.05.
#
#TODO: make list_times.sh

. params

if [ ! -f $root/gwdata/1D ]; then
	echo "1D file not found. Please generate and put into abid_bot/gwdata/"
else
	if [ ! -f $root/gwdata/time_list.txt ]; then
		echo "Creating time_list.txt"
		ls $root/xml/* | grep time* | sed -e 's/time_//;s/.txt//' > $root/gwdata/time_list.txt
	else
		echo "Using found time_list.txt"
	fi

	if [ -e $root/gwdata/less_3D ]; then
		echo "Deleting old less_3D folder"
		rm -rf $root/gwdata/less_3D
	fi
	
	echo "Creating less_3D folder"
	mkdir $root/gwdata/less_3D

	python $root/bin/gw_code/choose_3D.py $gw_dt $M $root

fi
