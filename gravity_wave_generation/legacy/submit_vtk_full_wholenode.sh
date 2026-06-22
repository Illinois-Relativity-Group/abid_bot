#!/bin/bash
#SBATCH -J vtk_full_200
#SBATCH -A mca99s008
#SBATCH -p wholenode
#SBATCH -N 1
#SBATCH -n 128
#SBATCH -t 02:00:00
#SBATCH -o /anvil/scratch/x-yguo11/abid_bot_dev/gravity_wave_generation/vtk_full_wn_%j.log
#SBATCH --export=ALL
# Full 2D VTK movie (all 8694 frames) at the approved test-image settings (xy_max_2D=200,
# r_lookup=bak1000*0.20, ylm reused, scale_factor=5000). ZSCALE 1.5 applied later in Blender.
# Wholenode: 128 cores -> Pool(128) in make_vtk_full.py. ~few min runtime; 2h is just buffer.
# Output: VTKdata/2D/hplus_NNNNNN.vtk (~1 MB each, ~8.7 GB). No make_lookup/rhphc rebuild.
set -e
cd /anvil/scratch/x-yguo11/abid_bot_dev/gravity_wave_generation
. ${MODULESHOME}/init/bash
module load anaconda/2024.02-py311
mkdir -p VTKdata/2D
echo "START $(date) on $(hostname); ntasks=$SLURM_NTASKS cpus_on_node=$SLURM_CPUS_ON_NODE"
python3 make_vtk_full.py
rc=$?
echo "EXIT rc=$rc $(date)"
echo "VTK files in VTKdata/2D: $(ls VTKdata/2D/*.vtk 2>/dev/null | wc -l)  (expect 8694)"
