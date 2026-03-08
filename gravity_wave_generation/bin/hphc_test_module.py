import numpy as np
import time
from scipy.special import factorial as fact


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

def write_vtk_test_2D(gw):
    ts = np.linspace(0, gw.test_dt*gw.test_num_times, num=gw.test_num_times)
    X, Y = np.meshgrid(gw.xs_2D, gw.ys_2D, indexing='ij')
    ph = np.arctan2(Y,X)
    th = np.arccos(0.0)
    if gw.test_kind == 0: #rotate
        Ixx, Iyy, Ixy, Izz = get_I_rotate(ts, gw.test_R, gw.test_M, gw.test_Om)
    elif gw.test_kind == 1: #pulsate
        Ixx, Iyy, Ixy, Izz = get_I_pulsate(ts, gw.test_R, gw.test_M, gw.test_Om)
    elif gw.test_kind == 2: #ring_pulsate
        Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(ts, gw.test_R, gw.test_M, gw.test_Om)
    print("Ixx shape = " + str(Ixx.shape))
    print("Iyy shape = " + str(Iyy.shape))
    print("Ixy shape = " + str(Ixy.shape))
    print("Izz shape = " + str(Izz.shape))
    print("r shape = " + str(gw.r_2D.shape))
    max_strain = 0.
    scale_factor = 10000    #to raise the plane so waves are more extreme
    for t in range(gw.test_num_times):
        print("write vtk test time = " + str(t))
        rt = ((t - (gw.r_2D/gw.test_dt)).astype(int)).clip(min=0)
        r_ji = np.einsum('ij->ji', gw.r_2D)
        Ixx_ij = Ixx[rt,]; Iyy_ij = Iyy[rt,]; Ixy_ij = Ixy[rt,]; Izz_ij = Izz[rt,]
        hp = scale_factor * np.einsum('ij->ji', get_hp(ph, th, Ixx_ij, Iyy_ij, Ixy_ij, Izz_ij)) / r_ji
        hc = scale_factor * np.einsum('ij->ji', get_hc(ph, th, Ixx_ij, Iyy_ij, Ixy_ij)) / r_ji
        hphc_to_vtk_2D(t, hp.flatten(), hc.flatten(), gw.xs_2D, gw.ys_2D, gw.sx_2D, gw.sy_2D, gw.fol_name)
        h_max = max(np.amax(hp), np.amax(hc)); max_strain = max(max_strain, h_max)
    print("max strain = " + str(max_strain))

def write_vtk_test_3D(gw):
    ts = np.linspace(0, gw.test_dt*gw.test_num_times, num=gw.test_num_times)
    X, Y, Z = np.meshgrid(gw.xs_3D, gw.ys_3D, gw.zs_3D, indexing='ij')
    ph = np.arctan2(Y,X)
    th = np.nan_to_num(np.arccos(Z/np.sqrt(X**2+Y**2+Z**2)), copy=False)
    # ph, th are of shape [i,j,k]
    if gw.test_kind == 0: #rotate
        Ixx, Iyy, Ixy, Izz = get_I_rotate(ts, gw.test_R, gw.test_M, gw.test_Om)
    elif gw.test_kind == 1: #pulsate
        Ixx, Iyy, Ixy, Izz = get_I_pulsate(ts, gw.test_R, gw.test_M, gw.test_Om)
    elif gw.test_kind == 2: #ring_pulsate
        Ixx, Iyy, Ixy, Izz = get_I_ring_pulsate(ts, gw.test_R, gw.test_M, gw.test_Om)
    # I[t], is like clm, reshape to I[rt[ijk]]
    max_strain = 0.
    for t in range(gw.test_num_times):
        print("write vtk test time = " + str(t))
        rt = ((t - (gw.r_3D/gw.test_dt)).astype(int)).clip(min=0)
        Ixx_ijk = Ixx[rt,]; Iyy_ijk = Iyy[rt,]; Ixy_ijk = Ixy[rt,]; Izz_ijk = Izz[rt,] #I_ijk[i,j,k]
        #t_ijk = np.full_like(r, t).astype(int)
        #Ixx_ijk = Ixx[t_ijk]; Iyy_ijk = Iyy[t_ijk]; Ixy_ijk = Ixy[t_ijk]; Izz_ijk = Izz[t_ijk]
        #print("I_ijk shape = " + str(Ixx_ijk.shape))
        normalize = 10.
        hp = np.einsum('ijk->kji', get_hp(ph, th, Ixx_ijk, Iyy_ijk, Ixy_ijk, Izz_ijk) / gw.r_3D)/normalize
        hc = np.einsum('ijk->kji', get_hc(ph, th, Ixx_ijk, Iyy_ijk, Ixy_ijk) / gw.r_3D)/normalize
        h_max = max(np.amax(hp), np.amax(hc)); max_strain = max(max_strain, h_max)
        hphc_to_vtk_3D(t, hp.flatten(), hc.flatten(), gw.xs_3D, gw.ys_3D, gw.zs_3D, gw.sx_3D, gw.sy_3D, gw.sz_3D, gw.fol_name)

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