#!/bin/bash
# This simple bash script clean up the "NaN" rows and sort the Psi4 file.
# Put this script in the folder with Psi4 files
# Run as "./clean_and_sort Psi4.mon.1 Psi4.mon.sort.1"
##infile=$1
##outfile=$2
infile=Psi4_rad.mon.3
outfile=Psi4_rad.mon.sort.3
sed '/NaN/d' ./$infile | sort -k1 -g -u > $outfile
