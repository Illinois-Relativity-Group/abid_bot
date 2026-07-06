#!/bin/bash
#SBATCH -J ov2mode
#SBATCH -A mca99s008
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -t 00:45:00
#SBATCH -o ov2mode_%j.log
#SBATCH --export=ALL
# Regenerate the transparent 1D "drawing-in" overlay using ONLY the (2,+-1)+(2,+-2) sum (two m-multiplets),
# at extraction radius 7 -- matches the four-mode mesh movie. Writes VTKdata/psi4_7/overlay_1d_pos/frame_*.png.
# (Copy to blender_gw_dev/frames_1D_transparent is a separate verified step, not done here.)
set -e
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"
. ${MODULESHOME}/init/bash 2>/dev/null || true
module load anaconda/2024.02-py311 2>/dev/null || true

source ./config.sh                     # sol_05 M_ADM/OMEGA_CUT, paths (working-tree)
export PSI4_NUM=7                       # extraction radius 7 (150 M_sun) -> reads psi4_dir/rhphc.7.dat
export OUT_TAG=psi4_7                   # write under VTKdata/psi4_7 (reuse the four-mode radius)
export TRET_MODE=pos                    # u>=0 crop only (matches the movie); no negative lead-in
export MAKE_1D_OVERLAY=1                # emit the drawing-in overlay frames
export OVERLAY_BG=transparent          # alpha background (no chroma key)
export OVERLAY_MODE=2mode               # <-- draw ONLY (2,+-1)+(2,+-2), not the all-mode sum

echo "START $(date) host=$(hostname) radius=$PSI4_NUM mode=$OVERLAY_MODE bg=$OVERLAY_BG range=$TRET_MODE"
python3 make_1d_plots.py
echo "EXIT rc=$? $(date)"
echo "overlay frames: $(ls VTKdata/psi4_7/overlay_1d_pos/frame_*.png 2>/dev/null | wc -l)  in VTKdata/psi4_7/overlay_1d_pos/"
