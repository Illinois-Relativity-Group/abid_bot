import h5py
import numpy as np

class Data_C:


    def __init__(self, h5folder, f_prefix, prefix, var, it, rl, c):

        # filename = f_prefix + str(c) + ".h5"
        filename = var + ".file_" + str(c) + ".h5"
        f = h5py.File(h5folder + filename, 'r')
#		ds_name = 'MHD_EVOLVE::' + var +  ' it='  + str(it) + ' tl=0' + ' rl=' + str(rl) + ' c=' + str(c)
        ds_name = prefix + '::' + var + ' it=' + str(it) + ' tl=0' + ' rl=' + str(rl) + ' c=' + str(c)
        self.data = f[ds_name]
        atts = self.data.attrs
        self.level = atts['level']
        self.it = atts['timestep']
        self.time = atts['time']
        self.origin = atts['origin']
        self.iorigin = atts['iorigin']
        self.delta = atts['delta']

        self.n_arr = [ self.data.shape[2 - i] for i in range(3) ]
        self.mins = [ self.origin[i] for i in range(3) ]
        self.maxs = [ self.origin[i] + (self.n_arr[i] - 1)*self.delta[i] for i in range(3)]


    def contains(self, x_arr):
        return all([ self.mins[i] <= x_arr[i] <= self.maxs[i] for i in range(3) ])


    def get_ijk(self, x_arr):
        return [ int(round((x_arr[i] - self.mins[i])/self.delta[i])) for i in range(3) ]


    def get_data(self, x_arr):
        [ix, iy, iz] = self.get_ijk(x_arr)
        return self.data[iz][iy][ix]


    def get_closest_xyz(self, x_arr):
        ijk = self.get_ijk(x_arr)
        return [ self.mins[i] + ijk[i]*self.delta[i] for i in range(3) ]



class Dataset:


    def __init__(self, h5folder, f_prefix, prefix, var, it, rl, MPI):
        self.MPI = MPI
        self.c_list = [ Data_C(h5folder, f_prefix, prefix, var, it, rl, c) for c in range(MPI) ]
        self.delta = self.c_list[0].delta
        self.level = self.c_list[0].level
        self.it = self.c_list[0].it
        self.time = self.c_list[0].time


    def contains(self, x, y, z):
        x_arr = [x, y, z]
        for c in self.c_list:
            if c.contains(x_arr):
                return True
        return False


    def get_data(self, x, y, z):
        x_arr = [x, y, z]
        for i, c in enumerate(self.c_list):
            if c.contains(x_arr):
                if i != 0:
                    a = self.c_list.pop(i)
                    self.c_list = [a] + self.c_list
                return c.get_data(x_arr)
        print("This should never print!")


    def get_closest_xyz(self, x, y, z):
        x_arr = [x, y, z]
        for i, c in enumerate(self.c_list):
            if c.contains(x_arr):
                if i != 0:
                    a = self.c_list.pop(i)
                    self.c_list = [a] + self.c_list
                return c.get_closest_xyz(x_arr)
        print("This should never print!")


def get_h5folder(list_sorted_txt, it):
    for line in open(list_sorted_txt, 'r'):
        data = line.split()
        if int(data[0]) <= it <= int(data[1]):
            return data[3]
    print("Error: iteration out of range")
    return None
