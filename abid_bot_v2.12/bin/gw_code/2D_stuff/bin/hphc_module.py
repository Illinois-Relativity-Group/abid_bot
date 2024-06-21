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

def get_lookup_3D(a):
    start = time.time()
    print("creating 3D lookups, total x vals: " + str(len(a.gw.xs_3D)))
    ylm = np.zeros((len(a.gw.xs_3D), len(a.gw.ys_3D), len(a.gw.zs_3D), a.gw.num_modes), dtype=complex)
    r = np.zeros((len(a.gw.xs_3D), len(a.gw.ys_3D), len(a.gw.zs_3D)), dtype=float)
    for i, x in enumerate(a.gw.xs_3D):
        print("at x: " + str(i))
        for j, y in enumerate(a.gw.ys_3D):
            ph = np.arctan2(y,x)
            for k, z in enumerate(a.gw.zs_3D):
                if x == 0 and y == 0: continue
                r[i,j,k] = np.sqrt(x**2+y**2+z**2)
                th = np.arccos(z/r[i,j,k])
                #if np.isnan(th): th = 0.0
                if np.isnan(th): ylm[i,j,k,:] = 0.0; continue
                l = 2; m = 2
                for mode in range(a.gw.num_modes):
                    ylm[i,j,k,mode] = calc_Ylm(l, m, th, ph)
                    if m > -l: m -= 1
                    else: l += 1; m = l
    end = time.time()
    print("lookup completed, time taken:" + str(end - start))
    return ylm, r

def get_lookup_2D(a):
    start = time.time()
    print("creating 2D lookups, total x vals: " + str(len(a.gw.xs_2D)))
    z = 0.0; th = np.arccos(0.0)
    ylm = np.zeros((len(a.gw.xs_2D), len(a.gw.ys_2D), a.gw.num_modes), dtype=complex)
    r = np.zeros((len(a.gw.xs_2D), len(a.gw.ys_2D)), dtype=float)
    for i, x in enumerate(a.gw.xs_2D):
        print("at x: " + str(i))
        for j, y in enumerate(a.gw.ys_2D):
            ph = np.arctan2(y,x)
            r[i,j] = np.sqrt(x**2+y**2+z**2)
            l = 2; m = 2
            for mode in range(a.gw.num_modes):
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

    hp_f = open(fol + "/2D/hplus_" + str(t) + ".vtk", "w")
    hc_f = open(fol + "/2D/hcross_" + str(t) + ".vtk", "w")
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
    hp_f = open(fol + "/3D/hplus_" + str(t) + ".vtk", "w")
    hc_f = open(fol + "/3D/hcross_" + str(t) + ".vtk", "w")
    hp_f.write(header); hc_f.write(header)
    hp_f.write(" ".join([str(i) for i in hp]))
    hc_f.write(" ".join([str(i) for i in hc]))
    hp_f.close(); hc_f.close()

def write_vtk_2D_grid(a):
    new_num = a.gw.xy_num_2D//20
    xs, sx = np.linspace(-a.gw.xy_max_2D, a.gw.xy_max_2D, num=new_num, retstep=True)
    ys, sy = np.linspace(-a.gw.xy_max_2D, a.gw.xy_max_2D, num=new_num, retstep=True)
    header = ("# vtk DataFile Version 3.0\nand we've done so much to deserve it\nASCII\nDATASET STRUCTURED_POINTS\n"
           "DIMENSIONS " + str(len(xs)) + " " + str(len(ys)) + " 1\n"
           "ORIGIN " + str(min(xs)) + " " + str(min(ys)) + " 0.0\n"
           "SPACING " + str(sx) + " " + str(sy) + " 0.0\n"
           "POINT_DATA " + str(len(xs)*len(ys)) + "\n"
           "SCALARS GW-FIELD float 1\nLOOKUP_TABLE default\n")

    grid_f = open(a.gw.fol_name + "/grid.vtk", "w")
    grid_f.write(header)
    grid_f.write(" ".join([str(i) for i in np.zeros(new_num*new_num)]))
    grid_f.close()

def write_vtk_2D(ylm, r, t, dt, clm, xs, ys, sx, sy, fol): 
    rt = ((t - (r/dt)).astype(int)).clip(min=0)  #see write_vtk_3D for details
    clm_ij = clm[rt,:]
    r_ji = np.einsum('ij->ji', r)
    hphc = np.einsum('ijm->ji', ylm*clm_ij)/r_ji
    scale_factor = 2000  #to scale the plane so it doesn't look flat
    hp = scale_factor * 2*np.real(hphc).flatten()
    hc = scale_factor * -2*np.imag(hphc).flatten()
    hphc_to_vtk_2D(t, hp, hc, xs, ys, sx, sy, fol)
    return np.real(hphc[0,0])

def write_vtk_3D(ylm, r, t, dt, clm, xs, ys, zs, sx, sy, sz, fol):
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
    hphc_to_vtk_3D(t, hp, hc, xs, ys, zs, sx, sy, sz, fol)
    h_max = max(np.amax(hp), np.amax(hc))
    return h_max


def gen_data(a):
    time_f = open(a.gw.fol_name + "/time_list.txt", "w")
    max_strain = 0.0
    hp_f = open(a.gw.fol_name + "/1D_hp.txt", "w")
    if a.gw.all_times: 
        times = range(0, a.gw.num_times)
    else:
        times = range(a.gw.start_time, a.gw.end_time)

    for t in times:
        time_f.write(str(t*a.gw.gw_dt))   #unretarded time
        print("gen_data at time=" + str(t))
        if a.gw.threeD:
            h_max = write_vtk_3D(a.gw.ylm_3D, a.gw.r_3D, t, a.gw.gw_dt, a.gw.clm, a.gw.xs_3D, a.gw.ys_3D, a.gw.zs_3D, a.gw.sx_3D, a.gw.sy_3D, a.gw.sz_3D, a.gw.fol_name)
            max_strain = max(max_strain, h_max)
        if a.gw.twoD:
            hp = write_vtk_2D(a.gw.ylm_2D, a.gw.r_2D, t, a.gw.gw_dt, a.gw.clm, a.gw.xs_2D, a.gw.ys_2D, a.gw.sx_2D, a.gw.sy_2D, a.gw.fol_name)
            hp_f.write(str(hp) + '\n')

    hp_f.close()
    time_f.close()
    max_strain_f = open(a.gw.fol_name + "/max_strain.txt", "w")
    max_strain_f.write(str(max_strain))
    max_strain_f.close()


# # # # # START TEST H FROM IDEALIZED SOURCES # # # # #
def get_I_rotate(t, R, M, Om):
    const = 4*M*R**2*Om**2
    Ixx = -const*np.cos(2*Om*t)
    Iyy = const*np.cos(2*Om*t)
    Ixy = const*np.sin(2*Om*t)
    Izz = np.zeros_like(t)
    Ixx[0] = 0.; Iyy[0] = 0.; Ixy[0] = 0.; Izz[0] = 0.
    return Ixx, Iyy, Ixy, Izz
def get_I_pulsate(t, R, M, Om):
    const = (4./3.)*M*R**2*Om**2*(np.cos(Om*t)+np.cos(2*Om*t))
    Ixx = -2.*const
    Iyy = const
    Ixy = np.zeros_like(t)
    Izz = const
    Ixx[0] = 0.; Iyy[0] = 0.; Ixy[0] = 0.; Izz[0] = 0.
    return Ixx, Iyy, Ixy, Izz
def get_I_ring_pulsate(t, R, M, Om):
    const = (1./6.)*M*R**2*Om**2*(np.cos(Om*t)+np.cos(2*Om*t))
    Ixx = -1.*const
    Iyy = -1.*const
    Ixy = np.zeros_like(t)
    Izz = 2.*const
    Ixx[0] = 0.; Iyy[0] = 0.; Ixy[0] = 0.; Izz[0] = 0.
    return Ixx, Iyy, Ixy, Izz

def get_hp(ph, th, Ixx, Iyy, Ixy, Izz):
    ret = ((Ixx-Iyy)/2.)*(1+np.cos(th)**2)*np.cos(2*ph)
    ret += Ixy*(1+np.cos(th)**2)*np.sin(2*ph)
    ret += (Izz - ((Ixx+Iyy)/2.))*np.sin(th)**2
    return ret

def get_hc(ph, th, Ixx, Iyy, Ixy):
    ret = ((Iyy-Ixx)/2.)*np.cos(th)*np.sin(2*ph)
    ret += Ixy*np.cos(th)*np.cos(2*ph)
    return ret

def write_vtk_test_2D(a):
    ts = np.linspace(0, a.gw.test_dt*a.gw.test_num_times, num=a.gw.test_num_times)
    X, Y = np.meshgrid(a.gw.xs_2D, a.gw.ys_2D, indexing='ij')
    ph = np.arctan2(Y,X)
    th = np.arccos(0.0)
    if a.gw.test_kind == 0: #rotate
        Ixx, Iyy, Ixy, Izz = get_I_rotate(ts, a.gw.test_R, a.gw.test_M, a.gw.test_Om)
    elif a.gw.test_kind == 1: #pulsate
        Ixx, Iyy, Ixy, Izz = get_I_pulsate(ts, a.gw.test_R, a.gw.test_M, a.gw.test_Om)
    elif a.gw.test_kind == 2: #ring_pulsate
        Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(ts, a.gw.test_R, a.gw.test_M, a.gw.test_Om)
    print("Ixx shape = " + str(Ixx.shape))
    print("Iyy shape = " + str(Iyy.shape))
    print("Ixy shape = " + str(Ixy.shape))
    print("Izz shape = " + str(Izz.shape))
    print("r shape = " + str(a.gw.r_2D.shape))
    max_strain = 0.
    scale_factor = 10000    #to raise the plane so waves are more extreme
    for t in range(a.gw.test_num_times):
        print("write vtk test time = " + str(t))
        rt = ((t - (a.gw.r_2D/a.gw.test_dt)).astype(int)).clip(min=0)
        r_ji = np.einsum('ij->ji', a.gw.r_2D)
        Ixx_ij = Ixx[rt,]; Iyy_ij = Iyy[rt,]; Ixy_ij = Ixy[rt,]; Izz_ij = Izz[rt,]
        hp = scale_factor * np.einsum('ij->ji', get_hp(ph, th, Ixx_ij, Iyy_ij, Ixy_ij, Izz_ij)) / r_ji
        hc = scale_factor * np.einsum('ij->ji', get_hc(ph, th, Ixx_ij, Iyy_ij, Ixy_ij)) / r_ji
        hphc_to_vtk_2D(t, hp.flatten(), hc.flatten(), a.gw.xs_2D, a.gw.ys_2D, a.gw.sx_2D, a.gw.sy_2D, a.gw.fol_name)
        h_max = max(np.amax(hp), np.amax(hc)); max_strain = max(max_strain, h_max)
    print("max strain = " + str(max_strain))

def write_vtk_test_3D(a):
    ts = np.linspace(0, a.gw.test_dt*a.gw.test_num_times, num=a.gw.test_num_times)
    X, Y, Z = np.meshgrid(a.gw.xs_3D, a.gw.ys_3D, a.gw.zs_3D, indexing='ij')
    ph = np.arctan2(Y,X)
    th = np.nan_to_num(np.arccos(Z/np.sqrt(X**2+Y**2+Z**2)), copy=False)
    # ph, th are of shape [i,j,k]
    if a.gw.test_kind == 0: #rotate
        Ixx, Iyy, Ixy, Izz = get_I_rotate(ts, a.gw.test_R, a.gw.test_M, a.gw.test_Om)
    elif a.gw.test_kind == 1: #pulsate
        Ixx, Iyy, Ixy, Izz = get_I_pulsate(ts, a.gw.test_R, a.gw.test_M, a.gw.test_Om)
    elif a.gw.test_kind == 2: #ring_pulsate
        Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(ts, a.gw.test_R, a.gw.test_M, a.gw.test_Om)
    # I[t], is like clm, reshape to I[rt[ijk]]
    max_strain = 0.
    for t in range(a.gw.test_num_times):
        print("write vtk test time = " + str(t))
        rt = ((t - (a.gw.r_3D/a.gw.test_dt)).astype(int)).clip(min=0)
        Ixx_ijk = Ixx[rt,]; Iyy_ijk = Iyy[rt,]; Ixy_ijk = Ixy[rt,]; Izz_ijk = Izz[rt,] #I_ijk[i,j,k]
        #t_ijk = np.full_like(r, t).astype(int)
        #Ixx_ijk = Ixx[t_ijk]; Iyy_ijk = Iyy[t_ijk]; Ixy_ijk = Ixy[t_ijk]; Izz_ijk = Izz[t_ijk]
        #print("I_ijk shape = " + str(Ixx_ijk.shape))
        normalize = 10.
        hp = np.einsum('ijk->kji', get_hp(ph, th, Ixx_ijk, Iyy_ijk, Ixy_ijk, Izz_ijk) / a.gw.r_3D)/normalize
        hc = np.einsum('ijk->kji', get_hc(ph, th, Ixx_ijk, Iyy_ijk, Ixy_ijk) / a.gw.r_3D)/normalize
        h_max = max(np.amax(hp), np.amax(hc)); max_strain = max(max_strain, h_max)
        hphc_to_vtk_3D(t, hp.flatten(), hc.flatten(), a.gw.xs_3D, a.gw.ys_3D, a.gw.zs_3D, a.gw.sx_3D, a.gw.sy_3D, a.gw.sz_3D, a.gw.fol_name)

    max_strain_f = open(a.gw.fol_name + "/max_strain.txt", "w")
    max_strain_f.write(str(max_strain))
    max_strain_f.close()
