#!/bin/bash

# Script to use the scripts in psi4_hlm to generate the h_lm and GW fluxes from the Psi4 outputs 
# from the NS-NS simulations 

# source /opt/intel/oneapi/setvars.sh   # removed: gfortran build, no Intel/oneAPI on Anvil
home_dir=$(pwd)
GW_ROOT=${GW_ROOT:-$(cd "$home_dir/.." && pwd)}   # from config.sh; default = parent of this dir

sim_names=(
"$GW_ROOT/psi4_dir"   # rhphc.N.dat written directly into psi4_dir
)


for sim_name in ${sim_names[@]}
do
  for Psi4_file_num in ${PSI4_NUM:-8}   # only the configured extraction radius (config.sh)
  do
    echo "##### getting GW h_22 for ${sim_name}"
    #cp /data/jbamber/${sim_name}/data/Psi4_rad.mon.* .
    cd $sim_name

    tail -n +2 Psi4_rad.mon.${Psi4_file_num} | sed '/NaN/d' | sort -k1 -g -u > Psi4_rad.mon_sorted.${Psi4_file_num}

    echo "Sorted Psi4_rad.mon.${Psi4_file_num}"

    m_adm_val=${M_ADM:-0.0603349020955639}     # from config.sh (ADM mass, code units)
    omega_val=${OMEGA_CUT:-0.342}              # from config.sh (w_lower_cut, orbital ang. vel., code units)
    t_start=-100
    t_end=100.0
    number_of_columns=$(awk 'NR==1{print NF; exit}' Psi4_rad.mon_sorted.${Psi4_file_num})   # auto from data: (NCOL-5)/2 = num modes

    declare $(head -n1 Psi4_rad.mon_sorted.${Psi4_file_num} | awk '{printf "t_start=%.6g",$1}')
    declare $(tail -n1 Psi4_rad.mon_sorted.${Psi4_file_num} | awk '{printf "t_end=%.6g",$1}')

    echo "Omega = ${omega_val}"
    echo "M_ADM = ${m_adm_val}"
    echo "t_start = ${t_start}"
    echo "t_end = ${t_end}"

    rm -f ccc_ffi.input
    cp $home_dir/ccc_ffi.input_blank ccc_ffi.input

    sed -i "s|PSI4FNAME|Psi4_rad.mon_sorted.${Psi4_file_num}|" ccc_ffi.input
    sed -i "s|OMEGAVAL|${omega_val}|" ccc_ffi.input
    sed -i "s|ADMMASS|${m_adm_val}|" ccc_ffi.input
    sed -i "s|TSTART|${t_start}|" ccc_ffi.input
    sed -i "s|TEND|${t_end}|" ccc_ffi.input
    sed -i "s|NCOL|${number_of_columns}|" ccc_ffi.input

    $home_dir/rhphc

    cp $home_dir/gw_flux.input_blank gw_flux.input

    sed -i "s|ADMMASS|${m_adm_val}|" gw_flux.input
    sed -i "s|TSTARTVAL|${t_start}|" gw_flux.input
    sed -i "s|TENDVAL|${t_end}|" gw_flux.input

    #$home_dir/flux

    mv rhphc.dat rhphc.${Psi4_file_num}.dat
    mv rhphcdot.dat rhphcdot.${Psi4_file_num}.dat
    mv ejv_GW.dat ejv_GW.${Psi4_file_num}.dat
    #mv EJ_rect.dat EJ_rect.${Psi4_file_num}.dat
    mv omega22.dat omega22.${Psi4_file_num}.dat
    cd $home_dir

  done
done

cd $home_dir