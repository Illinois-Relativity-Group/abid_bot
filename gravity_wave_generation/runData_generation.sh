#!/bin/bash
# generate_memory_data.sh
# Runs all Python scripts needed to generate memory data

#set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting memory data generation..."

python3 make_lookup_with_memory.py
echo "Finished make_lookup_with_memory.py"

python3 make_gw_clm_from_jamies_data.py
echo "Finished make_gw_clm_from_jamies_data.py"

python3 make_vtk_with_memory.py
echo "Finished make_vtk_with_memory.py"

python3 memory_plots.py
echo "Finished memory_plots.py"

echo "All scripts completed successfully!"
