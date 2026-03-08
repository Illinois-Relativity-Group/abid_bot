import numpy as np
import time
from gwbot import gw
import sys
from multiprocessing import Pool
from contextlib import closing
from scipy.special import factorial as fact

def calc_l_d_ms(l, m, theta, s=-2):
    sint = np.sin(theta/2); cost = np.cos(theta/2)
    k_i = np.maximum(0, m-s); k_f = np.minimum(l+m, l-s)
    pt1 = np.sqrt(fact(l+m)*fact(l-m)*fact(l+s)*fact(l-s))
    pt2 = 0.0
    for k in range(k_i, k_f+1, 1):
        num = ((-1)**k)*(sint**(2*k+s-m))*(cost**(2*l+m-s-2*k))
        den = fact(k)*fact(l+m-k)*fact(l-s-k)*fact(s-m+k)
        pt2 += num/den
    return pt1 * pt2


def calc_Ylm(l, m, theta, phi, s=-2):
    coeff = ((-1)**s)*np.sqrt((2*l+1)/(4*np.pi))*calc_l_d_ms(l,m,theta)
    re = coeff*np.cos(m*phi)
    im = coeff*np.sin(m*phi)
    return re+im*1j

def hphc_to_vtk_2D(t, hp, hc, xs, ys, sx, sy, fol, hp_mem, plot_memory_effect):
    header = ("# vtk DataFile Version 3.0\nand we've done so much to deserve it\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " 1\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " 0.0\n"
           "SPACING " + str(sx) + " " + str(sy) + " 0.0\n"
           "POINT_DATA " + str(len(xs)*len(ys)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")

    hp_f = open(fol + "/2D/hplus_" + str(t).zfill(6) + ".vtk", "w")
    #hc_f = open(fol + "/2D/hcross_" + str(t).zfill(6) + ".vtk", "w")
    hp_f.write(header); #hc_f.write(header)
    hp_f.write(" ".join([str(i) for i in hp]))
    if plot_memory_effect:
        hp_f.write("\n" + "\n")
        hp_f.write("SCALARS GW-MEM float 1\nLOOKUP_TABLE default\n")
        hp_f.write(" ".join([str(i) for i in hp_mem]))
    #hc_f.write(" ".join([str(i) for i in hc]))
    hp_f.close(); #hc_f.close()

def hphc_to_vtk_3D(t, hp, hc, xs, ys, zs, sx, sy, sz, fol):
    header = ("# vtk DataFile Version 3.0\nand we've done so much to deserve it\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " " + str(len(zs)) + "\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " " + str(min(zs)) + "\n"
           "SPACING " + str(sx) + " " + str(sy) + " " + str(sz) + "\n"
           "POINT_DATA " + str(len(xs)*len(ys)*len(zs)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")
    hp_f = open(fol + "/3D/hplus_" + str(t).zfill(6) + ".vtk", "w")
    hc_f = open(fol + "/3D/hcross_" + str(t).zfill(6) + ".vtk", "w")
    hp_f.write(header); hc_f.write(header)
    hp_f.write(" ".join([str(i) for i in hp]))
    hc_f.write(" ".join([str(i) for i in hc]))
    hp_f.close(); hc_f.close()

def write_vtk_2D_grid(gw):
    new_num = gw.xy_num_2D//20
    xs, sx = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=new_num, retstep=True)
    ys, sy = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=new_num, retstep=True)
    header = ("# vtk DataFile Version 3.0\nand we've done so much to deserve it\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " 1\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " 0.0\n"
           "SPACING " + str(sx) + " " + str(sy) + " 0.0\n"
           "POINT_DATA " + str(len(xs)*len(ys)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")

    grid_f = open(gw.fol_name + "/grid.vtk", "w")
    grid_f.write(header)
    grid_f.write(" ".join([str(i) for i in np.zeros(new_num*new_num)]))
    if gw.plot_memory_effect:
        grid_f.write("\n" + "\n")
        grid_f.write("SCALARS GW-MEM float 1\nLOOKUP_TABLE default\n")
        grid_f.write(" ".join([str(i) for i in np.zeros(new_num*new_num)]))
    grid_f.close()

def write_vtk_2D(ylm, r, t, dt, clm, xs, ys, sx, sy, fol, all_modes, modes, r_areal, num_times, dmemory, clm20, clm40, ylm20, ylm40, gw_root, plot_memory_effect):
    rt = ((t - (r - r_areal/dt)).astype(int)).clip(min=0)  #see write_vtk_3D for details
    rt[rt > num_times - 1] = num_times - 1
    clm_ij = clm[rt,:]
    r_ji = np.einsum('ij->ji', r)
    if all_modes == True:
        hphc = np.einsum('ijm->ji', ylm*clm_ij)/r_ji  #Plotting just h
        hphc_1d = np.einsum('ijm->ji', ylm*clm_ij)    #Plotting rxh
        #hphc = np.einsum('ijm->ji', ylm*clm_ij) #Plotting rxh
    else:  #plot chosen mode
        hphc = (ylm*clm_ij)[...,modes]
        # for m in range(1,len(modes)):
        #     hphc += (ylm*clm_ij)[...,modes[m]]
        hphc = np.einsum('ij->ji', hphc)/r_ji  #Plotting just h
        #hphc = np.einsum('ij->ji', hphc)    #Plotting rxh

    scale_factor = 15000 #20000 #30000  #to scale the plane so it doesn't look flat (default 5000)
    
    if plot_memory_effect:
        rtmem = (rt + dmemory).clip(min=0, max=num_times - 1)
        hp20 = (clm20[rtmem]*ylm20/r).T
        hp40 = (clm40[rtmem]*ylm40/r).T
        hp = scale_factor * (2*(np.real(hphc + hp20 + hp40))).T.flatten()
        hp_mem = scale_factor * (2*np.real(hp20 + hp40)).flatten()
        hc = scale_factor * -2*np.imag(hphc).flatten()
        hphc_1d = (np.real(hphc_1d + clm20[rtmem]*ylm20 + clm40[rtmem]*ylm40)).flatten()
        hphc_to_vtk_2D(t, hp, hc, xs, ys, sx, sy, fol, hp_mem, plot_memory_effect)
        out = hphc[0,0] + hp20[0,0] + hp40[0,0]
    else:
        hp = scale_factor * 2*np.real(hphc).T.flatten()
        hc = scale_factor * -2*np.imag(hphc).flatten()
        hphc_1d = (np.real(hphc_1d)).flatten()
        hphc_to_vtk_2D(t, hp, hc, xs, ys, sx, sy, fol, hp_mem=None, plot_memory_effect=False)
        out = hphc[0,0]
    return (t, hphc_1d[0], np.real(out))

def write_vtk_3D(ylm, r, t, dt, clm, xs, ys, zs, sx, sy, sz, fol, all_modes, mode, r_areal):
    # gives a 'retarded time index' for the clm array
    #     needs to be int to reindex clm[t,mode] -> clm[rt[i,j,k], mode]
    #     clip sets all negative values to 0 so doesn't go out of index
    rt = ((t - (r/dt)).astype(int)).clip(min=0)  #r is r[i,j,k], so this is rt[i,j,k]
    clm_ijk = clm[rt,:]   #becomes clm_ijk[i,j,k,mode], same shape as ylm
    r_kji = np.einsum('ijk->kji', r)
    # sum over modes column (u should learn einsum if u haven't already)
    #      order is reversed b/c vtk requires the flattened array to be indexed like
    #      kji = (k*num_y+j)*num_y+i; a[kji]
    if all_modes == True:
        hphc = np.einsum('ijkm->kji',ylm*clm_ijk)/r_kji    #Plotting just h
        #hphc = np.einsum('ijkm->kji',ylm*clm_ijk)   #Plotting rxh
    else:  #plot chosen mode
        hphc = (ylm*clm_ijk)[...,modes[0]]
        for m in range(1,len(modes)):
            hphc += (ylm*clm_ijk)[...,modes[m]]
        hphc = np.einsum('ijk->kji',hphc)/r_kji    #Plotting just h
        #hphc = np.einsum('ijk->kji',hphc)   #Plotting rxh

    hp = 2*np.real(hphc).flatten()
    hc = -2*np.imag(hphc).flatten()
    hphc_to_vtk_3D(t, hp, hc, xs, ys, zs, sx, sy, sz, fol)
    h_max = max(np.amax(hp), np.amax(hc))
    return h_max


print(gw.M_ADM)
#start_time = sys.argv[1]
#end_time = sys.argv[2]
#job_num = sys.argv[3]
start_time = 0
end_time = gw.num_times - 1
gw.xs_2D, gw.sx_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=gw.xy_num_2D, retstep=True)
gw.ys_2D, gw.sy_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=gw.xy_num_2D, retstep=True)
#gw.num_modes = 77
gw.ylm_2D = np.loadtxt(gw.bin_dir + "/ylm_lookup_2D.txt", dtype=complex).reshape(len(gw.xs_2D), len(gw.ys_2D), gw.num_modes)
gw.r_2D = np.loadtxt(gw.bin_dir + "/r_lookup_2D.txt", dtype=float).reshape(len(gw.xs_2D), len(gw.ys_2D))
gw.clm_file = gw.root + "/VTKdata/gw.clm"
gw.clm = np.loadtxt(gw.clm_file, dtype=complex)
#gw.gw_dt = 1.2
if gw.plot_memory_effect:
    for mode, mem_file in zip(gw.memory_modes, gw.memory_files):
        l, m = int(str(mode)[0]), int(str(mode)[1])
        globals()[f"ylm{l}{m}"] = calc_Ylm(l, m, np.pi/2, 0.0)
        globals()[f"clm{l}{m}"] = np.loadtxt(mem_file, dtype=float)[:, 1] / gw.M_ADM
    gw.dmemory = min(len(clm20), len(clm40)) - len(gw.clm)
else: 
    gw.dmemory = 0.0
    for mode, mem_file in zip(gw.memory_modes, gw.memory_files):
        l, m = int(str(mode)[0]), int(str(mode)[1])
        globals()[f"ylm{l}{m}"] = 0.0
        globals()[f"clm{l}{m}"] = 0.0

print(gw.M_ADM)
max_strain = 0.0
r_areal_star = gw.r_areal + 2 * gw.M_ADM * np.log((gw.r_areal / (2*gw.M_ADM)) - 1)
xy_corner = gw.xy_max_2D*np.sqrt(2)
xy_corner_star = xy_corner + 2 * gw.M_ADM * np.log((xy_corner / (2*gw.M_ADM)) - 1)

times = range(int(start_time), int(end_time)+1)
l = len(times)

def run_single_time(t):
    t_val, hphc_1d_val, hp = write_vtk_2D(gw.ylm_2D, gw.r_2D, t, gw.gw_dt, gw.clm, gw.xs_2D, gw.ys_2D, gw.sx_2D, gw.sy_2D, gw.root + "/VTKdata", gw.plot_all_modes, gw.modes_to_plot, gw.r_areal, gw.num_times, gw.dmemory, clm20, clm40, ylm20, ylm40, gw.root, gw.plot_memory_effect)
    print(f'Processed time = {t}', flush=True)
    return (t_val, hphc_1d_val)

if __name__ == '__main__':
    with closing(Pool(processes=32)) as pool:
        result = pool.map(run_single_time, times)
        pool.terminate()
    # Sort results by time and write to file in order
    result.sort(key=lambda x: x[0])
    with open(gw.root + "/VTKdata/hphc_1d.txt", "w") as f:
        for t, hphc_1d_val in result:
            f.write(f"{t} {hphc_1d_val}\n")
