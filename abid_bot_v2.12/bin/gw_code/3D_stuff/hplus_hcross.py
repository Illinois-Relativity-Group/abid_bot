import numpy as np
#from math import factorial as fact
from scipy.special import factorial as fact
from sys import argv
import os
import time



#NOTES ON IMPLMENETATION
#
# write a function that applies the radial time retardation
#   such that r = 0 is the time from the original Psi4 file
#   and for greater r, the time is 'time - r'
# general time retardation
#   the time at r = 0 is the time from the source minus the extraction radius of the Psi4 file
#
# once you have a set of hc and hp at times of the Psi4 file, with time retardation within the grid taken into account
#   have a function that finds the correct hp or hc .vtk file for a given time in the source movie (this step can account for general time retardation)
#   then you can make a list of the .vtk files that correspond to each frame in the source movie
#   and can launch a job to combine the two plots
#   the .vtk file may have to be 'down sized' so that the source's size is exagerrated in the final movie
#
#
# instead of shifting, just gen the .vtk files like old script does, and then rename / move them to match up with source movie

root = str(argv[1]) #don't end with slash (though i don't think it matters)
fol_name = str(argv[2]) # where the data is saved
dt = float(argv[3])      #dt from Psi4
num_modes = int(argv[4]) #comes from number of columns in Psi4
num_times = int(argv[5]) #num rows in Psi4
xy_max = int(argv[6]) #(X,Y) is squared grid, range from (-xy_max, xy_max), this is postiive
xy_num = int(argv[7]) #like xs = np.linspace(-xy_max, xy_max, xy_num)
z_min = int(argv[8]) 
z_max = int(argv[9])
z_num = int(argv[10])  #like zs = np.linspace(z_min, z_max, z_num)
test_flag=int(argv[11])
test_num_times=int(argv[12])
test_dt=float(argv[13])
test_kind = int(argv[14])
test_R = float(argv[15])
test_M = float(argv[16])
test_Om = float(argv[17])
update_lookup = int(argv[18])
start_num = int(argv[19])
end_num = int(argv[20])

clm_file = fol_name + "/Clm" 



# https://visit-sphinx-github-user-manual.readthedocs.io/en/develop/data_into_visit/VTKFormat.html


def main():
    start_TOT = time.time()
    # create grid
    xs, sx = np.linspace(-xy_max, xy_max, num=xy_num, retstep=True)  #from low to high
    ys, sy = np.linspace(-xy_max, xy_max, num=xy_num, retstep=True)
    zs, sz = np.linspace(z_min, z_max, num=z_num, retstep=True)
    # load, reshape, and prepare clm array    
    clm_f = np.loadtxt(clm_file, dtype=float)
    clm_f_reshape = np.reshape(clm_f, (num_times, num_modes, 2))
    clm = clm_f_reshape[:,:,0] + clm_f_reshape[:,:,1]*1j
     
    if update_lookup: #this is slow for a fine grid, also just slow, np-ize it
         ylm, r = get_lookup(xs, ys, zs, num_modes)
         np.savetxt("ylm_lookup.txt", ylm.reshape(ylm.shape[0], -1))
         np.savetxt("r_lookup.txt", r.reshape(r.shape[0], -1))
    else:
        ylm = np.loadtxt("ylm_lookup.txt", dtype=complex).reshape(len(xs), len(ys), len(zs), num_modes)
        r = np.loadtxt("r_lookup.txt", dtype=float).reshape(len(xs), len(ys), len(zs))

    if test_flag: #not functional and fast yet; need 1/r and t->rt and to speed up?
        write_vtk_test(test_dt, test_num_times, xs, ys, zs, sx, sy, sz, test_kind, test_R, test_M, test_Om, fol_name)
    else:
        gen_data(dt, start_num, min(end_num, num_times), clm, xs, ys, zs, sx, sy, sz, num_modes, fol_name, ylm, r)
    end_TOT = time.time()
    print("python done, time taken: " + str(end_TOT - start_TOT))


s = -2 #spin weight -2 spherical harmonic sYlm
def calc_l_d_ms(l, m, theta):
    sint = np.sin(theta/2); cost = np.cos(theta/2)
    k_i = np.maximum(0, m-s); k_f = np.minimum(l+m, l-s)
    pt1 = np.sqrt(fact(l+m)*fact(l-m)*fact(l+s)*fact(l-s))
    pt2 = 0.0
    for k in range(k_i, k_f+1, 1):
        num = ((-1)**k)*(sint**(2*k+s-m))*(cost**(2*l+m-s-2*k))
        den = fact(k)*fact(l+m-k)*fact(l-s-k)*fact(s-m+k)
        pt2 += num/den
    return pt1 * pt2

def calc_Ylm(l, m, theta, phi):
    coeff = ((-1)**s)*np.sqrt((2*l+1)/(4*np.pi))*calc_l_d_ms(l,m,theta)
    re = coeff*np.cos(m*phi)
    im = coeff*np.sin(m*phi)
    return re+im*1j

def get_lookup(xs, ys, zs, num_modes):
    start = time.time()
    print("creating lookups, total x vals: " + str(len(xs)))
    ylm = np.zeros((len(xs), len(ys), len(zs), num_modes), dtype=complex)
    r = np.zeros((len(xs), len(ys), len(zs)), dtype=float)
    for i, x in enumerate(xs):
        print("at x: " + str(i))
        for j, y in enumerate(ys):
            ph = np.arctan2(y,x)
            for k, z in enumerate(zs):
                if x == 0 and y == 0: continue
                r[i,j,k] = np.sqrt(x**2+y**2+z**2)
                th = np.arccos(z/r[i,j,k])
                #if np.isnan(th): th = 0.0
                if np.isnan(th): ylm[i,j,k,:] = 0.0; continue
                l = 2; m = 2
                for mode in range(num_modes):
                    ylm[i,j,k,mode] = calc_Ylm(l, m, th, ph)
                    if m > -l: m -= 1
                    else: l += 1; m = l
    end = time.time()
    print("lookup completed, time taken:" + str(end - start))
    return ylm, r

def get_h_clm(t, clm, ylm, i, j, k, num_modes):
    for mode in range(num_modes):
        Ylm = ylm[i, j, k, mode]
        Clm = clm[t,mode]
        if mode == 0:
            hphc = Clm*Ylm
        else: 
            hphc +=	Clm*Ylm
    #the reuturn here is just t, not t-rt
    return np.real(hphc), np.imag(hphc)


def write_vtk(ylm, r, t, dt, num_times, clm, xs, ys, zs, sx, sy, sz, num_modes, fol):
    #header = ("# vtk DataFile Version 3.0\nhunters done us all a great service\nBINARY\nDATASET STRUCTURED_POINTS\n"
           #"DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " " + str(len(zs)) + "\n"
           #"ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " " + str(min(zs)) + "\n"
           #"SPACING " + str(sx) + " " + str(sy) + " " + str(sz) + "\n"
           #"POINT_DATA " + str(len(xs)*len(ys)*len(zs)) + "\n"
           #"SCALARS GW-FIELD double 1\nLOOKUP_TABLE default\n")
    header = ("# vtk DataFile Version 3.0\nhunters done us all a great service\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " " + str(len(zs)) + "\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " " + str(min(zs)) + "\n"
           "SPACING " + str(sx) + " " + str(sy) + " " + str(sz) + "\n"
           "POINT_DATA " + str(len(xs)*len(ys)*len(zs)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")

    hp_f = open(fol + "/3D/hplus_" + str(t) + ".vtk", "w")
    hc_f = open(fol + "/3D/hcross_" + str(t) + ".vtk", "w")
    hp_f.write(header); hc_f.write(header)
    # gives a 'retarded time index' for the clm array
    #     needs to be int to reindex clm[t,mode] -> clm[rt[i,j,k], mode]
    #     clip sets all negative values to 0 so doesn't go out of index
    rt = ((t - (r/dt)).astype(int)).clip(min=0)  #r is r[i,j,k], so this is rt[i,j,k]
    clm_ijk = clm[rt,:]   #becomes clm_ijk[i,j,k,mode], same shape as ylm
    r_kji = np.einsum('ijk->kji', r)
    # sum over modes column (u should learn einsum if u haven't already)
    #      order is reversed b/c vtk requires the flattened array to be indexed like
    #      kji = (k*num_y+j)*num_y+i; a[kji]
    hphc = np.einsum('ijkm->kji',ylm*clm_ijk)/r_kji
    hp = 2*np.real(hphc).flatten()
    hc = -2*np.imag(hphc).flatten()
    h_max = max(np.amax(hp), np.amax(hc))
    hp_f.write(" ".join([str(i) for i in hp]))
    hc_f.write(" ".join([str(i) for i in hc]))
    hp_f.close(); hc_f.close()
    return h_max
                 
def gen_data(dt, start_num, end_num, clm, xs, ys, zs, sx, sy, sz, num_modes, fol, ylm, r):
    time_f = open(fol + "/time_list.txt", "w")
    max_strain = 0.0
    for time in range(start_num, end_num, 1):
        time_f.write(str(time*dt))   #unretarded time
        print("gen_data at time=" + str(time))
        h_max = write_vtk(ylm, r, time, dt, num_times, clm, xs, ys, zs, sx, sy, sz, num_modes, fol)
        max_strain = max(max_strain, h_max)
    time_f.close()
    print("max strain = " + str(max_strain))

# # # # # START TEST H FROM IDEALIZED SOURCES # # # # #
def get_I_rotate(t, R, M, Om):
    const = 4*M*R**2*Om**2
    Ixx = -const*np.cos(2*Om*t)
    Iyy = const*np.cos(2*Om*t)
    Ixy = const*np.sin(2*Om*t)
    Izz = 0.
    return Ixx, Iyy, Ixy, Izz

def get_I_pulsate(t, R, M, Om):
    const = (4./3.)*M*R**2*Om**2*(np.cos(Om*t)+np.cos(2*Om*t))
    Ixx = -2.*const
    Iyy = const
    Ixy = 0.
    Izz = const
    return Ixx, Iyy, Ixy, Izz

def get_I_ring_pulsate(t, R, M, Om):
    const = (1./6.)*M*R**2*Om**2*(np.cos(Om*t)+np.cos(2*Om*t))
    Ixx = -1.*const
    Iyy = -1.*const
    Ixy = 0.
    Izz = 2.*const
    return Ixx, Iyy, Ixy, Izz

def get_hp(t, ph, th, Ixx, Iyy, Ixy, Izz):
    ret = ((Ixx-Iyy)/2.)*(1+np.cos(th)**2)*np.cos(2*ph)
    ret += Ixy*(1+np.cos(th)**2)*np.sin(2*ph)
    ret += (Izz - ((Ixx+Iyy)/2.))*np.sin(th)**2
    return ret

def get_hc(t, ph, th, Ixx, Iyy, Ixy):
    ret = ((Iyy-Ixx)/2.)*np.cos(th)*np.sin(2*ph)
    ret += Ixy*np.cos(th)*np.cos(2*ph)
    return ret

def write_vtk_test(dt, num_times, xs, ys, zs, sx, sy, sz, kind, R, M, Om, fol):
    # hedder = "# vtk DataFile Version 3.0.\nkeep at it the end is in sight\nASCII\nDATASET STRUCTURED_POINTS\n"\
    #        "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " " + str(len(zs)) + "\n"\
    #        "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " " + str(min(zs)) + "\n"\
    #        "SPACING " + str(sx) + " " + str(sy) + " " + str(sz) + "\n"\
    #        "POINT_DATA " + str(len(xs)*len(ys)*len(zs)) + "\n"\
    header = ("# vtk DataFile Version 3.0\nhunters done us all a great service\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " " + str(len(zs)) + "\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " " + str(min(zs)) + "\n"
           "SPACING " + str(sx) + " " + str(sy) + " " + str(sz) + "\n"
           "POINT_DATA " + str(len(xs)*len(ys)*len(zs)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")
    ts = np.linspace(0, dt*num_times, num=num_times)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
    ph = np.arctan2(Y,X)
    th = np.nan_to_num(np.arccos(Z/np.sqrt(X**2+Y**2+Z**2)), copy=False)
    # ph, th are of shape [i,j,k]
    if kind == 0: #rotate
        Ixx, Iyy, Ixy, Izz = get_I_rotate(ts, R, M, Om)
    elif kind == 1: #pulsate
        Ixx, Iyy, Ixy, Izz = get_I_pulsate(ts, R, M, Om)
    elif kind == 2: #ring_pulsate
        Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(ts, R, M, Om)
    # I[t], is like clm, reshape to I[rt[ijk]]

    max_strain = 0.
    for t in range(num_times):
        print("write vtk test time = " + str(t))
        hp_f = open(fol + "/3D/hplus_" + str(t) + ".vtk", "w")
        hc_f = open(fol + "/3D/hcross_" + str(t) + ".vtk", "w")
        hp_f.write(header); hc_f.write(header)
        rt = ((t - (r/dt)).astype(int)).clip(min=0)
        #print("th shape = " + str(th.shape))
        #print("ph shape = " + str(ph.shape))
        #print("rt shape = " + str(rt.shape))

        Ixx_ijk = Ixx[rt,]; Iyy_ijk = Iyy[rt,]; Ixy_ijk = Ixy[rt,]; Izz_ijk = Izz[rt,] #I_ijk[i,j,k]

        #t_ijk = np.full_like(r, t).astype(int)
        #Ixx_ijk = Ixx[t_ijk]; Iyy_ijk = Iyy[t_ijk]; Ixy_ijk = Ixy[t_ijk]; Izz_ijk = Izz[t_ijk]

        #print("I_ijk shape = " + str(Ixx_ijk.shape))
        normalize = 100.
        hp = np.einsum('ijk->kji', get_hp(t, ph, th, Ixx_ijk, Iyy_ijk, Ixy_ijk, Izz_ijk) / r)/normalize
        hc = np.einsum('ijk->kji', get_hc(t, ph, th, Ixx_ijk, Iyy_ijk, Ixy_ijk) / r)/normalize
        h_max = max(np.amax(hp), np.amax(hc)); max_strain = max(max_strain, h_max)
        #print("h shape = " + str(hp.shape))
        hp_f.write(" ".join([str(i) for i in hp.flatten()]))
        hc_f.write(" ".join([str(i) for i in hc.flatten()]))
        hp_f.close(); hc_f.close()


    print("max_strain = " + str(max_strain))
    #        "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default"
    # t = 5
    # hp_fname = fol + "/3D/hplus_" + str(t).zfill(6) + ".vtk"
    # hc_fname = fol + "/3D/hcross_" + str(t).zfill(6) + ".vtk"

    # ts = np.linspace(0, dt*num_times, num=num_times)
    # T, X, Y, Z = np.meshgrid(ts,xs,ys,zs,indexing='ij')
    # if kind == 0: #rotate
    #     Ixx, Iyy, Ixy, Izz = get_I_rotate(T, R, M, Om)
    # elif kind == 1: #pulsate
    #     Ixx, Iyy, Ixy, Izz = get_I_pulsate(T, R, M, Om)
    # elif kind == 2: #ring_pulsate
    #     Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(T, R, M, Om)
    # hp = get_hp(T, np.arctan2(Y,X), np.nan_to_num(np.arccos(Z/np.sqrt(X**2+Y**2+Z**2)), copy=False), Ixx, Iyy, Ixy, Izz)
    # hc = get_hc(T, np.arctan2(Y,X), np.nan_to_num(np.arccos(Z/np.sqrt(X**2+Y**2+Z**2)), copy=False), Ixx, Iyy, Ixy)
    # # hp = hp.reshape(num_times, len(xs)*len(ys)*len(zs))
    # # hc = hc.reshape(num_times, len(xs)*len(ys)*len(zs))
    # for t in range(num_times):
    #     print(t)
    #     hp_fname = fol + "/3D/hplus_" + str(t).zfill(6) + ".vtk"
    #     hc_fname = fol + "/3D/hcross_" + str(t).zfill(6) + ".vtk"
    #     np.savetxt(hp_fname, hp[t].flatten(), header=hedder, comments='')
    #     np.savetxt(hc_fname, hc[t].flatten(), header=hedder, comments='')

    # X, Y, Z = np.meshgrid(xs,ys,zs,indexing='ij')
    # if kind == 0: #rotate
    #     Ixx, Iyy, Ixy, Izz = get_I_rotate(t, R, M, Om)
    # elif kind == 1: #pulsate
    #     Ixx, Iyy, Ixy, Izz = get_I_pulsate(t, R, M, Om)
    # elif kind == 2: #ring_pulsate
    #     Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(t, R, M, Om)
    # hp = get_hp(t, np.arctan2(Y,X), np.arccos(np.nan_to_num(Z/np.sqrt(X**2+Y**2+Z**2), copy=False, nan=1.0)), Ixx, Iyy, Ixy, Izz)
    # hc = get_hc(t, np.arctan2(Y,X), np.arccos(np.nan_to_num(Z/np.sqrt(X**2+Y**2+Z**2), copy=False, nan=1.0)), Ixx, Iyy, Ixy)
    # hp = hp.flatten(); hc = hc.flatten()
    # np.savetxt(hc_fname, hc, header=hedder, comments='')
    # np.savetxt(hp_fname, hp, header=hedder, comments='')
    
    # hc = get_hc(t, np.arctan2(Y,X), np.arccos(z/np.sqrt(X**2+Y**2+Z**2)), Ixx, Iyy, Ixy)







if __name__ == '__main__':
    main()

