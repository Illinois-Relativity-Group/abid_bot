import time
import numpy as np
from gwbot import gw
import sys, os, shutil, subprocess
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

    # build 3D grid
    X, Y, Z = np.meshgrid(gw.xs_3D, gw.ys_3D, gw.zs_3D, indexing='ij')
    # radial and angles
    r = np.sqrt(X**2 + Y**2 + Z**2)
    phi = np.arctan2(Y, X)
    # safe theta
    theta = np.arccos(np.divide(Z, r, out=np.zeros_like(Z), where=r!=0))

    # allocate
    ylm = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D), gw.num_modes), dtype=complex)

    # inline (l,m) sequence
    l = 2; m = 2
    for mode in range(gw.num_modes):
        ylm[..., mode] = calc_Ylm(l, m, theta, phi)
        if m > -l:
            m -= 1
        else:
            l += 1
            m = l

    # zero out singular axis x=y=0
    singular = (X == 0) & (Y == 0)
    r[singular] = 0.0
    ylm[singular, :] = 0.0

    print(f"lookup completed, time taken: {time.time() - start:.2f}s")
    return ylm, r

def get_lookup_2D(gw):
    start = time.time()
    print("creating 2D lookups, total x vals: " + str(len(gw.xs_2D)))

    # build 2D grid (z=0 plane)
    X, Y = np.meshgrid(gw.xs_2D, gw.ys_2D, indexing='ij')
    z = 0.0
    r = np.sqrt(X**2 + Y**2 + z**2)
    phi = np.arctan2(Y, X)
    theta = np.arccos(np.divide(z, r, out=np.zeros_like(r), where=r!=0))

    # allocate
    ylm = np.zeros((len(gw.xs_2D), len(gw.ys_2D), gw.num_modes), dtype=complex)

    # inline (l,m) sequence
    l = 2; m = 2
    for mode in range(gw.num_modes):
        ylm[..., mode] = calc_Ylm(l, m, theta, phi)
        if m > -l:
            m -= 1
        else:
            l += 1
            m = l

    # zero out singular axis x=y=0
    singular = (X == 0) & (Y == 0)
    r[singular] = 0.0
    ylm[singular, :] = 0.0

    print(f"lookup completed, time taken: {time.time() - start:.2f}s")
    return ylm, r

job_name = "VTKdata"    #folder in root containing data will be named this
fol_name = gw.root + '/' + job_name   # # #  where the data is saved
gw.fol_name = fol_name

if os.path.exists(fol_name): shutil.rmtree(fol_name)

os.mkdir(fol_name)
os.mkdir(fol_name + '/2D')
os.mkdir(fol_name + '/3D')

subprocess.run([gw.bin_dir + "/run_cpp.sh", gw.bin_dir, gw.psi4_f_sorted, str(gw.M_ADM), str(gw.cutoff_w), fol_name])

if gw.plot_memory_effect:
    for mode, mem_file in zip(gw.memory_modes, gw.memory_files):
        l, m = int(str(mode)[0]), int(str(mode)[1])
        globals()[f"ylm{l}{m}"] = calc_Ylm(l, m, np.pi/2, 0.0)
        globals()[f"clm{l}{m}"] = np.loadtxt(mem_file, dtype=float)[:, 1] / gw.M_ADM


gw.threeD = False; gw.twoD = False
if gw.threeD_flag == 1: 
    gw.threeD = True
elif gw.threeD_flag == 0: 
    gw.twoD = True
elif gw.threeD_flag == 2:
    gw.twoD = True; gw.threeD = True

# --- set up your grids ---
# 3D grid in x, y, z
gw.xs_3D, gw.sx_3D = np.linspace(-gw.xy_max_3D, gw.xy_max_3D,
                                 num=gw.xy_num_3D, retstep=True)
gw.ys_3D, gw.sy_3D = np.linspace(-gw.xy_max_3D, gw.xy_max_3D,
                                 num=gw.xy_num_3D, retstep=True)
gw.zs_3D, gw.sz_3D = np.linspace(gw.z_min_3D, gw.z_max_3D,
                                 num=gw.z_num_3D, retstep=True)

# 2D grid in x, y (z = 0 plane)
gw.xs_2D, gw.sx_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D,
                                 num=gw.xy_num_2D, retstep=True)
gw.ys_2D, gw.sy_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D,
                                 num=gw.xy_num_2D, retstep=True)


# --- lookup-generation & loading logic ---
if gw.update_lookup:
    # regenerate & save
    if gw.threeD:
        gw.ylm_3D, gw.r_3D = get_lookup_3D(gw)
        # flatten first two dims so savetxt writes (nx, ny*nz) rows
        np.savetxt(f"{gw.bin_dir}/ylm_lookup_3D.txt",gw.ylm_3D.reshape(gw.ylm_3D.shape[0], -1),fmt="%s")
        np.savetxt(f"{gw.bin_dir}/r_lookup_3D.txt",gw.r_3D.reshape(gw.r_3D.shape[0], -1),fmt="%.6e")

    if gw.twoD:
        gw.ylm_2D, gw.r_2D = get_lookup_2D(gw)
        np.savetxt(f"{gw.bin_dir}/ylm_lookup_2D.txt",gw.ylm_2D.reshape(gw.ylm_2D.shape[0], -1),fmt="%s")
        np.savetxt(f"{gw.bin_dir}/r_lookup_2D.txt",gw.r_2D.reshape(gw.r_2D.shape[0], -1),fmt="%.6e")

else:
    # load from disk
    if gw.threeD:
        gw.ylm_3D = (np.loadtxt(f"{gw.bin_dir}/ylm_lookup_3D.txt", dtype=complex).reshape(len(gw.xs_3D),len(gw.ys_3D),len(gw.zs_3D),gw.num_modes))
        gw.r_3D = (np.loadtxt(f"{gw.bin_dir}/r_lookup_3D.txt", dtype=float).reshape(len(gw.xs_3D),len(gw.ys_3D),len(gw.zs_3D)))
    if gw.twoD:
        gw.ylm_2D = (np.loadtxt(f"{gw.bin_dir}/ylm_lookup_2D.txt", dtype=complex).reshape(len(gw.xs_2D),len(gw.ys_2D),gw.num_modes))
        gw.r_2D = (np.loadtxt(f"{gw.bin_dir}/r_lookup_2D.txt", dtype=float).reshape(len(gw.xs_2D),len(gw.ys_2D)))

# if lookups are disabled, fill with zero-arrays
if not gw.threeD:
    gw.ylm_3D = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D), gw.num_modes),dtype=complex)
    gw.r_3D = np.zeros((len(gw.xs_3D), len(gw.ys_3D), len(gw.zs_3D)),dtype=float)
if not gw.twoD:
    gw.ylm_2D = np.zeros((len(gw.xs_2D), len(gw.ys_2D), gw.num_modes),dtype=complex)
    gw.r_2D = np.zeros((len(gw.xs_2D), len(gw.ys_2D)),dtype=float)

# load, reshape, and prepare clm array 
print("going dark")
gw.clm_file = gw.fol_name + "/Clm"
gw.clm_f = np.loadtxt(gw.clm_file, dtype=float)
shape = int(gw.clm_f.size / gw.num_modes / 2)
gw.clm_f_reshape = np.reshape(gw.clm_f, (shape, gw.num_modes, 2))
# gw.clm_f_reshape[:int(gw.r_areal/gw.gw_dt), :, :] = 0 
gw.clm = gw.clm_f_reshape[:,:,0] + gw.clm_f_reshape[:,:,1]*1j


gw.clm_1d = np.einsum('ijk->ik', gw.clm_f_reshape)
np.savetxt(gw.fol_name + "/gw.clm",  gw.clm)
np.savetxt(gw.fol_name + "/Clm_1D.txt",  gw.clm_1d)

print("done with lookup business")
