#!/bin/bash
# ============================================================================
#  USER CONFIG for the GW-generation pipeline
#  Edit the values below for YOUR simulation, then run:  ./runData_generation.sh
#  (Shipped with the sol_05 reference values as a known-good example.)
# ============================================================================

# Pipeline root -- auto-detects this file's directory; normally leave as-is.
export GW_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- your simulation ---------------------------------------------------------
export PSI4_NUM=8                       # which Psi4_rad.mon.N to process (extraction radius)
export M_ADM=0.0603349020955639         # ADM mass in code units (= M_sun)
export OMEGA_CUT=0.342                  # w_lower_cut: orbital angular velocity (code units),
                                        #   must be below the (2,2) GW mode frequency

# --- 2D output mesh (units of M_sun) -----------------------------------------
export XY_MAX_2D=200                    # half-width of the square mesh
export XY_NUM_2D=500                    # grid points per side
export SCALE_FACTOR=5000                # vertical exaggeration baked into the .vtk strain

# --- 1D strain plots ---------------------------------------------------------
export TRET_MODE=both                   # 1D-plot retarded-time range: both | pos | full
                                        #   both = produce *_full (incl. negative lead-in) AND *_pos (u>=0)
                                        #   pos  = only the u>=0 crop;  full = only the whole record

# NCOL, num_modes, num_times, r_areal, gw_dt are auto-derived from the data
# (Psi4 column count + bin/sort.sh) -- you do not set them here.
