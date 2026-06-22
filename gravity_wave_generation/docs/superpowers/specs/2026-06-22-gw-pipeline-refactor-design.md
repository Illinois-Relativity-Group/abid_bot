# GW-generation pipeline refactor — clean, runnable-by-others

**Date:** 2026-06-22
**Scope:** `abid_bot_dev/gravity_wave_generation` (the Fortran-`rhphc` GW data/movie pipeline)

## Goal

Make the GW-generation pipeline runnable by an outside user on their own simulation:
edit **one** config file (paths, sim params, cutoff omega), drop their `Psi4_rad.mon.N`
into `psi4_dir/`, run **one** driver, and get every deliverable — `rhphc.*.dat` and the rest
of `psi4_dir/`, the lookup tables, `gw.clm`, the 2D `.vtk`, and the 1D strain plots.
Ship our working sol_05 values as the defaults so others have a known-good config.

## Current state & problems

Working route (Fortran):
```
Psi4_rad.mon.N  →[rhphc Fortran]→ rhphc.N.dat  →[lookups]→ ylm/r_lookup
                →[make_gw_clm]→ VTKdata/gw.clm  →[make_vtk]→ VTKdata/2D/*.vtk  →[1D plots]
```
Problems:
1. **Config duplicated across languages** — `M_ADM`, cutoff omega, NCOL live in both
   `make_GW_hlm_from_psi4.sh` (bash) and `params_gw.py` (python), and can drift.
2. **Hardcoded absolute paths** (`/anvil/scratch/x-yguo11/...`) in `params_gw.py` and the bash stage.
3. **Stale entry point** — shipped `runData_generation.sh` + `README.md` describe the *old*
   C++/"with_memory" route (`make_lookup_with_memory.py`, `make_vtk_with_memory.py` scale 15000,
   wrong `psi4_num`), not the working Fortran route.
4. **Lookup generation is a footgun** — `make_lookup_with_memory.py` conflates lookup generation
   with `shutil.rmtree(VTKdata)` (line 95) and a C++ `calc_clm` run (line 101) that writes a
   conflicting `gw.clm`. The lookup files are now gitignored, so others *must* regenerate them,
   but this script would wipe their outputs and run the wrong (C++) route.

## Design

Decided approach: **one `config.sh` of exported vars + one driver**; bash uses the vars directly,
python reads `os.environ`. No cross-language parser, one file to edit. Clean minimal path only —
optional/legacy branches (C++ `calc_clm`, memory-effect, analytical test source, 3D VTK) are set
aside, not deleted.

### 1. `config.sh` (new — the only file a user edits)
```sh
export GW_ROOT=/anvil/scratch/x-yguo11/abid_bot_dev/gravity_wave_generation
export PSI4_NUM=8           # which Psi4_rad.mon.N (extraction radius)
export M_ADM=0.0603349020955639
export OMEGA_CUT=0.342      # w_lower_cut (orbital ang. vel.), code units
export XY_MAX_2D=200
export XY_NUM_2D=500
export SCALE_FACTOR=5000
```
`NCOL`, `num_modes`, `num_times`, `r_areal`, `gw_dt` are **auto-derived from the data**
(Psi4 column count + `bin/sort.sh`) — users never set them.

### 2. `runData_generation.sh` (rewritten driver)
`source config.sh`; `mkdir -p $GW_ROOT/VTKdata/2D`; then run all five stages in order:
```
1. (cd rhphc_wave_generation && ./make_GW_hlm_from_psi4.sh)  → psi4_dir/rhphc.N.dat, omega22, ejv_GW
                                                               [requires the `rhphc` binary built; see README]
2. make_lookup.py    → bin/ylm_lookup_2D.txt, bin/r_lookup_2D.txt
3. make_clm.py       → VTKdata/gw.clm, VTKdata/Clm_1D.txt
4. make_vtk.py       → VTKdata/2D/hplus_*.vtk
5. make_1d_plots.py  → VTKdata/clm_sum_vs_tret_pos.{png,dat}, each_mode_vs_tret_pos.png
```
The rhphc stage (stage 1) is what "generate all the `psi4_dir` contents" means; it runs inside the
driver so the whole thing is one command. (A `--skip-rhphc` style guard can re-use existing
`rhphc.N.dat` if present — minor, decided at implementation.)

### 3. Per-file changes (de-hardcode + env)
- **`rhphc_wave_generation/make_GW_hlm_from_psi4.sh`**: `m_adm_val`←`$M_ADM`, `omega_val`←`$OMEGA_CUT`,
  `NCOL`←actual column count of the Psi4 file (`awk 'NR==2{print NF}'`), `psi4_dir`←`$GW_ROOT/psi4_dir`,
  loop only over `$PSI4_NUM`.
- **`params_gw.py`**: replace the hardcoded top block with `os.environ` reads (defaults = our values);
  keep the `sort.sh` auto-derivation of `num_times`/`num_modes`/`r_areal`/`gw_dt`. `gwbot.py` unchanged.
- **`make_lookup.py`** (new): only `get_lookup_2D` + `savetxt` of `ylm_lookup_2D.txt` / `r_lookup_2D.txt`
  to `bin/`. **No `rmtree`, no C++ `calc_clm`, no `Clm`/`gw.clm` writes.**
- **`make_clm.py`** (from `make_gw_clm_from_jamies_data.py`): de-hardcode paths via `gw`; unchanged math
  (reads `rhphc.N.dat`, writes `VTKdata/gw.clm`, crops `t_ret<0`).
- **`make_vtk.py`** (from `make_vtk_full.py`): `scale_factor`←`$SCALE_FACTOR`; 2D path; de-hardcode paths.
- **`make_1d_plots.py`** (from `regen_1d_plots.py`): paths via `gw`/env.

### 4. Legacy → `legacy/` (kept on disk, out of the main path, unreferenced)
`make_lookup_with_memory.py`, `make_vtk_with_memory.py`, `make_vtk_smoke.py`, the C++
`bin/calc_clm*`/`run_cpp*.sh` (+ `hphc_*`/`hplus_hcross.py` helpers), memory-effect / test-source /
3D branches, `Psi4_plot.py`, `plot_visit_stu.py`, `preview_frames.py`.

### 5. `README.md` (rewritten)
Requirements (gfortran to build `rhphc` from `ccc_ffi_hplus_hcross_ejkick.f90`; python
numpy/scipy/meshio); quickstart (edit `config.sh`, put `Psi4_rad.mon.N` in `psi4_dir/`,
`./runData_generation.sh`); a one-line description of each deliverable.

## Out of scope
- OBJ conversion + Blender render (live in `blender_gw_dev`).
- Git history rewrite to shrink the push (separate, larger task).
- 3D VTK, memory effect, analytical test source (legacy branches, re-exposable later).

## Success criteria
- A fresh user edits only `config.sh`, supplies `Psi4_rad.mon.N`, runs `./runData_generation.sh`,
  and gets `rhphc.N.dat`, the lookups, `gw.clm`, `VTKdata/2D/*.vtk`, and the 1D plots.
- No hardcoded `/anvil/scratch/x-yguo11` paths remain in the clean-path files.
- `M_ADM` / cutoff omega are set in exactly one place.
- Re-running is non-destructive (no `rmtree` of `VTKdata`).
- Our sol_05 run reproduces with the shipped defaults.
