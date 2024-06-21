from math import sin,cos,pi,sqrt
import numpy as np
import os.path

# This is a template for making rings of reference seeds
# Use as many centers, pairs, number of seeds per ring as necessary for you case
# Note: centers, pairs, and num_seeds_per_ring must be the same length
# Run as `python reference_seed_maker.py`

file_name = 'seeds_0'

centers = [(-8.9607884743E+000,-1.5508309988E+000, 0), (8.9604425681E+000, 1.5506292565E+000, 0), (-8.9607884743E+000,-1.5508309988E+000, 0), (8.9604425681E+000, 1.5506292565E+000, 0)] # (x, y, z) list of centers
pairs = [(2.7, 1.5), (2.7, 1.5), (0.7, 2), (0.7, 2)] # (radius, height) you can have as many pairs as you want
num_seeds_per_ring = [6, 6, 6, 6] # list containing number of seeds per ring. Must be same len as num of pairs
offset = 0.0 # possible offset. Good values to try are fractions of pi (pi/8, pi/10, pi/12, ...) 

with open(file_name + ".txt","w+") as f:
        for pair,num_seeds,center in zip(pairs, num_seeds_per_ring, centers):
                for phi in np.linspace(0+offset,2*pi+offset,num_seeds, endpoint=False):
                        xC,yC,zC = center
                        r,h = pair
                        x = xC + r * cos(phi)
                        y = yC + r * sin(phi)
                        z = zC + h
                        loc = tuple(map(str, (x,y,z,x,y,-z)))
                        f.write("%s %s %s\n%s %s %s\n" % loc)
