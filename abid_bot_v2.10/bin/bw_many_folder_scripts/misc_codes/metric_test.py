#written by eric yu 6/2022
#
#sometimes disk and/or bh shrinks unexpectedly in the 2d/3d movies
#weird numerical general relativity stuff says that this might be because of the choice of coordinates
#	(i.e. the coordinates are changing which gives the appearance of a physical effect when actually the size isn't changing)
#this script uses the components of the metric to calculate the proper circumference of certain parts of the system
#NEED:
#	-3ddata of the metric components (this code only uses gxx, gyy, gxy, psi since we've only needed to calculate this on xy plane so far)
#		-sometimes this data isn't run so you might need to ask milton to run the first folder for you, which usually is enough
#	-3ddata of density (rho_b): this is for calculation on a disk (or maybe an NS)
#	-horizon data (you will need to run setup_bh to populate bhdata): for calculatoin on a bh
#
#as said, this script calculates the proper circumference of a circle (or almost circle) of points on the xy plane
#centered at the origin
#this is because our proper length element, or ds, was calculated in spherical coordinates at z=0
#as a result, it only works with spherically symmetric systems such as single BH, accretion disk, single NS (haven't tested with last one yet)
#see this for some more math explanation: https://www.overleaf.com/read/nphpgycfxchx


from datetime import datetime, date
import numpy as np
import matplotlib
import math
matplotlib.use('Agg')
import pylab as plt
from h5loader import *
from gridder import *
np.seterr(divide='ignore', invalid='ignore')
import os

#TO DO (maybe): make get_circs() more general so that it doesn't only support a constant dphi

	
def main():
	### params to change ############################
	#there are also some parameters you may need to change in the plot() function
	#  -pertaining to all bh related plots; accuracy (see get_bhdata)
	#  -pertaining to all rho related plots; 
	#		-target_rho (density of the part of the disk whose circumference you are measruing, ask postdocs for 2d density plot or make one))
	#		-low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps: see comments above r_of_target_rho() 
	#  -pertaining to everything; numsteps (number of integration steps)
	### i tried to make it so that everything you need to tinker with is in main() and plot() but i may be dumb or there might be a new case in the future
	### try to make any changes you make to the code easy for others to pick up
	root = "/home/colten1/Desktop/metric_abid_bot/"
	metric_dir = root + "h5data/22_06_16_131253/" #folder with gxx, gyy, gxy, psi.h5 files
	rho_dir = root + "h5data/22_06_16_131253/" #first folder of 3d_data containing rho_b.h5 files
	rho_max = 2.2362990124e-4
	M_ADM =  5.2339263497e-1
	dit = 512  #it from params
	final_it = 11264 
	dt = 0.113
	#################################################
	
	rl = range(13)
	MPI = 128
	num_frames = final_it/dit + 1
	its = np.linspace(0, final_it, num_frames, dtype = int)
	savefolder = root + "bin/plotting_tool/metric_plots/"
	if not os.path.exists(savefolder): os.makedirs(savefolder)

	now = datetime.now(); current_time = now.strftime("%H%M%S")  #hour minute second    
	today = date.today(); current_date = today.strftime("%Y%m%d") #year month day
	savefol = savefolder + "out_" + current_date + current_time + "/"
	os.makedirs(savefol)

	### below make sure to set the flags to True or False when plot() is called ###
	### use comments to change whether you want to run one it or all its ###

	### to run a single it for testing ###
	plot(root, metric_dir, rho_dir, rho_max, M_ADM, dit, dt, savefol, rl, MPI, it = 0, bh_fixed_r = True, rho_fixed_r = True, rho_jagged_r = True)
				
	### to run all its ###
#	for it in its:
#		plot(root, metric_dir, rho_dir, rho_max, M_ADM, dit, dt, savefol, rl, MPI, it, bh_fixed_r = False, rho_fixed_r = True, rho_jagged_r = False)

	
		
def plot(root, metric_dir, rho_dir, rho_max, M_ADM, dit, dt, savefolder, rl, MPI, it, bh_fixed_r, rho_fixed_r, rho_jagged_r):
	tM = ( (it*1.0)/(dit*1.0) * dt ) / M_ADM  #t/M

	if bh_fixed_r:
		#####params####
		accuracy = 3
		numsteps = 2
		###############
		r_phi_list = bh_fixed_rad(root, it, numsteps, accuracy)
		coord_circ, proper_circ = get_circs(metric_dir, it, rl, MPI, r_phi_list)
		print_step(it, coord_circ, proper_circ)
		out_f = savefolder + "output_bh_fixed_r.txt"
		with open(out_f, "a+") as out:
			if len(out.readlines()) == 0:
				out.write("#t/M,coordCirc,ProperCirc\n")
			out.write(str(tM) + "," + str(coord_circ) + "," + str(proper_circ) + "\n")
			
	if rho_fixed_r:
		#########params#########
		rho_target = rho_max/100
		low_dens_rad = 0.2
		high_dens_rad = 0.8
		binsearch_threshold = 0.01
		num_linsearch_steps = 25	
		num_rho_steps = 2 #r_of_target_rho is costly, so we choose to take the average radius across fewer phis bc that part of the script takes long time
		numsteps = 2
		########################
		r_phi_list = rho_fixed_rad(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, num_rho_steps, numsteps) 
		coord_circ, proper_circ = get_circs(metric_dir, it, rl, MPI, r_phi_list)
		print_step(it, coord_circ, proper_circ)
		out_f = savefolder + "output_rho_fixed_r.txt"
		with open(out_f, "a+") as out:
			if len(out.readlines()) == 0:
				out.write("#rho_target = rho_max/" + str(int(rho_max/rho_target)) + "\n")
				out.write("#t/M,coordCirc,properCirc\n")
			out.write(str(tM) + "," + str(coord_circ) + "," + str(proper_circ) + "\n")

	if rho_jagged_r:
		#########params#########
		rho_target = rho_max/100
		low_dens_rad = 0.2
		high_dens_rad = 0.8
		binsearch_threshold = 0.01
		num_linsearch_steps = 25
		numsteps = 2
		########################
		r_phi_list = rho_jagged_rad(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, numsteps)	
		coord_circ, proper_circ = get_circs(metric_dir, it, rl, MPI, r_phi_list)
		print_step(it, coord_circ, proper_circ)
		out_f = savefolder + "output_rho_jagged_r.txt"
		with open(out_f, "a+") as out:
			if len(out.readlines()) == 0:
				out.write("#rho_target = rho_max/" + str(int(rho_max/rho_target)) + "\n")
				out.write("#t/M,coordCirc,properCirc\n")
			out.write(str(tM) + "," + str(coord_circ) + "," + str(proper_circ) + "\n")

####################################################################################################################

def get_circs(metric_dir, it, rl, MPI, r_phi_list):
	numsteps = len(r_phi_list)
	dphi = (2 * np.pi) / numsteps
	coord_circ = 0.0
	proper_circ = 0.0
	for r_phi in r_phi_list:
		r = r_phi[0]; phi = r_phi[1]
		coord_circ += dphi * r
		proper_circ += dphi * proper_length_element(metric_dir, it, rl, MPI, r, phi)
	return coord_circ, proper_circ


def proper_length_element(metric_dir, it, rl, MPI, r, phi):
	x = r * np.cos(phi); y = r * np.sin(phi)
	gxx = make_xy_grid(metric_dir, "gxx", it, rl, MPI, [x], [y], "BSSN")[0][0][0]
	gyy = make_xy_grid(metric_dir, "gyy", it, rl, MPI, [x], [y], "BSSN")[0][0][0]
	gxy = make_xy_grid(metric_dir, "gxy", it, rl, MPI, [x], [y], "BSSN")[0][0][0]
	psi = make_xy_grid(metric_dir, "psi", it, rl, MPI, [x], [y], "BSSN")[0][0][0]
	return r*np.sqrt((psi**4)*(gxx*(np.sin(phi)**2)+gyy*(np.cos(phi)**2)-2*gxy*np.sin(phi)*np.cos(phi)))


def bh_fixed_rad(root, it, numsteps, accuracy, ahnum=1):
	xy_vals = get_bhdata(root, it, accuracy, ahnum)
	r_sum = 0
	for	xy in xy_vals:
		x = xy[0]; y = xy[1]
		r_sum += np.sqrt(x**2 + y**2)

	avg_r = r_sum/len(xy_vals)
	r_phi_list = []
	for phi in np.linspace(0, 2.0*np.pi, numsteps, endpoint=False):
		r_phi_list.append((avg_r, phi)) 

	return r_phi_list


def rho_fixed_rad(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, num_rho_steps, numsteps):
	avg_r = 0.0
	for phi in np.linspace(0.0, 2.0*np.pi, num=num_rho_steps, endpoint=False):
		r = r_of_target_rho(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, phi)
		avg_r += r
		print("found target_rho at r = " + str(r) + " at phi = " + str(phi)) 

	avg_r = avg_r/num_rho_steps
	r_phi_list = []
	for phi in np.linspace(0, 2.0*np.pi, numsteps, endpoint=False):
		r_phi_list.append((avg_r, phi))

	return r_phi_list


def rho_jagged_rad(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, numsteps):
	r_phi_list = []
	for phi in np.linspace(0, 2.0*np.pi, numsteps, endpoint=False):
		r = r_of_target_rho(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, phi)
		r_phi_list.append((r, phi))		

	return r_phi_list


#int accuracy:if the z value is equal to zero up to 'accuracy' decimals, then the 
#point is considered on the xy plane  
def get_bhdata(root, it, accuracy, ahnum):
    bh_file = root + "bhdata/ht" + str(ahnum) + "_" + str(it).zfill(7) + ".3d"
    bh_f = open(bh_file, "r")
    xy_vals = []
    for i, line in enumerate(bh_f.readlines()):
        if i == 0: continue
        li = line.strip(); lis = li.split()
        x = float(lis[0]); y = float(lis[1]); z = float(lis[2])
        if np.round(z,accuracy) == 0:
            xy_vals.append((x, y))

    bh_f.close()
    return xy_vals


#finds a radius close to where the target density occurs
#	we are allowed to use a binary search because we assume that the density values of the
#	disk are already 'sorted' in the interval that we pass into this function
#	in past experience, this assumption hasn't given us any issues
#on the mentioned interval:
#	we have only used this script on disks (not any NSs yet), and on a disk at fixed azimuthal angle, as 
#	the radius increases from zero the density increases to a max value (thiccest part of donut) and then decreases again
#	you must pick an appropriate interval that contains where you think the target density occurs, take care that this interval
#	does not contain the point where drho/dr = 0, if the density values in the interval aren't all increasing or all decreasing
#	as r increases, then binary search does not work
#PARAMETERS:
#	-low_dens_rad: the bound of the interval with the lower density
#	-high_dens_rad: the bound of the interval with the higher density
#	-binsearch_threshold: binary search does binary search things until 
#			abs(high_desn_rad - low_dens_rad) < binsearch_threshold
#	-num_linsearch_steps: divides up the interval after binserach into this number
#			of evenly spaced points, point with rho closest to target rho is the final radius
#
#basically uses a binary search to narrow down a range, and does a linear search over that range
def r_of_target_rho(rho_dir, rho_target, it, rl, MPI, low_dens_rad, high_dens_rad, binsearch_threshold, num_linsearch_steps, phi):
	mid_dens_rad = low_dens_rad
	while high_dens_rad - low_dens_rad > binsearch_threshold:
		mid_dens_rad = (high_dens_rad + low_dens_rad) / 2.0
		rho_curr = make_xy_grid(rho_dir, "rho_b", it, rl, MPI, [mid_dens_rad*np.cos(phi)], [mid_dens_rad*np.sin(phi)], "MHD_EVOLVE")[0][0][0]
		if rho_curr < rho_target:
			low_dens_rad = mid_dens_rad
		elif rho_curr > rho_target:
			high_dens_rad = mid_dens_rad
		elif rho_curr == rho_target:
			print("wtf how did this happen?")
			return mid_dens_rad

	r_list = np.linspace(high_dens_rad, low_dens_rad, num_linsearch_steps);     
	min_rho_diff_radius = r_list[0]  #radius in r_list with rho closest to rho_target
	min_rho_diff = make_xy_grid(rho_dir, "rho_b",  it, rl, MPI,  [min_rho_diff_radius*np.cos(phi)], [min_rho_diff_radius*np.sin(phi)]  ,"MHD_EVOLVE")[0][0][0]
	for radius in r_list:
		rho_curr = make_xy_grid(rho_dir, "rho_b",  it, rl, MPI,  [radius*np.cos(phi)], [radius*np.sin(phi)]  ,"MHD_EVOLVE")[0][0][0]
		if abs(rho_curr - rho_target) < min_rho_diff:
			min_rho_diff_radius = radius
			min_rho_diff = rho_curr

	print("found at radius "+str(min_rho_diff_radius),flush=True)
	return min_rho_diff_radius	


def print_step(it, coord_circ, proper_circ):
	print("at it = " + str(it))
	print("coordinate circumference = " + str(coord_circ))
	print("proper circumference = " + str(proper_circ))	


####################################################################################################################
main()
