How to use:

1. ittxt.py: generate iteration list with corresponding folder to iters.txt. This is the frame list for our job.
   root: main h5 folder (without "/" at the end)
   If this doesn't work, try 
	module unload impi	(or any mpi module on your system, this is tested on frontera)
	module load hdf5

2. Main script in main_bsq2r.py and plotter.py. To change the box for calculation, change in calc_bsq_over_2rho in plotter.py.

3. Params in main_bsq2r.py:
   root: root folder for this tool.(end with plotting_tool/)
   h5dir: main h5 folder.
   rl: refinement level range.
   MPI: numbers of small files the h5 data splits into. For example, if you have smallb2_file_0 to smallb2_file_127, MPI=128.
   savefolder: where to save the result.
   You will also want to change the path in job_submit_frontera.pbs. If you are not on Frontera, you also need to change the submission part.
4. . runjobs.sh <startframe> <lastframe>
   This will automatically split your job into small jobs.
   I suggest to put less than 200 frames in one job. (I use 100)
   Startframe and lastframe should be line numbers from iters.txt

   Output of this file, the avgb2rho*.txt files, have each line of the form
   iteration \t time \t average b2rho
   keep this in mind if you want to build your own plotting tools. 
   It is unclear atm what the time is, as it is an artifact of the old code. 

5. . merge.sh 
   Automatically merge results into one file.


This tool can also plot image for single frame. Check functions in plotters.py
Plotting tools for the bsq2r for the whole case are currently under construction.

Extra scripts: the movieSeq script in bin is abids original script, should work with diagnostics.py and main.py. It doesn't work for me for unknown reason. You can try that if you have time :)

env_frontera is a quick script for setting up environment in idev on frontera.
print_density_test is used to check the density along z axis and decide where to put the box.

5th Oct., 2020



Python Plotter:
Use bsq2r_plot_python.sh to call python plotter. Remember to set the M_ADM in bin/plot_bsq2r.py
This version of data generater seems to use the old data format, so let oldversion=1.

1st May., 2021
