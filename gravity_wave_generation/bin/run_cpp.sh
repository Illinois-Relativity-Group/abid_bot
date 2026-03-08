#!/bin/bash

bin=$1
psi4_f_sorted=$2
M_ADM=$3
cutoff_w=$4
fol_name=$5

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/lib
g++  -I $HOME/usr/include -O2 -fopenmp $bin/DataFile.cpp $bin/calc_clm.cpp -o $bin/calc_clm -L/usr/lib64 -L$HOME/usr/lib -lfftw3 && $bin/calc_clm $psi4_f_sorted $M_ADM $cutoff_w $fol_name
