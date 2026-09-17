# What differs from the Anvil and Frontera trees

riemann has no batch scheduler, no compute nodes and no `module` command, and
runs VisIt 3.3.3 rather than 3.1.4. Images render directly on the login machine.

| Anvil / Frontera | riemann |
|---|---|
| `module load visit/3.1.x` | VisIt **3.3.3** at `/data/shared/visit/bin`, put on `$PATH` by `params` |
| `module load python` | system `python3` |
| `sbatch` + a `.pbs` template | direct `visit -cli`; `runMulti.sh` uses `xargs -P $maxParallel` |
| `bin/scheduler/multirun_template_anvil` | `bin/scheduler/multirun_template_riemann` |

## Code changes the version bump forced

- **`PlotBH()` no longer adds the Delaunay operator.** VisIt 3.3.3 ships it
  disabled and `visit -cli` has no API to enable it, so `AddOperator("Delaunay")`
  raises `Invalid operator plugin name`. The horizon renders correctly without it.
- **Spin-vector attributes gained `colorByMagnitude`.** 3.3.3 renamed the 3.1.4
  `colorByMag` field and defaults the new one to `true`, which overrides
  `vectorColor` and renders the arrow blue whatever colour you asked for.
  Both names are now present so the file works on either version.
- **`PlotBox()` reads `$root`** instead of a hardcoded scratch path.

## Bug fixes carried in

- `clean_h5folders.sh` quarantines a folder when it has no `*.h5`, not when it
  has no files. Restart folders often hold only `CCTK_Proc1.out`, which passes a
  file-count test, consumes a folder index and renders nothing.
- `rmdupes.py` moves the symlink, not the data behind it. `shutil.move` resolves
  a symlinked `3d_data_*` folder and relocates the real files out of your data
  tree.
- `setup_params.py` derives `offset`, needs no `pip install`, and will not
  overwrite a value you set yourself. `dt` is derived from the widest pair of
  (iteration, time) samples in a data folder rather than the closest pair,
  since `h5dump` truncates `time` to ~6 significant figures and that rounding
  is a much larger fraction of `dt` over one step than over the whole folder.

## Known gaps

- Twelve other `atts/*.xml` files still carry only the 3.1.4 `colorByMag` field.
  They have not been exercised here; if a vector plot comes out the wrong
  colour, that is the first thing to check.
- All 146 `atts/*.xml` files parse as well-formed XML and none contains an XML
  comment. Two arrived corrupt and were repaired:
  `Vec_spin_MassiveDisk_superzoomin.xml` had a vi status line pasted into it
  followed by a second complete copy, and `bhdisk_view_10deg_superzoomin_first.xml`
  was 21 bytes of a truncated shell redirect and was removed.
- `abid_bot_bhdisk/bhdisk_riemann` on `master` is an unported SLURM tree despite
  its name. Use this branch instead.
- Four inherited auxiliary files still carry another user's Anvil scratch paths:
  `copy_data.sh`, `compute_spinvec_start.ipynb`, and the two scripts in
  `bin/particle_tracer/`. None is part of the documented workflow; edit the
  paths before using any of them.
