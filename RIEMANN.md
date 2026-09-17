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
- **`setup_spinvtk_*.py` sort `bh1_cm_*.txt` numerically.** `setmovie.py` names
  those with the same `"{:07.2f}"` as `time_*.txt`, which pads to four integer
  digits, so past t/M 10000 a plain `.sort()` puts `bh1_cm_10001.36.txt` before
  `bh1_cm_9995.52.txt`. The loop index becomes `spin_%04d.vtk`, so every frame
  in such a folder got another frame's spin vector. This is the same defect as
  the `time_*.txt` one below, in a second place, and it is on by default
  (`spin_dimless=true`, `PlotSpinVec=1`). Fixed in all three variants.
- `setmovie.py` no longer imports `distutils`, which left the stdlib in Python
  3.12 and only resolves there when setuptools happens to shim it.
- Run scripts `return` rather than `exit` on a bad `$root`: they are sourced, so
  an `exit` closed the user's shell.
- `clean_h5folders.sh` refuses to run with `$root` unset (it did
  `rm -rf $root/xml$1/` unquoted) and moves an existing quarantine aside
  instead of deleting it. `rmdupes.py` does the same.
- `h5data/link_h5data.sh` refuses to link `h5data` into itself, never `rm -rf`s
  a real directory out of `bad_data/`, and no longer auto-releases quarantined
  folders -- `rmdupes.py` puts *duplicates* there too, and they pass the
  "has .h5 again" test, so releasing on it brought duplicate frames back.
- `runSingle.sh`/`runLocal.sh` stop with an error when `foldernum` or `ranknum`
  is empty. They have no `firstFolder`..`lastFolder` to fall back on, so an
  empty selector rendered nothing and looked like a clean run.
- `runMisc.sh` honours the `setN` argument like the other run scripts, and
  ships with all three of its flags off -- it had `fly_around_flag=1` armed
  against a hardcoded folder name from another case.
- - `setup_params.py` derives `offset`, needs no `pip install`, and will not
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
- 23 inherited files still carry another user's Anvil or Frontera scratch
  paths. None is reachable from the documented workflow, and none has been
  exercised here. Fifteen of them are under
  `bin/bw_many_folder_scripts/misc_codes/`, which is an unsorted drawer of
  one-off scripts; the rest are `copy_data.sh`,
  `compute_spinvec_start.ipynb`, `bin/particle_code/particlePicker.py`,
  the two in `bin/particle_tracer/`, `bin/plotting_tool/bin/main.py`, and a
  comment in `bin/bw_many_folder_scripts/movieSeq_v2_arg.bash`. Edit the paths
  before using any of them.
  Find them again with:
  `grep -rln -E '/anvil/|/scratch/|/work2/' .`
