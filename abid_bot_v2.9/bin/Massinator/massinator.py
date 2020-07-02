###MASSINATOR###
###By Sam Qunell and Michael Mudd###
###July 2019###
import math
import numpy as np
from scipy import integrate
import sys
from mass_functions import *

# TODO: Make code more legible, comment more, check 1d more, check prebuilt geo functions
M = 0.5528972241940432
CoM_x = 0*M
CoM_z = 0*M
region_func = allspace
print(f"Mass is calculated inside the region of '{region_func.__name__}'")
def region(x,z): return region_func(x, z, 40, 4, M)
dim = sys.argv[1]
filename = sys.argv[2]

#################################################################
"""	Your code here-defaults to all data. template interiors for common shapes are below. For exterior, just flip the inequality. Recall that spherical symmetry is assumed. No boxes can be done in this method. 

	***Please test any filter used on dummy data first. Filter mistakes are common and will produce incorrect masses!***
	
	sphere with radius 1: return x<=1
	shell between r=1 and r=2: return x<=2 and x>=1
	
	Alternatively, simple geometries are provided as functions below.
	sphere of radius 1: return sphere1(x,1)
	To get the exterior of one a these region, just use negation i.e. return not sphere1(x, z, 1)
	spherical cloud between radii 1 and 2: return sphere1(x, 2) and not sphere1(x, 1)"""
def region1(x):
	return True
#################################################################


#################################################################
"""	Your code here-defaults to all data. template interiors for common shapes are below. For exterior, just flip the inequality. Recall that axial symmetry is assumed. No boxes can be done in this method. 
	
	***Please test any filter used on dummy data first. Filter mistakes are common and will produce incorrect masses!***
	
	cylinder with radius 1: return x<=1
	sphere of radius 1: return x**2+z**2<=1
	spherical cloud between radius 1 and 2: return x**2+z**2<=2 and x**2+z**2>=1
	ellipsoid of x radius 1 and z radius 2: return (x**2+(y/2)**2)<=1
	circular torus of tube radius 1 and cross section centered at (1,0): return (x-1)**2+z**2<=1
	elliptic torus with x radius of 2, z radius of 1, and cross section centered at (3,0): return ((x-3)/4)**2+z**2<=1
	
	Alternatively, simple geometries are provided as functions below.
	sphere of radius 1: return sphere2(x, z, 1)
	infinite height cylinder of radius 1: return cylinder(x, z, 1)
	cylinder of radius 1 that extends to z = 10 and z = -10: return cylinder(x, z, 1, 10)
	ellipsoid of x radius 1 and z radius 2: return ellipsoid(x, z, 1, 2)
	Note that the ellipsoid does still assume axial symmetry around z. make sure x radius = y radius
	To get the exterior of one of these regions, just use negation i.e. return not sphere2(x, z, 1)
	spherical cloud between radii 1 and 2: return sphere2(x, z, 2) and not sphere2(x, z, 1)"""
def region2(x, z):
	return True
#################################################################


#################################################################
""" Mass = Integral(Integral(2 * pi * r * rhostar * dr) * dz) """
""" A 1d integral is done for each z value to get mass at that z. Then an integral is done across all z values for total mass. Axial symmetry is obtained by integrating with a factor of 2*pi*r at each z"""
def integrate2d(zdict, zarr):
	discs = np.zeros(zarr.size)
	disc_index = 0
	for z in zarr:
		xs, ring_dens = np.zeros(zdict[z].size), np.zeros(zdict[z].size)
		index = 0
		"""Build integration arrays"""
		for pt in zdict[z]:
			xs[index] = pt[0]
			ring_dens[index] = pt[1] * pt[0] * 2 * math.pi
			index = index + 1
			
		"""Just in case debugger"""
		try:
			disc_dens = integrate.simps(ring_dens, xs)
		except:
			print('Integration failed. Terminating...')
			print(ring_dens.size, xs.size, z)
			#print(ringdens)
			#print(xs)
			exit()
		"""discs is the array of masses concentrated at each z value. It is essentially linear density in z"""
		discs[disc_index] = disc_dens
		disc_index += 1
		
	result = integrate.simps(discs, zarr)
	print('Mass: ' + str(2*result))
#################################################################


#################################################################
######################### MAIN BLOCK ############################
#################################################################

filey = open(filename, "r")	
lines = filey.readlines()

if dim == "1":
	data_list = []
	print("Reading data...")
	for line in lines:
		vals = line.split()
		x = float(vals[1])
		rho = float(vals[2])
		"""check if data point is in acceptable region"""
		if region1(x) and x >= 0 and not any(x == data[0] for data in data_list):
			"""Put data into lists first because repeatedly appending to an array is very inefficient due to how the data is stored"""
			data_list.append((x,rho))

	print("Sorting data...")
	"""Sort can possibly be upgraded for efficiency. Note that the array of tuples format was chosen solely to allow for this sort. """
	dtype = [('Xcoord', float), ('Rho', float)]
	arr_temp = np.array(data_list, dtype=dtype)
	data_sorted = np.sort(arr_temp, order='Xcoord')

	print("Integrating data...")
	xs, rhos = np.zeros(data_sorted.size), np.zeros(data_sorted.size)
	index = 0
	for pt in data_sorted:
		xs[index] = pt[0]
		rhos[index] = pt[1]
		index = index + 1
	"""Mass = Integral(4 * pi * r^2 * rhostar * dr)"""
	result = integrate.simps(xs**2 * rhos * 4 * math.pi, xs)
	print('Mass: ' + str(result))

elif dim == "2":
	zdict = {}
	zlist = []

	print("Reading data...")
	for line in lines:
		x,z,rho = map(float,line.split()[1:4])
		x -= CoM_x; z -= CoM_z

		"""check if data point is in acceptable region"""
		if region(x,z) and x >= 0:
			"""Put data into lists first because repeatedly appending to an array is very inefficient due to how the data is stored"""
			if z not in zdict:
				zdict[z] = [(x,rho)]
				zlist.append(z)
			elif not any(x == data[0] for data in zdict[z]):
				"""The following line slows the code rather considerably. The issue is that duplicate values need to be removed for successful integration, but checking through all data is quite inefficient. Better implementation needed."""
				zdict[z].append((x, rho))
	
	print("Sorting data...")				
	for z in zdict:
		"""Sort can possibly be upgraded for efficiency. Note that the array of tuples format was chosen solely to allow for this sort. """
		dtype = [('Xcoord', float), ('Rho', float)]
		zarr_temp = np.array(zdict[z], dtype=dtype)
		zsorted = np.sort(zarr_temp, order='Xcoord')
		zdict[z] = zsorted
		
	zarr = np.sort(np.array(zlist))
	
	print("Integrating data...")
	integrate2d(zdict, zarr)
