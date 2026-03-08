#!/bin/bash
#
# Usage:
#   ./run_cpp.sh  <bin>  <psi4_mode20.csv>  <psi4_mode40.csv>  <M_ADM>  <cutoff_w>  <r_extr>  <output_folder>
#

bin="$1"
psi4_mode20="$2"
psi4_mode40="$3"
M_ADM="$4"
cutoff_w="$5"
r_extr="$6"
fol_name="$7"

# Make sure fol_name exists; if not, create it:
mkdir -p "$fol_name"

# If you need FFTW3 and DataFile headers in HOME/usr/include and libs in HOME/usr/lib:
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$HOME/usr/lib"

# Compile the "two modes, real‐only" code. We assume DataFile.cpp and
# calc_clm_two_modes_realonly.cpp both live under $bin/.
g++ -O2 -fopenmp \
    -I "$HOME/usr/include" \
    "$bin/DataFile.cpp" \
    "$bin/calc_clm_memory.cpp" \
    -o "$bin/calc_clm_memory" \
    -L "/usr/lib64" \
    -L "$HOME/usr/lib" \
    -lfftw3

# Check that compilation succeeded
if [ $? -ne 0 ]; then
  echo "Compilation failed. Exiting."
  exit 1
fi

# Run the newly compiled executable with all seven arguments:
"$bin/calc_clm_memory" \
  "$psi4_mode20" \
  "$psi4_mode40" \
  "$M_ADM" \
  "$cutoff_w" \
  "$r_extr" \
  "$fol_name"
