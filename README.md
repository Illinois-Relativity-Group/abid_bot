# abid_bot — riemann

VisIt visualization of GRMHD black-hole-disk simulations, set up to run on
**riemann**. Same workflow as the Anvil and Frontera trees; the differences are
listed in `RIEMANN.md`.

    git clone -b yguo/bhdisk-riemann --single-branch \
        git@github.com:Illinois-Relativity-Group/abid_bot.git
    cd abid_bot

## Before you start

Nothing to install and no modules to load. `params` puts VisIt 3.3.3
(`/data/shared/visit/bin`) on your `$PATH`, and the python here is the system
`python3` — the setup scripts are stdlib only.

Every script sources `params` itself, so you never source it by hand.
`setup.sh` and the four `run*.sh` scripts are meant to be **sourced**
(`. setup.sh`), not executed, because they export into your shell.

Renders run on this machine — there is no scheduler and no compute node.
One 1920x1080 frame takes roughly two minutes, so a 1000-frame movie is
hours of wall clock on a box other people are sharing.

## 1. Put your data in `h5data/`

Symlink or copy it in, exactly as on the other machines:

    h5data/3d_data_YY_MM_DD_HHMMSS/rho_b.file_*.h5
    h5data/bhns.xon  bhns.mon  bhns_BHspin.mon  BH_diagnostics.ah1.gp
    h5data/horizon/all_horizon/h.t*.ah1.gp

Two things that are easy to get wrong:

- Data folders **must** carry the `3d_data_` prefix.
- `BH_diagnostics.ah1.gp` is needed in **both** places — at the top of
  `h5data/` and inside `horizon/all_horizon/`. `setup_spinvtk_dimensionless.py`
  reads only the `all_horizon` copy, and if it is missing the spin vector comes
  out empty instead of erroring.

If your data is too big to live in the checkout, set `h5src` in `params` and run
`. h5data/link_h5data.sh` to build the tree above out of symlinks. That helper is
optional.

## 2. Edit `params`

The block at the top lists what to change. `setup_params.py` fills in the
physics for you once `h5data/` exists:

    python3 setup_params.py

It derives `it`, `dt`, `M`, `maxdensity`, `firstTime` and `offset`, and will not
overwrite a value you have already set.

**`offset` matters.** It is `first h5 iteration / it`. If your run does not start
at iteration 0 and `offset` is left at 0, every frame gets the wrong `t/M`.

## 3. Run setup

    . setup.sh

This cleans empty folders into `h5data/bad_data/`, builds `xml/` with one
settings folder per data folder, and generates the black hole and spin-vector
geometry. Check `xml/` afterwards — it should hold `.xml`, `.3d`, `.vtk` and
`time_*.txt` files.

For a second configuration — a different camera, a different colour map —
copy `params` to `params2` and run `. setup.sh 2`. It reads `params2` and
writes `xml2/`, leaving the first set untouched. Every run script takes the
same argument: `. runMulti.sh 2` renders the second configuration. Any suffix
works, not just `2`.

## 4. Render

    . runSingle.sh      # a few frames -- edit foldernum / ranknum first
    . runLocal.sh       # the same script, kept under the older name
    . runMulti.sh       # a movie -- edit firstFolder / lastFolder
    . runMisc.sh        # zoom / fly-over / fly-around paths

Frames land in `movies/` as `<jobName>_<folder>_<rank>_<frame>.png`, one PNG
per frame. `runLocal.sh` and `runMulti.sh` put them in
`movies/<DATE>_<jobName>/`, so each run is its own folder; `runSingle.sh` uses
`movies/<jobName>/` with no date, so repeated test renders land together and
overwrite. Swap the commented line next to `picsavefolder=` to change either.

Choose what to render with the `foldernum` and `ranknum` arrays near the top
of the script: `foldernum` lists data folders (1-indexed, in `xml/` order) and
`ranknum` lists ranks within a folder (0-indexed). Leave either empty and it
falls back — `foldernum` to the `firstFolder`..`lastFolder` range, `ranknum` to
all ranks.

riemann has no batch scheduler, so `runMulti.sh` runs `$maxParallel` VisIt
processes at once on this machine. It is a shared box — 160 cores — so raise
`maxParallel` with care.

## Adjusting the look

`rho_isoXML` sets the isosurface shells, `rho_pseudoXML` the colour map,
`view1XML` the camera. `change_view.py` swaps the view without re-running setup.

Three settings in `params` that used to be buried in `runModule.py`:

| setting | effect |
|---|---|
| `cutNormal` | clip plane normal when `cutPlot=1`. `0,-1,0` shows the back half; `0,0,1` cuts in the orbital plane. Must match your view. |
| `showTimeLabel` | `0` drops the `t/M = ...` caption, for stills |
| `transparentBG` | `1` writes PNGs with alpha instead of `$bgcolor` |

**Do not put XML comments in the `atts/*.xml` files.** VisIt's parser rejects
the file outright and silently falls back to defaults for every field.

## Debugging

Read the output stream; most failures name the file they could not find.
VisIt needs at least two data folders to form a database, so keep the first
`3d_data_*` folder present even when rendering later times.

If a run seems to hang forever, a script exception has dropped `visit -cli` to
an interactive prompt. The run scripts redirect `< /dev/null` to prevent this;
if you invoke VisIt by hand, do the same.

If a `t/M` label looks wrong, check `offset` first — it is wrong far more often
than anything else.

`RIEMANN.md` lists what this branch changed against the Anvil and Frontera
trees, including the VisIt 3.3.3 differences and the known gaps.
