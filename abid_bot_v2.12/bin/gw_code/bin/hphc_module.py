import numpy as np
import time
from scipy.special import factorial as fact


### s = -2 ;spin weight -2 spherical harmonic sYlm
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

def get_lookup_3D(gw):
    start = time.time()
    print("creating 3D lookups, total x vals: " + str(len(gw.xs_3D)))
    #print("hi")
    #print(gw.num_modes)
    ylm = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D), gw.num_modes), dtype=complex)
    r = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D)), dtype=float)
    le = len(gw.xs_3D)
    printProgressBar(0, le, prefix = 'Generating 3D Lookup Table:', suffix = '', length = 50)
    for i, x in enumerate(gw.xs_3D):
        printProgressBar(i + 1, le, prefix = 'Generating 3D Lookup Table:', suffix = '', length = 50)
        for j, y in enumerate(gw.ys_3D):
            ph = np.arctan2(y,x)
            for k, z in enumerate(gw.zs_3D):
                if x == 0 and y == 0: continue
                r[i,j,k] = np.sqrt(x**2+y**2+z**2)
                th = np.arccos(z/r[i,j,k])
                #if np.isnan(th): th = 0.0
                if np.isnan(th): ylm[i,j,k,:] = 0.0; continue
                l = 2; m = 2
                for mode in range(gw.num_modes):
                    ylm[i,j,k,mode] = calc_Ylm(l, m, th, ph)
                    if m > -l: m -= 1
                    else: l += 1; m = l
    end = time.time()
    print("lookup completed, time taken:" + str(end - start))
    return ylm, r

def get_lookup_2D(gw):
    start = time.time()
    print("creating 2D lookups, total x vals: " + str(len(gw.xs_2D)))
    z = 0.0; th = np.arccos(0.0)
    ylm = np.zeros((len(gw.xs_2D), len(gw.ys_2D), gw.num_modes), dtype=complex)
    r = np.zeros((len(gw.xs_2D), len(gw.ys_2D)), dtype=float)
    le = len(gw.xs_2D)
    printProgressBar(0, le, prefix = 'Generating 2D Lookup Table:', suffix = '', length = 50)
    for i, x in enumerate(gw.xs_2D):
        printProgressBar(i + 1, le, prefix = 'Generating 2D Lookup Table:', suffix = '', length = 50)
        for j, y in enumerate(gw.ys_2D):
            ph = np.arctan2(y,x)
            r[i,j] = np.sqrt(x**2+y**2+z**2)
            l = 2; m = 2
            for mode in range(gw.num_modes):
                ylm[i,j,mode] = calc_Ylm(l, m, th, ph)
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
            hphc +=     Clm*Ylm
    #the return here is just t, not t-rt
    return np.real(hphc), np.imag(hphc)


def hphc_to_vtk_2D(t, hp, hc, xs, ys, sx, sy, fol):
    header = ("# vtk DataFile Version 3.0\nand we've done so much to deserve it\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " 1\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " 0.0\n"
           "SPACING " + str(sx) + " " + str(sy) + " 0.0\n"
           "POINT_DATA " + str(len(xs)*len(ys)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")
    #header = ("# vtk DataFile Version 3.0\nand we've done so much to deserve it\nASCII\nDATASET RECTILINEAR_GRID\n"
    #       "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " 1\n"
    #       "X_COORDINATES " + str(len(xs)) + " float\n"
    #       "Y_COORDINATES " + str(len(ys)) + " float\n"
    #       "Z_COORDINATES 1 float\n"
    #       "0.000\n\n"
    #       "POINT_DATA " + str(len(xs)*len(ys)) + "\n"
    #       "SCALARS GW-FIELD float 1\nLOOKUP_TABLE GW-FIELD\n")

    hp_f = open(fol + "/2D/hplus_" + str(t).zfill(6) + ".vtk", "w")
    hc_f = open(fol + "/2D/hcross_" + str(t).zfill(6) + ".vtk", "w")
    hp_f.write(header); hc_f.write(header)
    hp_f.write(" ".join([str(i) for i in hp]))
    hc_f.write(" ".join([str(i) for i in hc]))
    hp_f.close(); hc_f.close()


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
    grid_f.close()

def write_vtk_2D(ylm, r, t, dt, clm, xs, ys, sx, sy, fol, all_modes, modes, r_areal):
    rt = ((t - (r/dt)).astype(int)).clip(min=0)  #see write_vtk_3D for details
    clm_ij = clm[rt,:]
    r_ji = np.einsum('ij->ji', r)
    if all_modes == True:
        hphc = np.einsum('ijm->ji', ylm*clm_ij)/r_ji  #Plotting just h
        #hphc = np.einsum('ijm->ji', ylm*clm_ij) #Plotting rxh
    else:  #plot chosen mode
        hphc = (ylm*clm_ij)[...,modes[0]]
        for m in range(1,len(modes)):
            hphc += (ylm*clm_ij)[...,modes[m]]
        hphc = np.einsum('ij->ji', hphc)/r_ji  #Plotting just h
        #hphc = np.einsum('ij->ji', hphc)    #Plotting rxh

    scale_factor = 5000  #to scale the plane so it doesn't look flat
    hp = scale_factor * 2*np.real(hphc).flatten()
    hc = scale_factor * -2*np.imag(hphc).flatten()
    hphc_to_vtk_2D(t, hp, hc, xs, ys, sx, sy, fol)
    return np.real(hphc[0,0])

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


def gen_data(gw):
    time_f = open(gw.fol_name + "/time_list.txt", "w")
    max_strain = 0.0
    hp_f = open(gw.fol_name + "/1D_hp.txt", "w")
    if gw.all_times: 
        times = range(0, gw.num_times)
    else:
        times = range(gw.start_time, gw.end_time)
    l = len(times)
    printProgressBar(0, l, prefix = 'Generating GW VTK Data:', suffix = '', length = 50)
    for t in times:
        printProgressBar(t + 1, l, prefix = 'Generating GW VTK Data', suffix = '', length = 50)
        time_f.write(str(t*gw.gw_dt))   #unretarded time
        if gw.threeD:
            h_max = write_vtk_3D(gw.ylm_3D, gw.r_3D, t, gw.gw_dt, gw.clm, gw.xs_3D, gw.ys_3D, gw.zs_3D, gw.sx_3D, gw.sy_3D, gw.sz_3D, gw.fol_name, gw.plot_all_modes, gw.modes_to_plot, gw.r_areal)
            max_strain = max(max_strain, h_max)
        if gw.twoD:
            hp = write_vtk_2D(gw.ylm_2D, gw.r_2D, t, gw.gw_dt, gw.clm, gw.xs_2D, gw.ys_2D, gw.sx_2D, gw.sy_2D, gw.fol_name, gw.plot_all_modes, gw.modes_to_plot, gw.r_areal)
            hp_f.write(str(hp) + '\n')

    hp_f.close()
    time_f.close()
    max_strain_f = open(gw.fol_name + "/max_strain.txt", "w")
    max_strain_f.write(str(max_strain))
    max_strain_f.close()






# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
