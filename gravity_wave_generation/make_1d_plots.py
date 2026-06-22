"""make_1d_plots.py -- 1D strain plots from rhphc, cropped to retarded time u >= 0.

The rhphc.N.dat time column is retarded time u = t_coord - r_* (spans -r_* .. T_end-r_*).
u = source emission time, so u=0 = simulation start; u<0 is the (negligible ~1e-10) recording
lead-in / initial-data transient. We crop to u>=0 and plot in physical t/M (= u / M_ADM).

Config (paths, M_ADM, which rhphc.N) comes from config.sh -> params_gw -> gwbot.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gwbot import gw

ROOT  = gw.root
RHPHC = gw.rhphc_file          # psi4_dir/rhphc.<PSI4_NUM>.dat
M_ADM = gw.M_ADM
OUT   = gw.root + "/VTKdata"

data = np.loadtxt(RHPHC)
u_code = data[:, 0]                       # retarded time, code units (M_sun)
mask   = u_code >= 0.0                     # crop the negative (pre-signal) lead-in
u_M    = u_code[mask] / M_ADM              # retarded time in units of M (t_ret/M)
modes  = data[mask, 1::2] / M_ADM          # (R/M_ADM) * h_+  per mode (21 odd columns)
hsum   = np.sum(modes, axis=1)             # summed h_+ (matches memory_plots.py)

print(f"rows total={len(u_code)}  kept (u>=0)={mask.sum()}  "
      f"u range kept: {u_M[0]:.1f} .. {u_M[-1]:.1f} t/M  ({u_code[mask][0]:.2f} .. {u_code[mask][-1]:.2f} M_sun)")

# ---- (1) summed h_+ vs retarded time ----
plt.figure(figsize=(9, 4))
plt.plot(u_M, hsum, c="red", lw=0.9, label=r"$h_+$ (summed modes)")
plt.axvline(0, color="gray", lw=0.6)
plt.xlim(0, u_M[-1])
plt.xlabel(r"retarded time  $t_{ret}/M$")
plt.ylabel(r"$(R/M_{ADM})\,h_+$")
plt.title("sol_05 summed $h_+$ vs retarded time (u $\\geq$ 0)")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
plt.savefig(f"{OUT}/clm_sum_vs_tret_pos.png", dpi=200); plt.close()

# ---- (2) each mode vs retarded time ----
nmodes = modes.shape[1]
ncols = 3; nrows = (nmodes + ncols - 1)//ncols
fig, axes = plt.subplots(nrows, ncols, figsize=(12, 2.3*nrows), sharex=True)
axes = axes.flatten()
# (l,m) ordering: l=2 m=2..-2, then l=3 m=3..-3, ...
lm = []; l = 2
while len(lm) < nmodes:
    for m in range(l, -l-1, -1):
        lm.append((l, m))
        if len(lm) == nmodes: break
    l += 1
for i in range(nmodes):
    axes[i].plot(u_M, modes[:, i], lw=0.7)
    axes[i].set_title(f"({lm[i][0]},{lm[i][1]})", fontsize=9)
    axes[i].grid(alpha=0.3); axes[i].set_xlim(0, u_M[-1])
for j in range(nmodes, len(axes)): fig.delaxes(axes[j])
for ax in axes[max(0,nmodes-ncols):nmodes]: ax.set_xlabel(r"$t_{ret}/M$")
fig.suptitle("sol_05 each $h_+$ mode vs retarded time (u $\\geq$ 0)", fontsize=14)
plt.tight_layout(rect=[0, 0.02, 1, 0.97])
plt.savefig(f"{OUT}/each_mode_vs_tret_pos.png", dpi=150); plt.close()

np.savetxt(f"{OUT}/clm_sum_vs_tret_pos.dat", np.column_stack((u_M, hsum)),
           header="t_ret/M    (R/M_ADM)*h_plus_summed")
print(f"wrote {OUT}/clm_sum_vs_tret_pos.png , each_mode_vs_tret_pos.png , clm_sum_vs_tret_pos.dat")
