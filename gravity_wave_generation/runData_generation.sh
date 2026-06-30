#!/bin/bash
# ============================================================================
#  GW-generation pipeline driver.
#  Edit config.sh, drop your Psi4_rad.mon.<PSI4_NUM> into psi4_dir/, then run:
#      ./runData_generation.sh
#  Re-runs skip the two expensive stages if their output already exists;
#  use  FORCE=1 ./runData_generation.sh  to regenerate everything.
# ============================================================================
#set -e
#module load texlive
#module load anaconda
#conda activate plotenv

cd "$(dirname "$0")"
source ./config.sh

echo "=== GW data generation  (GW_ROOT=$GW_ROOT  PSI4_NUM=$PSI4_NUM  M_ADM=$M_ADM  OMEGA_CUT=$OMEGA_CUT) ==="
mkdir -p "$GW_ROOT/VTKdata/2D"
RHPHC="$GW_ROOT/psi4_dir/rhphc.${PSI4_NUM}.dat"
YLM="$GW_ROOT/bin/ylm_lookup_2D.txt"

echo "[1/5] rhphc Fortran stage -> psi4_dir/rhphc.${PSI4_NUM}.dat"
if [[ -s "$RHPHC" && "${FORCE:-0}" != 1 ]]; then
  echo "      exists -> skip (FORCE=1 to regenerate)"
else
  ( cd rhphc_wave_generation && ./make_GW_hlm_from_psi4.sh )
fi

echo "[2/5] ylm + r lookups -> bin/  (slow; depends on XY_MAX_2D/XY_NUM_2D/num_modes)"
if [[ -s "$YLM" && "${FORCE:-0}" != 1 ]]; then
  echo "      exists -> skip (FORCE=1 to regenerate)"
else
  python3 make_lookup.py
fi

echo "[3/5] gw.clm -> VTKdata/gw.clm"
python3 make_clm.py

echo "[4/5] 2D VTK frames -> VTKdata/2D/hplus_*.vtk"
python3 make_vtk.py

echo "[5/5] 1D strain plots -> VTKdata/*.png"
python3 make_1d_plots.py

echo "=== done ==="
echo "  psi4_dir/rhphc.${PSI4_NUM}.dat   bin/ylm_lookup_2D.txt  bin/r_lookup_2D.txt"
echo "  VTKdata/gw.clm   VTKdata/2D/*.vtk   VTKdata/clm_sum_vs_tret_pos.png"
