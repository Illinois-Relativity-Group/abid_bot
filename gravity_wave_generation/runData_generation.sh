#!/bin/bash
# ============================================================================
#  GW-generation pipeline driver (multi-extraction-radius).
#  Edit config.sh, drop your Psi4_rad.mon.<N> files into psi4_dir/, then run:
#      ./runData_generation.sh
#  Loops over PSI4_NUMS (config.sh); each radius N writes to VTKdata/psi4_N/.
#  The ylm/r lookup is radius-independent and built ONCE (shared by all radii).
#  Re-runs skip rhphc/lookup if their output exists; FORCE=1 regenerates them.
# ============================================================================
set -e
cd "$(dirname "$0")"
source ./config.sh

RADII="${PSI4_NUMS:-$PSI4_NUM}"          # space-separated radius list; default = single PSI4_NUM
echo "=== GW data generation | radii: [$RADII] | M_ADM=$M_ADM OMEGA_CUT=$OMEGA_CUT ==="

# --- shared lookup (radius-INDEPENDENT: grid + num_modes only) -- build once ---
YLM="$GW_ROOT/bin/ylm_lookup_2D.txt"
echo "[lookup] ylm + r tables -> bin/  (shared by all radii)"
if [[ -s "$YLM" && "${FORCE:-0}" != 1 ]]; then
  echo "         exists -> skip (FORCE=1 to regenerate)"
else
  python3 make_lookup.py
fi

# --- per-radius stages ---
for n in $RADII; do
  export PSI4_NUM=$n
  TAG="psi4_$n"
  echo "=== radius $n -> VTKdata/$TAG ==="
  RHPHC="$GW_ROOT/psi4_dir/rhphc.$n.dat"

  echo "  [1] rhphc Fortran stage -> psi4_dir/rhphc.$n.dat"
  if [[ -s "$RHPHC" && "${FORCE:-0}" != 1 ]]; then
    echo "      exists -> skip (FORCE=1 to regenerate)"
  else
    ( cd rhphc_wave_generation && ./make_GW_hlm_from_psi4.sh )
  fi

  echo "  [3] gw.clm -> VTKdata/$TAG/gw.clm"
  python3 make_clm.py

  echo "  [5] 1D strain plots -> VTKdata/$TAG/*.png"
  python3 make_1d_plots.py

  # --- stage 4 (2D VTK): heavy; gated by MAKE_VTK (config.sh). Default off -- the mesh movie is
  #     normally produced via sbatch submit_vtk_4mode.sh. Set MAKE_VTK=1 to emit it per-radius here.
  if [[ "${MAKE_VTK:-0}" == 1 ]]; then
    echo "  [4] 2D VTK frames -> VTKdata/$TAG/2D/hplus_*.vtk"
    python3 make_vtk.py
  fi
done

echo "=== done: $(echo $RADII | wc -w) radius/radii -> VTKdata/psi4_* (stages 1,3,5; 4 disabled) ==="
