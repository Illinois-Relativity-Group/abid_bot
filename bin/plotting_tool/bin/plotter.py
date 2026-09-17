import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as plt
from h5loader import *
from gridder import *
np.seterr(divide='ignore', invalid='ignore')


def make_plot(data, x_list, y_list, title, x_label, y_label, \
		 save_file, vl=None, vh=None, cb=None):

	def extents(f):
		delta = f[1] - f[0]
		return [f[0] - delta/2, f[-1] + delta/2]

	print("plotting")
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = plt.imshow(data, interpolation='bicubic', cmap=cb, \
		extent=extents(x_list) + extents(y_list), origin='lower',\
		vmin=vl, vmax=vh)
	ax.set_aspect('equal')
	plt.colorbar(cax, orientation='vertical')
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.savefig(save_file)
	plt.close(fig)
		
	
def plot_rho_xy(h5dir, it, rl, MPI, rho_max, M_ADM, savefolder, LOG=True, vmin=None, vmax=None):
	
	x_list = np.linspace(-50.0, 50.0, 200)
	y_list = np.linspace(-50.0, 50.0, 200)

	rho, time = make_xy_grid(h5dir, "rho_b", it, rl, MPI, x_list, y_list)
	rho = np.log10(rho/rho_max) if LOG else rho/rho_max

	title = "t/M = " + str(float(time)/M_ADM)
	x_label = "x/M"
	y_label = "y/M"
	save_file = savefolder + "rho_xy_" + str(it).zfill(7) + ".png"
	make_plot(rho, x_list/M_ADM, y_list/M_ADM, title, x_label, y_label, \
		 save_file, vmin, vmax)

def plot_T_xy(h5dir, it, rl, MPI, rho_code, rho, M_ADM, savefolder, vmin=None, vmax=None):
	
	x_list = np.linspace(-50.0, 50.0, 200)
	y_list = np.linspace(-50.0, 50.0, 200)

	P_code, time = make_xy_grid(h5dir, "P", it, rl, MPI, x_list, y_list)
	
	c = 299792458 # m/s
	G = 6.674e-11 # m^3/(kg s^2)
	a = 7.565767e-16 #J/(m^3 K^4)
	
	P = rho/rho_code*P_code
	P_phys = P*c**4/G
	
	logT = .25*np.log10(np.array(3*P_phys/a, dtype=np.float64))

	title = "t/M = " + str(float(time)/M_ADM)
	x_label = "x/M"
	y_label = "y/M"
	save_file = savefolder + "T_xy_" + str(it).zfill(7) + ".png"
	make_plot(logT, x_list/M_ADM, y_list/M_ADM, title, x_label, y_label, \
		 save_file)#, vmin, vmax)


def plot_rho_xz(h5dir, it, rl, MPI, rho_max, M_ADM, savefolder):

	x_list = np.linspace(0.0, 150.0, 300)
	z_list = np.linspace(0.0, 150.0, 300)

	rho, time = make_xz_grid(h5dir, "rho_b", it, rl, MPI, x_list, z_list)
	rho = np.log10(rho/rho_max)

	title = "t/M = " + str(float(time)/M_ADM)
	x_label = "x/M"
	y_label = "z/M"
	save_file = savefolder + "rho_xz_" + str(it).zfill(7) + ".png"
	vmin = -4.0
	vmax = 0.0
	make_plot(rho, x_list/M_ADM, z_list/M_ADM, title, x_label, y_label, \
		 save_file, vmin, vmax)


def plot_b2_over_2rho(h5dir, it, rl, MPI, M_ADM, savefolder):

	x_list = np.linspace(-50.0, 50.0, 300)
	z_list = np.linspace(0.0, 100.0, 300)

	rho, time = make_xz_grid(h5dir, "rho_b", it, rl, MPI, x_list, z_list)
	smallb2, time = make_xz_grid(h5dir, "smallb2", it, rl, MPI, x_list, z_list)

	b2_over_2rho = np.log10(np.divide(smallb2, 2*rho))

	title = "t/M = " + str(float(time)/M_ADM)
	x_label = "x/M"
	y_label = "z/M"
	save_file = savefolder + "b2_over_2rho_" + str(it).zfill(7) + ".png"
	vmin = -2.0
	vmax = 2.0
	make_plot(b2_over_2rho, x_list/M_ADM, z_list/M_ADM, title, x_label, y_label, \
			 save_file, vmin, vmax, plt.cm.gist_stern)

def plot_b2(h5dir, it, rl, MPI, M_ADM, savefolder):

	x_list = np.linspace(-10.0, 10.0, 300)
	z_list = np.linspace(0, 20.0, 300)

	smallb2, time = make_xz_grid(h5dir, "smallb2", it, rl, MPI, x_list, z_list)

	b2 = np.log10(smallb2)

	title = "t/M = " + str(float(time)/M_ADM)
	x_label = "x/M"
	y_label = "z/M"
	vmin = -4.7
	vmax = -4.1
	save_file = savefolder + "b2_" + str(it).zfill(7) + ".png"
	make_plot(b2, x_list/M_ADM, z_list/M_ADM, title, x_label, y_label, \
			 save_file, vmin, vmax, plt.cm.gist_stern)


def calc_b2_over_2rho(h5dir, it, rl, MPI):
	dens=20
	
	x_list = np.linspace(-1.0,1.0, dens)
	y_list = np.linspace(-1.0,1.0,dens)
	z_list = np.linspace(11.5, 13.5, dens)

	rho, time = make_xyz_grid(h5dir, "rho_b", it, rl, MPI, x_list,y_list, z_list)
	smallb2, time = make_xyz_grid(h5dir, "smallb2", it, rl, MPI, x_list,y_list, z_list)
	
	#print(smallb2)

	b2_over_2rho = np.log10(np.divide(smallb2, 2*rho))
	#b2_over_2rho = np.divide(smallb2, 2*rho)
	avg_b2rho = b2_over_2rho[np.where(np.isfinite(b2_over_2rho))]
	N  = len(avg_b2rho)
	avg = np.average(avg_b2rho)
	
	#print(rho)
	#print(avg_b2rho)
	#for i in avg_b2rho:
	#	print(i)
	
	print(avg)
	return time, avg
'''
	total=0
	count=0
	#print(smallb2)
	for x in range(dens):
		for y in range(dens):
			for z in range(dens):
				if smallb2[x][y][z]>=0 and b2_over_2rho[x][y][z]==b2_over_2rho[x][y][z]:
					total=total+b2_over_2rho[x][y][z]
					count=count+1

	avg=total/count
'''
