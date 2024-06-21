#!/bin/bash

fol_name=$1
files_per_folder=$2
root=$3

cd $fol_name/2D
numfiles=$(ls *hcross* | wc -l)
folderidx=0
echo "Moving 2D files into new folders"
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
cd $root
cd $fol_name/3D
numfiles=$(ls *hcross* | wc -l)
folderidx=0
echo "Moving 3D files into new folders"
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
cd $root
