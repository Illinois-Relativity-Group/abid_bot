#!/bin/bash
# Four-mode 2D VTK: build the full mesh movie from ONLY (2,+-1)+(2,+-2), excluding (2,0).
# Radius 7 (r_areal~150.87 Msun), sol_05 constants, reusing psi4_7's full 21-mode gw.clm.
# Output -> VTKdata/psi4_7_4mode/2D/hplus_*.vtk  (~8694 frames).
#SBATCH -J vtk4mode
#SBATCH -A mca99s008
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 48
#SBATCH -t 00:45:00
#SBATCH -o vtk4mode_%j.log
#SBATCH --export=ALL
set -e
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"
. ${MODULESHOME}/init/bash 2>/dev/null || true
module load anaconda/2024.02-py311 2>/dev/null || true

source ./config.sh                 # sol_05 M_ADM/OMEGA_CUT, grid, SCALE_FACTOR (working-tree)
export PSI4_NUM=7                  # extraction radius 7 -> r_areal for retarded-time anchor
export OUT_TAG=psi4_7_4mode        # read gw.clm + write 2D/ under VTKdata/psi4_7_4mode
export MODE_SELECT=4mode           # sum only (2,+-1)+(2,+-2); (2,0) excluded
export NPROC=${SLURM_NTASKS:-48}
unset VTK_TIMES                    # FULL movie (not the smoke subset)

echo "START $(date) host=$(hostname) NPROC=$NPROC radius=$PSI4_NUM tag=$OUT_TAG mode=$MODE_SELECT"
python3 make_vtk.py
echo "EXIT rc=$? $(date)"
