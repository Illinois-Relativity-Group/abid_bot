from math import sin,cos,pi,sqrt
import numpy as np
import os.path

# This is a template for making rings of reference seeds
# Use as many centers, pairs, number of seeds per ring as necessary for you case
# Note: centers, pairs, and num_seeds_per_ring must be the same length
# Run as `python reference_seed_maker.py`


file_name = 'seeds_0'

#x1, y1, x2, y2 = -12.485443527,  -0.28579732960,   12.485443653,   28.579846807
#x1, y1 = 0.0, 0.0
x1, y1, x2, y2 = -1.2361902071E+01,    -7.8654707895E-01,    1.2361900642E+01,    7.8655739543E-01
#x1, y1, x2, y2 = -1.2781289234E+001,  -7.5899084720E-001,   1.2781294446E+001,   7.5899281250E-001

#x1, y1, x2, y2 = -1.2423280123E+001,  -1.0485555414E+000,   1.2423279611E+001,   1.0485652039E+000
#r1, r2, r3, r4 = 0.5, 1., 1.5, 2.
#h1, h2, h3, h4 = 4.5, 4.5, 4.5, 4.5
r1, h1, r2, h2, r3, h3 = 3, 1, 0.6, 2, 1, 2
num_per = 8
ref_z = True
#centers = [(x1, y1, 0), (x1, y1, 0), (x1, y1, 0), (x1, y1, 0)] # (x, y, z) list of centers
#pairs = [(r1, h1), (r2, h2), (r3, h3), (r4, h4)] # (radius, height) you can have as many pairs as you want
#num_seeds_per_ring = [num_per, num_per, num_per, num_per] # list containing number of seeds per ring. Must be same len as num of pairs
centers = [(x1, y1, 0), (x1, y1, 0), (x1, y1, 0), (x2, y2, 0), (x2, y2, 0), (x2, y2, 0)]
pairs = [(r1, h1), (r2, h2), (r3, h3), (r1, h1), (r2, h2), (r3, h3)]
num_seeds_per_ring = [num_per, num_per, num_per, num_per, num_per, num_per]
offset = np.pi/8 # possible offset. Good values to try are fractions of pi (pi/8, pi/10, pi/12, ...) 

with open(file_name + ".txt","w+") as f:
        for pair,num_seeds,center in zip(pairs, num_seeds_per_ring, centers):
                for phi in np.linspace(0+offset,2*pi+offset,num_seeds, endpoint=False):
                        xC,yC,zC = center
                        r,h = pair
                        x = xC + r * cos(phi)
                        y = yC + r * sin(phi)
                        z = zC + h
                        if ref_z:
                            loc = tuple(map(str, (x,y,z,x,y,-z)))
                            f.write("%s %s %s\n%s %s %s\n" % loc)
                        else:
                            loc = tuple(map(str, (x,y,z)))
                            f.write("%s %s %s\n" % loc)




