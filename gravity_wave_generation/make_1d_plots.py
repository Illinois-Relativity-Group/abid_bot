"""make_1d_plots.py -- 1D strain plots from rhphc, vs retarded time.

The rhphc.N.dat time column is retarded time u = t_coord - r_* (spans -r_* .. T_end-r_*).
u = source emission time, so u=0 = simulation start; u<0 is the (negligible ~1e-10) recording
lead-in / initial-data transient.

By default produces BOTH versions (TRET_MODE in config.sh: both | pos | full):
  *_full.*  -- the whole record, including the negative-retarded-time lead-in
  *_pos.*   -- cropped to u >= 0 (the physical signal; matches the mesh-movie start)
x-axis is physical t/M (= u / M_ADM). Config (paths, M_ADM, which rhphc.N) comes from
config.sh -> params_gw -> gwbot.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gwbot import gw

OUT   = gw.root + "/VTKdata"
M_ADM = gw.M_ADM
MODE  = os.environ.get("TRET_MODE", "both").lower()   # both | pos | full

data   = np.loadtxt(gw.rhphc_file)
u_code = data[:, 0]                                    # retarded time, code units (M_sun)

# (l,m) ordering: l=2 m=2..-2, then l=3 m=3..-3, ...
nmodes = data[:, 1::2].shape[1]
lm = []; l = 2
while len(lm) < nmodes:
    for m in range(l, -l - 1, -1):
        lm.append((l, m))
        if len(lm) == nmodes:
            break
    l += 1


def make_set(sel, suffix, note):
    u  = u_code[sel] / M_ADM                  # retarded time in M
    md = data[sel, 1::2] / M_ADM              # (R/M_ADM) * h_+ per mode
    hs = np.sum(md, axis=1)                    # summed h_+

    # (1) summed h_+
    plt.figure(figsize=(9, 4))
    plt.plot(u, hs, c="red", lw=0.9, label=r"$h_+$ (summed modes)")
    plt.axvline(0, color="gray", lw=0.6)
    plt.xlim(u[0], u[-1])
    plt.xlabel(r"retarded time  $t_{ret}/M$"); plt.ylabel(r"$(R/M_{ADM})\,h_+$")
    plt.title(f"summed $h_+$ vs retarded time  {note}")
    plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig(f"{OUT}/clm_sum_vs_tret_{suffix}.png", dpi=200); plt.close()

    # (2) each mode
    ncols = 3; nrows = (nmodes + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 2.3 * nrows), sharex=True)
    axes = axes.flatten()
    for i in range(nmodes):
        axes[i].plot(u, md[:, i], lw=0.7)
        axes[i].set_title(f"({lm[i][0]},{lm[i][1]})", fontsize=9)
        axes[i].grid(alpha=0.3); axes[i].set_xlim(u[0], u[-1])
    for j in range(nmodes, len(axes)):
        fig.delaxes(axes[j])
    for ax in axes[max(0, nmodes - ncols):nmodes]:
        ax.set_xlabel(r"$t_{ret}/M$")
    fig.suptitle(f"each $h_+$ mode vs retarded time  {note}", fontsize=14)
    plt.tight_layout(rect=[0, 0.02, 1, 0.97])
    plt.savefig(f"{OUT}/each_mode_vs_tret_{suffix}.png", dpi=150); plt.close()

    np.savetxt(f"{OUT}/clm_sum_vs_tret_{suffix}.dat", np.column_stack((u, hs)),
               header="t_ret/M    (R/M_ADM)*h_plus_summed")
    print(f"  [{suffix}] wrote clm_sum_vs_tret_{suffix}.{{png,dat}}, each_mode_vs_tret_{suffix}.png "
          f"({int(sel.sum())} rows, t_ret/M {u[0]:.0f}..{u[-1]:.0f})")


allmask = np.ones(len(u_code), dtype=bool)
posmask = u_code >= 0.0
print(f"make_1d_plots: TRET_MODE={MODE}  (rows total={len(u_code)}, u>=0={int(posmask.sum())})")
if MODE in ("both", "full"):
    make_set(allmask, "full", "(full record, incl. negative lead-in)")
if MODE in ("both", "pos"):
    make_set(posmask, "pos", "(cropped to u >= 0)")
