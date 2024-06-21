#python 3.9
import matplotlib.pyplot as plt
import numpy as np

#print(1)
fig=plt.figure()
ax=plt.axes(projection='3d')
ax = fig.add_subplot(projection='3d')

ptc=np.loadtxt("dat/01249.73419350000.dat")
#ptc=np.loadtxt("../../particle_seeds_0000.txt")
print(ptc[0])

for loc in ptc:
	ax.scatter(loc[1],loc[2],loc[3],marker='.',c='blue')
	#ax.scatter(loc[0],loc[1],loc[2],marker='.',c='blue')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.view_init(elev=30, azim=0)

plt.savefig("particles_plot_3D/01249.73419350000.png")

plt.close()


#--------------------------2D-------------------------------

'''for loc in ptc:
	#print((loc[1], loc[2]))
	plt.plot(loc[1],loc[2],marker='.',c='blue')
plt.xlabel("X")
plt.ylabel("Y")

plt.savefig("particles_plot_2D/01249.73419350000.png")'''