import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gwbot import gw

OUT = gw.root + "/VTKdata"
M_ADM = gw.M_ADM
MODE = os.environ.get("TRET_MODE", "both").lower()

data = np.loadtxt("/anvil/scratch/x-oscanio/gravity_wave_generation/psi4_dir/rhphc.7.dat") ###Edit this path to the rhphc file you want###
u_code = data[:, 0]

# Build (l,m) list
nmodes = data[:, 1::2].shape[1]
lm = []
l = 2
while len(lm) < nmodes:
    for m in range(l, -l-1, -1):
        lm.append((l, m))
        if len(lm) == nmodes:
            break
    l += 1

# Keep only the desired modes
wanted_modes = [(2,2), (2,1), (2,-1), (2,-2)]
keep_modes = [i for i, mode in enumerate(lm) if mode in wanted_modes]


def make_set(sel, suffix, note):

    u = (u_code[sel] / M_ADM) / 259.3 ###This Number is equal to your P_c###

    md = data[sel, 1::2][:, keep_modes] / M_ADM
    hs = np.sum(md, axis=1)

    # --------------------------------------------------
    # Summed plot
    # --------------------------------------------------
    plt.figure(figsize=(9,4))
    plt.plot(u, hs, color="red", lw=0.9,
             label=r"$h_+$ ((2,$\pm$2),(2,$\pm$1) only)")
    plt.axvline(0, color="gray", lw=0.6)
    plt.xlim(u[0], u[-1])
    plt.xlabel(r"retarded time $t_{ret}/P_c$")
    plt.ylabel(r"$(R/M_{ADM})\,h_+$")
    plt.title(f"Summed (2,±2) and (2,±1) modes {note}")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{OUT}/clm_sum_l2_only_{suffix}.png", dpi=200)
    plt.close()

    # --------------------------------------------------
    # Individual modes (2x2 grid)
    # --------------------------------------------------
    fig, axes = plt.subplots(2, 2,
                             figsize=(10,6),
                             sharex=True)

    axes = axes.flatten()

    for j, idx in enumerate(keep_modes):
        axes[j].plot(u, md[:,j], lw=0.8)
        axes[j].set_title(f"({lm[idx][0]},{lm[idx][1]})")
        axes[j].grid(alpha=0.3)
        axes[j].set_xlim(u[0], u[-1])
        axes[j].set_xlabel(r"$t_{ret}/P_c$")
        axes[j].set_ylabel(r"$(R/M_{ADM})h_+$")

    fig.suptitle(f"Individual l=2 modes {note}", fontsize=14)
    plt.tight_layout(rect=[0,0.03,1,0.95])

    plt.savefig(f"{OUT}/each_mode_l2_only_{suffix}.png", dpi=200)
    plt.close()

    np.savetxt(
        f"{OUT}/clm_sum_l2_only_{suffix}.dat",
        np.column_stack((u, hs)),
        header="t_ret/P_c    (R/M_ADM)*h_plus_(2±2+2±1)"
    )

    print(f"[{suffix}] wrote l=2-only plots")


allmask = np.ones(len(u_code), dtype=bool)
posmask = u_code >= 0

if MODE in ("both", "full"):
    make_set(allmask, "full", "(full record)")

if MODE in ("both", "pos"):
    make_set(posmask, "pos", "(u >= 0)")
