"""make_clm_sum_4mode_Pc.py -- summed h_+ vs retarded time (P_c x-axis), but summing
ONLY the four l=2, m=+-1 / m=+-2 modes -- i.e. the non-axisymmetric quadrupole, with the
dominant (and 1/r-contaminated) m=0 mode EXCLUDED.

Sibling of make_clm_sum_Pc.py (which sums ALL 21 modes, data[:,1::2]); that script + its
outputs are left untouched. This one keeps the same crop (u >= 0), units ((R/M_ADM) h_+),
and P_c time axis so the two figures are directly comparable.

rhphc.N.dat column layout (0-indexed; col 0 = retarded time), per rhphc_lm.py:
    l=2:  (2, 2)->hp1/hc2   (2, 1)->hp3/hc4   (2, 0)->hp5/hc6   (2,-1)->hp7/hc8   (2,-2)->hp9/hc10
So the four h_+ columns we sum are [1, 3, 7, 9] = (2,2),(2,1),(2,-1),(2,-2); col 5 = (2,0) is dropped.

Radius: PSI4_NUM=7  ->  rhphc.7.dat  ->  extraction radius R ~ 150 M_sun.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT      = os.environ.get("GW_ROOT", os.path.dirname(os.path.abspath(__file__)))
PSI4_NUM  = int(os.environ.get("PSI4_NUM", 7))                   # 7 -> rhphc.7.dat, R ~ 150 M_sun
M_ADM     = float(os.environ.get("M_ADM", 0.0603349020955639))  # ADM mass, code units
PC_OVER_M = float(os.environ.get("PC_OVER_M", 304.2))           # central period P_c in units of M

# 0-indexed h_+ columns for (2,2),(2,1),(2,-1),(2,-2); (2,0)=col 5 deliberately excluded.
MODE_COLS = [1, 3, 7, 9]
MODE_TAG  = r"$(2,\pm1)+(2,\pm2)$"

OUT        = ROOT + "/VTKdata"
rhphc_file = f"{ROOT}/psi4_dir/rhphc.{PSI4_NUM}.dat"

data   = np.loadtxt(rhphc_file)
u_code = data[:, 0]                       # retarded time, code units (M_sun)
sel    = u_code >= 0.0                     # crop to physical signal (u >= 0)

u_M  = u_code[sel] / M_ADM                 # retarded time in M
u_Pc = u_M / PC_OVER_M                     # retarded time in P_c
md   = data[sel][:, MODE_COLS] / M_ADM     # (R/M_ADM) * h_+ for the four selected modes
hs   = np.sum(md, axis=1)                  # summed h_+ over the four modes

plt.figure(figsize=(9, 4))
plt.plot(u_Pc, hs, c="red", lw=0.9, label=r"$h_+$ (" + MODE_TAG + " modes)")
plt.axvline(0, color="gray", lw=0.6)
plt.xlim(u_Pc[0], u_Pc[-1])
plt.xlabel(r"retarded time  $t_{ret}/P_c$")
plt.ylabel(r"$(R/M_{ADM})\,h_+$")
plt.title(r"summed $h_+$, " + MODE_TAG + r" only  (R $\approx$ 150 $M_\odot$, u >= 0)")
plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()

base = f"{OUT}/clm_sum_l2m1m2_r{PSI4_NUM}_vs_tret_pos_Pc"
plt.savefig(f"{base}.png", dpi=200); plt.close()

np.savetxt(f"{base}.dat", np.column_stack((u_Pc, hs)),
           header=f"t_ret/Pc (Pc={PC_OVER_M}M)    (R/M_ADM)*h_plus  [modes (2,+-1),(2,+-2); R=rhphc.{PSI4_NUM}, ~150 Msun]")
print(f"wrote {base}.{{png,dat}}  "
      f"({int(sel.sum())} rows, t_ret/Pc {u_Pc[0]:.3f}..{u_Pc[-1]:.3f}, "
      f"cols {MODE_COLS}, peak |h|={np.max(np.abs(hs)):.3e})")
