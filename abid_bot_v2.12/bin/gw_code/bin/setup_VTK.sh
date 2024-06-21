#!/bin/bash

fol_name=$1
files_per_folder=$2
root=$3

cd $fol_name/2D
folderidx=0
file_count=0
echo "Moving files into new folders"
for f in hplus*; do
        curdir=VTK$(printf "%03d" $folderidx)
        if [ ! -d $curdir ]; then
                mkdir $curdir
        fi
        mv $f $curdir
        if [ $files_per_folder == $file_count ]; then
                folderidx=$((folderidx+1))
                file_count=0
        fi
        file_count=$((file_count+1))
done
folderidx=0
file_count=0
for f in hcross*; do
        curdir=VTK$(printf "%03d" $folderidx)
        if [ ! -d $curdir ]; then
                mkdir $curdir
        fi
        mv $f $curdir
        if [ $files_per_folder == $file_count ]; then
                folderidx=$((folderidx+1))
                file_count=0
        fi
        file_count=$((file_count+1))
done

cd $fol_name/3D
folderidx=0
file_count=0
echo "Moving files into new folders"
for f in hplus*; do
        curdir=VTK$(printf "%03d" $folderidx)
        if [ ! -d $curdir ]; then
                mkdir $curdir
        fi
        mv $f $curdir
        if [ $files_per_folder == $file_count ]; then
                folderidx=$((folderidx+1))
                file_count=0
        fi
        file_count=$((file_count+1))
done
folderidx=0
file_count=0
for f in hcross*; do
        curdir=VTK$(printf "%03d" $folderidx)
        if [ ! -d $curdir ]; then
                mkdir $curdir
        fi
        mv $f $curdir
        if [ $files_per_folder == $file_count ]; then
                folderidx=$((folderidx+1))
                file_count=0
        fi
        file_count=$((file_count+1))
done


cd $root
