#!/bin/bash
# ============================================================================
#  USER CONFIG for the GW-generation pipeline
#  Edit the values below for YOUR simulation, then run:  ./runData_generation.sh
#  (Shipped with the sol_05 reference values as a known-good example.)
# ============================================================================

# Pipeline root -- auto-detects this file's directory; normally leave as-is.
export GW_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- your simulation ---------------------------------------------------------
export PSI4_NUM=8                       # single-radius default / fallback (which Psi4_rad.mon.N)
export PSI4_NUMS="1 2 3 4 5 6 7 8 9"    # radii to loop over (space-separated); set to one value for a single radius
export M_ADM=0.0603349020955639         # ADM mass in code units (= M_sun)  [sol_05; restored for this run to match existing rhphc.N.dat]
export OMEGA_CUT=0.342                  # w_lower_cut: orbital angular velocity (code units),  [sol_05]
                                        #   must be below the (2,2) GW mode frequency

# --- 2D output mesh (units of M_sun) -----------------------------------------
export XY_MAX_2D=200                    # half-width of the square mesh
export XY_NUM_2D=500                    # grid points per side
export SCALE_FACTOR=5000                # vertical exaggeration baked into the .vtk strain

# --- 1D strain plots ---------------------------------------------------------
export TRET_MODE=both                   # 1D-plot retarded-time range: both | pos | full
                                        #   both = produce *_full (incl. negative lead-in) AND *_pos (u>=0)
                                        #   pos  = only the u>=0 crop;  full = only the whole record

# --- 1D overlay frames (optional) --------------------------------------------
# Progressive "drawing-in" h_+ animation frames, for compositing the waveform onto the
# GW-mesh movie. One frame set per produced TRET_MODE range -> VTKdata/overlay_1d_<suffix>/.
export MAKE_1D_OVERLAY=0                # 0 = off (default); 1 = also emit the overlay frames
export OVERLAY_BG=transparent          # transparent (alpha, no chroma key) | green (chroma key)

# --- mode selection (drives BOTH the 2D mesh and the 1D overlay) --------------
export MODE_SELECT=4mode                # 4mode (default) = only the non-axisymmetric quadrupole
                                        #   (2,+-1)+(2,+-2) -- the physically clean 1/r modes;
                                        #   all = every mode.  (2mode is a synonym of 4mode.)

# --- 2D VTK mesh stage (heavy) -----------------------------------------------
export MAKE_VTK=0                       # 0 = skip stage 4 in the driver (default; the mesh movie
                                        #   is normally produced via sbatch submit_vtk_4mode.sh);
                                        #   1 = also emit per-radius VTK from runData_generation.sh

# NCOL, num_modes, num_times, r_areal, gw_dt are auto-derived from the data
# (Psi4 column count + bin/sort.sh) -- you do not set them here.
