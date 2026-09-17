import numpy as np
from h5loader import *


def make_xy_grid(h5dir, var, it, rl_list, MPI, x_list, y_list, z=0):
	print("making " + var + " grid")
	Nx = len(x_list)
	Ny = len(y_list)
	data = np.zeros((Nx, Ny))
	T = np.ones((Nx, Ny))
	for rl in reversed(rl_list):
		print("using refinement level", rl)
		D = Dataset(h5dir, var, it, rl, MPI)
		for i, x in enumerate(x_list):
			for j, y in enumerate(y_list):
				if T[i][j] and D.contains(x, y, z):
					data[i][j] = D.get_data(x, y, z)
					T[i][j] = 0
	return data, D.time


def make_xz_grid(h5dir, var, it, rl_list, MPI, x_list, z_list, y=0):
	print("making " + var + " grid")
	Nx = len(x_list)
	Nz = len(z_list)
	data = np.zeros((Nz, Nx))
	T = np.ones((Nz, Nx))
	for rl in reversed(rl_list):
		print("using refinement level", rl)
		D = Dataset(h5dir, var, it, rl, MPI)
		for i, x in enumerate(x_list):
			for k, z in enumerate(z_list):
				if T[k][i] and D.contains(x, y, z):
					data[k][i] = D.get_data(x, y, z)
					T[k][i] = 0
	return data, D.time


def make_xyz_grid(h5dir, var, it, rl_list, MPI, x_list, y_list, z_list):
	print("making " + var + " grid")
	Nx = len(x_list)
	Ny = len(y_list)
	Nz = len(z_list)
	data = np.zeros((Nz, Ny, Nx))
	T = np.ones((Nz, Ny, Nx))
	for rl in reversed(rl_list):
		print("using refinement level", rl)
		D = Dataset(h5dir, var, it, rl, MPI)
		for i, x in enumerate(x_list):
			for j, y in enumerate(y_list):
				for k, z in enumerate(z_list):
					if T[k][j][i] and D.contains(x, y, z):
						data[k][j][i] = D.get_data(x, y, z)
						T[k][j][i] = 0
	return data, D.time

def make_point_grid(h5dir, var, it, rl_list, MPI, x_list, y_list, z_list):
	print("making " + var + " grid")
	N=len(x_list)
	data = np.zeros(N)
	T=np.ones(N)

	for rl in reversed(rl_list):
		#print("using refinement level", rl)
		D = Dataset(h5dir, var, it, rl, MPI)
		for i in range(N):
			if T[i] and D.contains(x_list[i], y_list[i], z_list[i]):
				data[i] = D.get_data(x_list[i], y_list[i], z_list[i])
				T[i] = 0
				if sum(T)==0:
					return data, D.time	
	return data, D.time
