#!/bin/bash

# Script to use the scripts in psi4_hlm to generate the h_lm and GW fluxes from the Psi4 outputs 
# from the NS-NS simulations 

# source /opt/intel/oneapi/setvars.sh   # removed: gfortran build, no Intel/oneAPI on Anvil
home_dir=$(pwd)

sim_names=(
../psi4_dir   # local data dir; rhphc.N.dat written directly into psi4_dir
)


for sim_name in ${sim_names[@]}
do
  for Psi4_file_num in 1 2 3 4 5 6 7 8 9   # all extraction radii present in psi4_dir
  do
    echo "##### getting GW h_22 for ${sim_name}"
    #cp /data/jbamber/${sim_name}/data/Psi4_rad.mon.* .
    cd $sim_name

    tail -n +2 Psi4_rad.mon.${Psi4_file_num} | sed '/NaN/d' | sort -k1 -g -u > Psi4_rad.mon_sorted.${Psi4_file_num}

    echo "Sorted Psi4_rad.mon.${Psi4_file_num}"

    m_adm_val=0.0603349020955639   # M_ADM in code units (= M_sun) for this system
    omega_val=0.342                # code-unit w_lower_cut (orbital ang. vel.), user-specified
    # Chi0.7_aligned: 0.25/m_adm=0.02239769052
    # Spatial_sigma_restart_1: 0.25/m_adm=0.02135921495
    # Chi0.7_aligned_restart_20_v12: 0.25/m_adm=0.02168762996 0.5/m_adm=0.04337525992 
    # Chi0.7_Spatial_Sigma: (0.25/m_adm is best) .1/m_adm=0.00865062577  1/m_adm=0.0865062577 0.5/m_adm=0.04325312887 0.01/m_adm=0.00865062577 0.25/m_adm=0.02162656443 0.2/m_adm=0.01730125154 
    t_start=-100
    t_end=100.0
    number_of_columns=47   # this data: 47 cols = 21 modes  ((47-5)/2)

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