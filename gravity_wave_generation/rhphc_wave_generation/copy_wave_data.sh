#!/bin/bash

home_dir=$(pwd)
sim_name="Monoenergetic_N25_yc0.605_ID2_chi0.7_aligned"  #Monoenergetic_N25_yc0.819_ID2_chi0.7_aligned_restart_20_v12" #"Monoenergetic_N25_yc0.819_ID2_chi0.7_spacial_sigma" --- IGNORE ---
source_dir="/data/codyolson/memory_effect/chi0.7_aligned"

echo "Copying Psi4 data and rhphc files from $home_dir/$sim_name to $source_dir/psi4_dir/"
cp -r $home_dir/$sim_name/Psi4_rad.mon* $source_dir/psi4_dir/
cp -r $home_dir/$sim_name/rhphc.* $source_dir/psi4_dir/
