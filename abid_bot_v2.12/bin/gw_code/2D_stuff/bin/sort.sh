#!/bin/bash

psi4_f=$1
psi4_f_sorted=$2


sed '/NaN/d' $psi4_f | sort -k1 -g -u > $psi4_f_sorted
a=($(wc $psi4_f_sorted))
num_times=$((${a[0]}-1))
num_cols=($(awk '{print NF}' $psi4_f_sorted | sort -nu | head -n 1))
num_modes=$(( ($num_cols - 5)/2 ))
r_areal=$(printf "%.14f" $(awk 'NR == 2 {print $'$(($num_cols - 3))'}' $psi4_f_sorted) ) # extraction radius, r_areal column in Psi4_file, first time
t2=$(printf "%.14f" $(awk 'NR == 3 {print $1}' $psi4_f_sorted) )
t1=$(printf "%.14f" $(awk 'NR == 2 {print $1}' $psi4_f_sorted) )
gw_dt=$(echo "$t2 - $t1" | bc)


echo $num_times   #out_arr[0]
echo $num_modes   #out_arr[1] ...
echo $r_areal
echo $gw_dt
