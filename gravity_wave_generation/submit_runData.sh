#!/bin/bash
# Batch wrapper for the GW pipeline -- use this instead of running on the login node.
#   sbatch submit_runData.sh        (or:  FORCE=1 sbatch --export=ALL,FORCE=1 submit_runData.sh)
# EDIT the #SBATCH account/partition for your cluster (defaults are Purdue Anvil / sol_05).
#SBATCH -J gw_pipeline
#SBATCH -A mca99s008
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 64
#SBATCH -t 02:00:00
#SBATCH -o gw_pipeline_%j.log
#SBATCH --export=ALL
set -e
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")}"
. ${MODULESHOME}/init/bash 2>/dev/null || true
module load anaconda/2024.02-py311 2>/dev/null || true   # numpy/scipy/meshio/matplotlib
export NPROC=${SLURM_NTASKS:-64}                          # make_vtk parallelism
echo "START $(date) on $(hostname); NPROC=$NPROC"
./runData_generation.sh
echo "EXIT rc=$? $(date)"
