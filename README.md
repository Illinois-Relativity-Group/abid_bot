# abid_bot
A visualization toolkit for making images and movies of GRMHD simulations of black hole and neutron star dynamics.

update 2024-03-18: added abid_bot_v2.11
- new velocity vector plotting tech (look at the python scripts in h5data/); creates a .vtk file on specified grid that can be plotted with a flag in the run Scripts
- runLocal.sh: can run as a process on local machines like riemann; is like runSingle but doesn't submit to a job, just runs the entire visit command in serial
- lots of bug fixes and stuff; this code works (probably) and was used to create the NSNS movies/images for Jamie's 2024 paper
