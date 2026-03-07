import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

p = pd.read_csv('00004.37760000000.dat', delim_whitespace=True)

x1 = -1.2485443527E+001  
y1 = -2.8579732960E-001
z1 = 0.0


p['distance_from_n1'] = np.sqrt( (p['x']-x1)**2 + (p['y']-y1)**2 + (p['z']-z1)**2 )
#p['distance_from_n1'] = np.sqrt( (p['x']-x1)**2 + (p['z']-z1)**2 )

good_p = p.loc[p['distance_from_n1'] < 7.5]

good_x = good_p['x']
good_y = good_p['y']
good_z = good_p['z']

good_points = zip(good_x, good_y, good_z)

for x, y, z in good_points:
    print("{} {} {}".format(x, y, z))
    print("{} {} {}".format(x, y, -z))

plt.clf()
plt.scatter(p['x'],p['z'], color="red")
plt.scatter(good_p['x'],good_p['z'], color="green")
plt.xlim(-20, -5)
plt.ylim(-7.5, 7.5)
plt.savefig('particles.png')
