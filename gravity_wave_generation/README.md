# GW generation pipeline

Turns a numerical-relativity simulation's `Psi4_rad.mon.*` output into gravitational-wave
data products: the `rhphc.*.dat` strains, ylm/r lookup tables, `gw.clm`, 2D `.vtk` mesh
frames, and 1D strain plots. (Downstream OBJ conversion + Blender rendering live in
`blender_gw_dev`, not here.)

## Requirements

- **gfortran** (to build the `rhphc` strain calculator; a prebuilt `rhphc` binary is included)
- **Python 3** with `numpy`, `scipy`, `meshio`, `matplotlib`

## Setup

1. **Put your data in `psi4_dir/`:** copy your `Psi4_rad.mon.N` file(s) there
   (`N` = extraction-radius index).
2. **Edit `config.sh`** — the only file you change. It ships with sol_05 reference values:
   ```sh
   export PSI4_NUM=8           # which Psi4_rad.mon.N to process
   export M_ADM=0.0603349...   # ADM mass, code units (= M_sun)
   export OMEGA_CUT=0.342      # w_lower_cut (orbital ang. vel., code units)
   export XY_MAX_2D=200        # mesh half-width (M_sun)
   export XY_NUM_2D=500        # grid points per side
   export SCALE_FACTOR=5000    # vertical exaggeration baked into the .vtk
   export TRET_MODE=both       # 1D plots: both | pos (u>=0 only) | full (whole record)
   ```
   `num_modes`, `num_times`, `r_areal`, `gw_dt`, and the Fortran `NCOL` are auto-derived
   from the data — you do not set them.
3. **(if needed) rebuild `rhphc`:** the included binary is for Anvil/Linux; to rebuild:
   ```sh
   cd rhphc_wave_generation && gfortran -O2 -o rhphc ccc_ffi_hplus_hcross_ejkick.f90 && cd ..
   ```

## Run

```sh
./runData_generation.sh
```
Re-runs skip the two slow stages (rhphc, lookups) if their output exists; use
`FORCE=1 ./runData_generation.sh` to regenerate everything.

On a cluster, run it as a **batch job** instead of on the login node (edit the `#SBATCH`
account/partition in the script for your system):
```sh
sbatch submit_runData.sh
```

## Stages & deliverables

| # | stage | script | output |
|---|-------|--------|--------|
| 1 | rhphc Fortran | `rhphc_wave_generation/make_GW_hlm_from_psi4.sh` | `psi4_dir/rhphc.N.dat`, `omega22.N.dat`, … |
| 2 | lookups | `make_lookup.py` | `bin/ylm_lookup_2D.txt`, `bin/r_lookup_2D.txt` |
| 3 | clm | `make_clm.py` | `VTKdata/gw.clm`, `VTKdata/Clm_1D.txt` |
| 4 | 2D VTK | `make_vtk.py` | `VTKdata/2D/hplus_*.vtk` |
| 5 | 1D plots | `make_1d_plots.py` | `VTKdata/clm_sum_vs_tret_{full,pos}.{png,dat}`, `each_mode_vs_tret_{full,pos}.png` |

Stage 5 plots strain vs **retarded time** `t_ret/M`. `TRET_MODE` (config.sh) chooses the range:
`pos` crops to `u>=0` (the physical signal, matching the mesh-movie start); `full` keeps the whole
record including the small negative-retarded-time lead-in; `both` (default) writes each as
`*_pos.*` / `*_full.*`.

`config.sh` → `params_gw.py` → `gwbot.py` (the `gw` object) carries the config to every
Python stage; the bash rhphc stage reads the same exported vars.

## Notes

- `legacy/` holds the old C++/memory-effect route, the analytical test source, 3D-VTK paths,
  and extra tools (green-screen 1D animation, diagnostics). Not needed for the clean path —
  in particular **do not** run `legacy/make_lookup_with_memory.py` (it `rmtree`s `VTKdata`).
- Generated data (`VTKdata/`, `psi4_dir/`, lookup tables, binaries) is gitignored; clone
  ships only source.
