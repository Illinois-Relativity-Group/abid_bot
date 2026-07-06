"""make_clm_sum_Pc.py -- summed h_+ vs retarded time, x-axis in orbital periods.

Same plot as make_1d_plots.py's '_pos' panel (summed modes, cropped to u >= 0),
but the retarded time is expressed in central/orbital periods P_c instead of M:
    t_ret/P_c = (u/M_ADM) / (P_c/M)
Output -> VTKdata/clm_sum_vs_tret_pos_Pc.png  (original *_pos.png left untouched).

Config (rhphc file, M_ADM) reuses config.sh / params_gw defaults via env vars, so this
needs no numpy-incompatible subprocess import. Set PC_OVER_M to change the period.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT     = os.environ.get("GW_ROOT", os.path.dirname(os.path.abspath(__file__)))
PSI4_NUM = int(os.environ.get("PSI4_NUM", 8))
M_ADM    = float(os.environ.get("M_ADM", 0.0603349020955639))   # ADM mass, code units
PC_OVER_M = float(os.environ.get("PC_OVER_M", 304.2))           # central period P_c in units of M

OUT        = ROOT + "/VTKdata"
rhphc_file = f"{ROOT}/psi4_dir/rhphc.{PSI4_NUM}.dat"

data   = np.loadtxt(rhphc_file)
u_code = data[:, 0]                       # retarded time, code units (M_sun)
sel    = u_code >= 0.0                     # crop to physical signal (u >= 0)

u_M  = u_code[sel] / M_ADM                 # retarded time in M
u_Pc = u_M / PC_OVER_M                     # retarded time in P_c
md   = data[sel, 1::2] / M_ADM             # (R/M_ADM) * h_+ per mode
hs   = np.sum(md, axis=1)                  # summed h_+

plt.figure(figsize=(9, 4))
plt.plot(u_Pc, hs, c="red", lw=0.9, label=r"$h_+$ (summed modes)")
plt.axvline(0, color="gray", lw=0.6)
plt.xlim(u_Pc[0], u_Pc[-1])
plt.xlabel(r"retarded time  $t_{ret}/P_c$")
plt.ylabel(r"$(R/M_{ADM})\,h_+$")
plt.title(r"summed $h_+$ vs retarded time  (cropped to u >= 0)")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
plt.savefig(f"{OUT}/clm_sum_vs_tret_pos_Pc.png", dpi=200); plt.close()

np.savetxt(f"{OUT}/clm_sum_vs_tret_pos_Pc.dat", np.column_stack((u_Pc, hs)),
           header=f"t_ret/Pc (Pc={PC_OVER_M}M)    (R/M_ADM)*h_plus_summed")
print(f"wrote clm_sum_vs_tret_pos_Pc.{{png,dat}}  "
      f"({int(sel.sum())} rows, t_ret/Pc {u_Pc[0]:.3f}..{u_Pc[-1]:.3f}, Pc={PC_OVER_M}M)")
