#python 3.9
import matplotlib.pyplot as plt
import numpy as np

#print(1)
fig=plt.figure()
ax=plt.axes(projection='3d')
#ax = fig.add_subplot(projection='3d')

ptc=np.loadtxt("dat/00000.00000000000.dat")
#ptc=np.loadtxt("../../particle_seeds_0000.txt")
print(ptc[0])

for loc in ptc:
	ax.scatter(loc[1],loc[2],loc[3],marker='.',c='blue')
	#ax.scatter(loc[0],loc[1],loc[2],marker='.',c='blue')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.view_init(elev=30, azim=0)

plt.savefig("particle_plot.png")


