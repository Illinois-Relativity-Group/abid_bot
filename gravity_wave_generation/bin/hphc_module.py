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
    z = 0.0; th = np.arccos(0.0) # Originally theta for (xy plane), phi for (xz plane), phi + pi/2 for (yz plane)
    ylm = np.zeros((len(gw.xs_2D), len(gw.ys_2D), gw.num_modes), dtype=complex)
    X, Y = np.meshgrid(gw.xs_2D, gw.ys_2D)
    r = np.sqrt(X**2 + Y**2)
    ph = np.arctan2(Y, X) # Originally phi for (xy plane), theta for (xz or yz plane)
    le = len(gw.xs_2D)
    printProgressBar(0, gw.num_modes, prefix = 'Generating 2D Lookup Table:', suffix = '', length = 50)
    l = 2; m = 2
    for mode in range(gw.num_modes):
        printProgressBar(mode, gw.num_modes, prefix = 'Generating 2D Lookup Table:', suffix = '', length = 50)
        ylm[:,:,mode] = calc_Ylm(l, m, th, ph)
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



def gen_data(gw):
    time_f = open(gw.fol_name + "/time_list.txt", "w")
    max_strain = 0.0
    hp_f = open(gw.fol_name + "/1D_hp.txt", "w")
    r_areal_star = gw.r_areal + 2 * gw.M_ADM * np.log((gw.r_areal / (2*gw.M_ADM)) - 1)
    xy_corner = gw.xy_max_2D*np.sqrt(2)
    xy_corner_star = xy_corner + 2 * gw.M_ADM * np.log((xy_corner / (2*gw.M_ADM)) - 1)
    if gw.all_times: 
        times = range(0, gw.num_times) 
    else:
        times = range(gw.start_time, gw.end_time)
    l = len(times)
    printProgressBar(0, l, prefix = 'Generating GW VTK Data:', suffix = '', length = 50)
    for t in times:
        printProgressBar(t + 1, l, prefix = 'Generating GW VTK Data', suffix = '', length = 50)
        time_f.write(str(t*gw.gw_dt)+'\n')   #unretarded time
        if gw.threeD:
            h_max = write_vtk_3D(gw.ylm_3D, gw.r_3D, t, gw.gw_dt, gw.clm, gw.xs_3D, gw.ys_3D, gw.zs_3D, gw.sx_3D, gw.sy_3D, gw.sz_3D, gw.fol_name, gw.plot_all_modes, gw.modes_to_plot, gw.r_areal)
            max_strain = max(max_strain, h_max)
        if gw.twoD:
            hp = write_vtk_2D(gw.ylm_2D, gw.r_2D, t, gw.gw_dt, gw.clm, gw.xs_2D, gw.ys_2D, gw.sx_2D, gw.sy_2D, gw.fol_name, gw.plot_all_modes, gw.modes_to_plot, gw.r_areal, gw.num_times)
            hp_f.write('{} {}\n'.format((t*gw.gw_dt - r_areal_star - xy_corner_star)/gw.M_ADM, hp)) ## writing to 1D file for 1D wave plot; this time corresponds to the time in the GW movie
            ## is because write_vtk_2D reutrns hp[0,0] in the corner of the grid so distance is sqrt(2)*xy_max
            
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
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd, flush=True)
    # Print New Line on Complete
    if iteration == total: 
        print()
