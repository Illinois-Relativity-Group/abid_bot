#This script undoes everything that setup.sh has done. It's a nice restart tool

. params

echo "cleaning root"
rm -rf $root/xml/
rm -rf $root/bhdata/
rm -rf $root/seeds/
rm -rf $root/cm.txt
rm -rf $root/movies/*
rm -rf $root/visitlog.py
rm -rf $root/core

echo "cleaning grid_code/"
cd $root/bin/grid_code/
rm -rf bhcen*.txt bhseeds/*

echo "cleaning particle_code/"
cd $root/bin/particle_code/
rm -rf dat/ filesOrigin.txt seeds/*
cd $root/bin/particle_code/misc/
rm -rf files.txt part.txt

echo "cleaning bw_many_folder_scripts/"
cd $root/bin/bw_many_folder_scripts/
rm -rf *.txt

echo "cleaning gwdata/"
rm -rf $root/gwdata/less_3D/
rm $root/gwdata/logtime.txt
rm $root/gwdata/time_list.txt

echo "cleaning done!"
cd $root
