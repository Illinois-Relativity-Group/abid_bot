"""make_lookup.py -- generate the 2D ylm + r lookup tables for the GW mesh.

Clean stage: writes ONLY bin/ylm_lookup_2D.txt and bin/r_lookup_2D.txt from the grid/modes
in the config (config.sh -> params_gw -> gwbot). Unlike the legacy make_lookup_with_memory.py
it does NOT rmtree VTKdata and does NOT run the C++ calc_clm -- those belong to the old route.

Run once per (xy_max_2D, xy_num_2D, num_modes) change; the lookups are otherwise reusable.
"""
import time
import numpy as np
from gwbot import gw
from scipy.special import factorial as fact


# spin-weight -2 spherical harmonic  (-2)Y_lm
def calc_l_d_ms(l, m, theta, s=-2):
    sint = np.sin(theta / 2); cost = np.cos(theta / 2)
    k_i = np.maximum(0, m - s); k_f = np.minimum(l + m, l - s)
    pt1 = np.sqrt(fact(l + m) * fact(l - m) * fact(l + s) * fact(l - s))
    pt2 = 0.0
    for k in range(k_i, k_f + 1, 1):
        num = ((-1) ** k) * (sint ** (2 * k + s - m)) * (cost ** (2 * l + m - s - 2 * k))
        den = fact(k) * fact(l + m - k) * fact(l - s - k) * fact(s - m + k)
        pt2 += num / den
    return pt1 * pt2


def calc_Ylm(l, m, theta, phi, s=-2):
    coeff = ((-1) ** s) * np.sqrt((2 * l + 1) / (4 * np.pi)) * calc_l_d_ms(l, m, theta)
    return coeff * np.cos(m * phi) + coeff * np.sin(m * phi) * 1j


def get_lookup_2D(gw):
    start = time.time()
    print("creating 2D lookups, total x vals: " + str(len(gw.xs_2D)))
    X, Y = np.meshgrid(gw.xs_2D, gw.ys_2D, indexing="ij")
    z = 0.0
    r = np.sqrt(X ** 2 + Y ** 2 + z ** 2)
    phi = np.arctan2(Y, X)
    theta = np.arccos(np.divide(z, r, out=np.zeros_like(r), where=r != 0))

    ylm = np.zeros((len(gw.xs_2D), len(gw.ys_2D), gw.num_modes), dtype=complex)
    l = 2; m = 2
    for mode in range(gw.num_modes):
        ylm[..., mode] = calc_Ylm(l, m, theta, phi)
        if m > -l:
            m -= 1
        else:
            l += 1; m = l

    singular = (X == 0) & (Y == 0)   # zero out the x=y=0 axis
    r[singular] = 0.0
    ylm[singular, :] = 0.0
    print(f"lookup completed, time taken: {time.time() - start:.2f}s")
    return ylm, r


# 2D grid (z = 0 plane) from the config
gw.xs_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=gw.xy_num_2D)
gw.ys_2D = np.linspace(-gw.xy_max_2D, gw.xy_max_2D, num=gw.xy_num_2D)

ylm_2D, r_2D = get_lookup_2D(gw)
np.savetxt(f"{gw.bin_dir}/ylm_lookup_2D.txt", ylm_2D.reshape(ylm_2D.shape[0], -1), fmt="%s")
np.savetxt(f"{gw.bin_dir}/r_lookup_2D.txt", r_2D.reshape(r_2D.shape[0], -1), fmt="%.6e")
print(f"wrote {gw.bin_dir}/ylm_lookup_2D.txt and r_lookup_2D.txt  "
      f"(grid {gw.xy_num_2D}x{gw.xy_num_2D}, +-{gw.xy_max_2D} M_sun, {gw.num_modes} modes)")
