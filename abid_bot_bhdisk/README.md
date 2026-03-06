# Black Hole Disk Visualization

This software generates visualizations for black hole disk systems using VisIt. The package includes all necessary codes to produce images of pseudo-color plots, isosurfaces, volume renderings, and more. It also has full capability to generate visualizations of magnetized black hole and disk systems with fieldline plotting.

## Setup

Untar the tarball and copy `bhdisk.ct` to your `~/.visit` directory to ensure colortable visibility. Then open the parameter file and update the following fields: `root`, `it`, `dt`, `M`, `rho_pseudoXML`, `rho_isoXML`, and `view1XML`. You have the option to plot either spin `S` or dimensionless spin `chi`. If you want magnetized systems, turn on `fieldlines` and the relevant settings.

Next, create an `h5data` folder. Softlink or copy your HDF5 data into this folder and add a `3d_data_` prefix to all data folders — there is a script in `h5data` to help with this. From your source directory, also copy over all files starting with `bhns*`. The most important ones are `bhns_BHspin.mon` (spin vector), `bhns.*on` (center of mass), and `bhns_particles.mon` (for particle fieldline plotting; rename it to `particles.mon`). You will also need a `horizon/all_horizon` directory inside `h5data`. Copy all apparent horizon data (files ending in `.gp`) into `all_horizon`, including `BH_diagnostics.ah#.gp`, where `#` can be 1–3 depending on how many black holes are in the system and whether they have merged.

Now run setup. If you encounter errors, read through the output stream carefully. On a first run you may need to `chmod` several files to make them executable. After setup completes, check the integrity of your `root/xml` folder. It should contain your setting files (`.xml`) along with `.3d`, `.vtk`, and seedpoint files used for black hole, spin vector, and fieldline plotting.

## Plotting

Use `runSingle.sh` for single-frame plotting. You can select what to plot: isosurface or volume rendering, spin vector on/off, reflection on/off, cut on/off, and velocity arrows on/off, and others. Then specify the folder number (1-indexed) and which image within that folder to plot (0-indexed).

For batch production of movie frames, use `runMulti`. For zoom-in transitions or fly-around/fly-over camera paths for movies, use `runMisc`.

## Adjusting Plot Settings

For a new case you will likely need to adjust plotting settings based on feedback. In the pseudo-color settings, you can shift the overall color range by adjusting `min`/`max` on the colorbar. You can also modify the color control points either in the colorbar or in the plotting settings (volume rendering only). Opacity can be toggled for both volume and pseudo-color plots, and isosurface layers can be adjusted for better results.

The best way to experiment is through the GUI or by turning on legends. In `runModule`, search for "legend" — you will need to toggle it off in two places, so read through the code and experiment.

## Miscellany

Three views are provided, but they may not always fit your plot directly. Use `change_view.py` in your root directory to swap views without re-running setup.

In `h5data` there are two scripts for generating a line or a box. The box is used for zoom-in transitions — enable it by setting `plot_box` to true in `runModule` and adjusting the path there. The line works the same way and is used as a scalebar. Since we need the scalebar in units of `M`, you plot a reference line in the image. `M` has some value in solar masses, and the plotting script works in code units (also in solar masses for our simulations), so you can convert accordingly and plot the correct length for reference.

## Debugging

When you encounter a bug, read through your script carefully. In most cases (~80%) the issue is immediately obvious, and for the rest you can usually make a good guess from the error message. Errors from module loading are typically fine to ignore. Pay extra attention to VisIt complaining about files not found, especially `.vtk` files, as these can cause issues. VisIt opens data in datasets, so you need at least two data files to plot or it may fail. If you only want to plot a later `3d_data` folder, you still need the first `3d_data` folder present — this is how the code determines the correct time.

Good luck!
