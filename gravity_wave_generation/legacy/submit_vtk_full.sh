#!/bin/bash
#SBATCH -J vtk_full_200
#SBATCH -A mca99s008
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 32
#SBATCH -t 01:00:00
#SBATCH -o /anvil/scratch/x-yguo11/abid_bot_dev/gravity_wave_generation/vtk_full_%j.log
#SBATCH --export=ALL
# Generate the FULL 2D VTK movie sequence (all 8694 frames) with the SAME settings that
# produced the approved test images: xy_max_2D=200 (+-200 mesh), r_lookup_2D = bak1000*0.20,
# ylm reused, scale_factor=5000. ZSCALE 1.5 is applied later in Blender, NOT here.
# Output: VTKdata/2D/hplus_NNNNNN.vtk  (~1 MB each, ~8.7 GB total). Reads existing gw.clm / lookups;
# does NOT touch make_lookup_with_memory.py / rhphc (no forbidden rebuild).
set -e
cd /anvil/scratch/x-yguo11/abid_bot_dev/gravity_wave_generation
. ${MODULESHOME}/init/bash
module load anaconda/2024.02-py311
mkdir -p VTKdata/2D
echo "START $(date) on $(hostname); cores=$SLURM_CPUS_PER_TASK"
python3 make_vtk_full.py
rc=$?
echo "EXIT rc=$rc $(date)"
echo "VTK files in VTKdata/2D: $(ls VTKdata/2D/*.vtk 2>/dev/null | wc -l)  (expect 8694)"
