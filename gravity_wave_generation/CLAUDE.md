# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A 5-stage pipeline that turns a numerical-relativity simulation's `Psi4_rad.mon.N` output
(`N` = extraction-radius index) into GW data products: `rhphc.N.dat` strains, ylm/r lookup
tables, `gw.clm`, 2D `.vtk` mesh frames, and 1D strain plots. Downstream OBJ conversion +
Blender rendering live in a separate `blender_gw_dev` project, not here.

This directory is one project inside the larger `abid_bot_dev` git repo — **the git root is the
parent directory**, not here. All paths below are relative to this `gravity_wave_generation/` dir.

## Commands

```sh
./runData_generation.sh              # run the full pipeline (stages 1-5)
FORCE=1 ./runData_generation.sh      # same, but regenerate the two slow stages too
sbatch submit_runData.sh             # cluster batch (edit #SBATCH account/partition first)
NPROC=64 python3 make_vtk.py         # NPROC caps make_vtk's process pool (default = cpu_count)
```

There is no build system, test suite, or linter — stages are run directly. To run/debug one
stage, invoke its script (`python3 make_clm.py`, `python3 make_vtk.py`, …); each reads its
config through `gwbot` (see below), so `source ./config.sh` first to set the env vars, or rely
on the in-script defaults.

Rebuild the Fortran strain calculator (only if the tracked `rhphc` binary won't run):
```sh
cd rhphc_wave_generation && gfortran -O2 -o rhphc ccc_ffi_hplus_hcross_ejkick.f90
```

## Architecture — the config-flow spine

The single most important thing to understand: **config flows `config.sh` → `params_gw.py` →
`gwbot.py`, and every Python stage starts with `from gwbot import gw`.**

- `config.sh` exports a small set of env vars (`PSI4_NUM`, `M_ADM`, `OMEGA_CUT`, `XY_MAX_2D`,
  `XY_NUM_2D`, `SCALE_FACTOR`, `TRET_MODE`, overlay flags). This is the **only file a user edits**.
- `params_gw.py` reads those env vars (with hardcoded sol_05 fallbacks), assembles a nested list
  `params_gw = [generalGWSettings, psi4Settings, gridSettings, simulationSettings, testGWSettings,
  memorySettings]`, and **prints/runs side effects at import time**.
- `gwbot.py` constructs the module-level singleton `gw = GWBot(params_gw)`, unpacking those lists
  into flat attributes (`gw.M_ADM`, `gw.num_modes`, `gw.xy_max_2D`, …). Stages mutate `gw` freely
  by attaching extra attributes at runtime (e.g. `gw.xs_2D`, `gw.ylm_2D`, `gw.clm`).
- Importing `gwbot` (hence `params_gw`) **always shells out to `bin/sort.sh`** on the Psi4 file to
  auto-derive `num_times`, `num_modes`, `r_areal`, and `gw_dt` from the data. These are NOT set by
  hand — `num_modes = (NCOL - 5) / 2`. If they look wrong, the Psi4 file / `sort.sh` is the place
  to check, not `params_gw.py`'s placeholder values.

Consequence: any change to grid size or mode count is a config change in `config.sh`, picked up
everywhere via `gw`. Don't hardcode dimensions in the stage scripts.

## Stage data flow

| # | stage | script | reads | writes |
|---|-------|--------|-------|--------|
| 1 | rhphc (Fortran) | `rhphc_wave_generation/make_GW_hlm_from_psi4.sh` | `psi4_dir/Psi4_rad.mon.N` | `psi4_dir/rhphc.N.dat`, `omega22.N.dat`, … |
| 2 | lookups | `make_lookup.py` | grid/modes from `gw` | `bin/ylm_lookup_2D.txt`, `bin/r_lookup_2D.txt` |
| 3 | clm | `make_clm.py` | `rhphc.N.dat` | `VTKdata/gw.clm`, `VTKdata/Clm_1D.txt` |
| 4 | 2D VTK | `make_vtk.py` | `gw.clm` + lookups | `VTKdata/2D/hplus_*.vtk` |
| 5 | 1D plots | `make_1d_plots.py` | `rhphc.N.dat` | `VTKdata/clm_sum_vs_tret_*.{png,dat}`, etc. |

`runData_generation.sh` **skips stages 1 and 2 if their output already exists** (the two slow
ones); `FORCE=1` forces them. Stages 3–5 always run.

Stage 1 is templated: `make_GW_hlm_from_psi4.sh` copies `ccc_ffi.input_blank` → `ccc_ffi.input`
and `sed`-substitutes the same config env vars (`OMEGA_CUT`, `M_ADM`, `PSI4_NUM`, column count)
before running the `rhphc` binary. To change Fortran inputs, edit the `*_blank` template, not the
generated `ccc_ffi.input`.

## Conventions and gotchas

- **Mode ordering** is `l=2 m=2..-2, then l=3 m=3..-3, …` (index 0 = (2,2)). This same ordering
  is reconstructed in `make_lookup.py`, `make_vtk.py`, and `make_1d_plots.py` — keep them in sync.
- **Retarded time** is the physics core. `make_vtk.py` indexes the strain by a per-pixel retarded-
  time index `rt = t - (r - r_areal_star)/dt`, where `r_areal_star` is the tortoise coordinate
  `r* = r + 2M ln(r/2M - 1)` that anchors `t_ret = 0` at the grid center on frame 0. `make_clm.py`
  zeroes strain at `tret < 0` (unphysical pre-emission). `make_1d_plots.py` plots vs `t_ret/M`.
- **`xy_max_2D` is a cross-project coupling point**: it must match the `linspace` bounds in the
  downstream `convert_vtk_to_obj.py` (in `blender_gw_dev`) or the mesh geometry won't line up.
- **`SCALE_FACTOR`** (vertical exaggeration) is baked into the `.vtk` strain values in `make_vtk.py`
  via the `SCALE_FACTOR` env var — it is not a separate render-time knob.
- All generated data (`VTKdata/`, `psi4_dir/`, lookup tables, compiled binaries) is gitignored;
  the repo ships source only. The `rhphc` binary is the one tracked binary (skip-worktree).

## legacy/ — do not use for the clean path

`legacy/` holds the old C++/`calc_clm` route, the memory-effect calculation, 3D-VTK paths, and
diagnostics. The clean pipeline does not touch it. In particular:

- **Never run `legacy/make_lookup_with_memory.py` — it `rmtree`s `VTKdata`.**
- The memory-effect (`plot_memory_effect`, `memory_modes`, `clm20`/`clm40`) and 3D (`threeD_flag`)
  branches still exist in `make_clm.py`/`make_vtk.py` but are off in the clean config; treat them
  as legacy unless explicitly working on them.
- `legacy/plot_1D_edit.py` is the historical original of the now-folded-in stage-5 overlay option
  (`MAKE_1D_OVERLAY` in `config.sh`); prefer the config flag over the standalone script.
