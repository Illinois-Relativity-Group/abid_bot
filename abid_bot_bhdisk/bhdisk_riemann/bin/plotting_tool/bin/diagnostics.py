import numpy as np
from h5loader import *
from gridder import *
np.seterr(divide='ignore', invalid='ignore')

def create_avg_small(list_txt, rl_list, MPI, it_start, it_end, out_freq, savefolder, cm_txt):

	cm_dict = {}
	for line in open(cm_txt, 'r'):
		data = line.split()
		it = int(round(float(data[0])/5.408))*512
		cm_dict[it] = (float(data[1]), float(data[2]), float(data[3]))
	
	f = open(savefolder + "avg_b2_" + str(it_start).zfill(7) + ".txt", 'w')
	for it in range(it_start, it_end + out_freq, out_freq):
		try:
			(x_c, y_c, z_c) = cm_dict[it]	
			x_list = np.linspace(x_c - 1.0, x_c + 1.0, 20)
			y_list = np.linspace(y_c - 1.0, y_c + 1.0, 20)
			z_list = np.linspace(z_c + 1.0, z_c + 3.0, 20)
			h5dir  = get_h5folder(list_txt, it)
			print(it)


			smallb2, time = make_xyz_grid(h5dir, "smallb2", it, rl_list, 
								MPI, x_list, y_list, z_list)
			rho_b, time   = make_xyz_grid(h5dir, "rho_b", it, rl_list, MPI, x_list, 
								y_list, z_list)

			smallb2_avg  = np.average(smallb2)
			b2_over_2rho = np.log10(np.divide(smallb2, 2*rho_b))
			avg_b2rho    = b2_over_2rho[np.where(np.isfinite(b2_over_2rho))]
			N            = len(avg_b2rho)
			avg_b2rho    = np.average(avg_b2rho)

			line = str(time) + "\t" + str(smallb2_avg) + "\t" + str(avg_b2rho)  + \
				"\t" +  str(N) + "\n"
			f.write(line)
			print(line)
		except:
			print("failed for it =", it)
	f.close()


def calculate_total_mass(it, rl_list, h5dir, MPI, out_freq):

	x_list = np.linspace(-384.0, 384.0, 129)
	y_list = np.linspace(-384.0, 384.0, 129)
	z_list = np.linspace(0, 384.0, 65)

	dx = x_list[1] - x_list[0]
	dy = y_list[1] - y_list[0]
	dz = z_list[1] - z_list[0]

	rho, t = make_xyz_grid(h5dir, "rho_star", it, rl_list, MPI, x_list, y_list, z_list)

	mass = 2*np.sum(rho)*dx*dy*dz
	print("mass = ", mass)
	return mass
