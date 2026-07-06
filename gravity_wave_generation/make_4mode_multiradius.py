"""make_4mode_multiradius.py -- four-mode ((2,+-1)+(2,+-2)) summed h_+ across ALL extraction radii.

Adopts the yguo/gw-multi-radius branch's per-radius idea, but keeps the sol_05 physics
(M_ADM=0.0603349, OMEGA_CUT=0.342) and REUSES the existing psi4_dir/rhphc.N.dat -- no regen.

rhphc.N.dat holds r*h per lm mode (0-indexed cols; col0 = retarded time), so plotting
(R/M_ADM)*h_+ = (r*h_+)/M_ADM directly tests 1/r falloff:
  * a clean wave-zone mode has r*h radius-INDEPENDENT  -> curves COLLAPSE across radii
  * a contaminated (non-1/r) mode                       -> curves FAN OUT with radius
We sum only the non-axisymmetric quadrupole (cols [1,3,7,9] = (2,2),(2,1),(2,-1),(2,-2)),
excluding the dominant (2,0)=col5.

Outputs -> VTKdata/multiradius_4mode/ :
  per radius:  hplus4_r<N>.{png,dat}
  overlay:     hplus4_overlay_allradii.png   (the 1/r-collapse test)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm

ROOT      = os.environ.get("GW_ROOT", os.path.dirname(os.path.abspath(__file__)))
M_ADM     = float(os.environ.get("M_ADM", 0.0603349020955639))   # sol_05 ADM mass, code units
PC_OVER_M = float(os.environ.get("PC_OVER_M", 304.2))            # central period P_c in units of M
RADII     = [int(x) for x in os.environ.get("PSI4_NUMS", "1 2 3 4 5 6 7 8 9").split()]

MODE_COLS = [1, 3, 7, 9]                    # (2,2),(2,1),(2,-1),(2,-2) h_+ ; (2,0)=col5 excluded
MODE_TAG  = r"$(2,\pm1)+(2,\pm2)$"

OUT = ROOT + "/VTKdata/multiradius_4mode"
os.makedirs(OUT, exist_ok=True)

plt.figure(figsize=(10, 4.5))                # overlay figure
colors = cm.viridis(np.linspace(0.05, 0.9, len(RADII)))

print(f"radius   R(~|u0|,Msun)   rows(u>=0)   peak|(R/M_ADM)h+|   (r*h collapse ==> ~const)")
summary = []
for i, n in enumerate(RADII):
    f = f"{ROOT}/psi4_dir/rhphc.{n}.dat"
    if not os.path.isfile(f):
        print(f"  {n:3d}   MISSING {f}"); continue
    data   = np.loadtxt(f)
    u_code = data[:, 0]
    R_est  = abs(u_code[0])                  # |first retarded time| ~ extraction radius (M_sun)
    sel    = u_code >= 0.0
    u_Pc   = (u_code[sel] / M_ADM) / PC_OVER_M
    hs     = np.sum(data[sel][:, MODE_COLS], axis=1) / M_ADM
    peak   = np.max(np.abs(hs))
    summary.append((n, R_est, peak))
    print(f"  {n:3d}   {R_est:10.2f}      {int(sel.sum()):6d}       {peak:.4e}")

    # per-radius outputs
    base = f"{OUT}/hplus4_r{n}"
    np.savetxt(f"{base}.dat", np.column_stack((u_Pc, hs)),
               header=f"t_ret/Pc (Pc={PC_OVER_M}M)  (R/M_ADM)*h_plus  [modes (2,+-1),(2,+-2); rhphc.{n}, R~{R_est:.1f} Msun]")
    plt.figure(figsize=(9, 4))
    plt.plot(u_Pc, hs, c="red", lw=0.9, label=fr"$h_+$ ({MODE_TAG}), R$\approx${R_est:.0f} $M_\odot$")
    plt.axvline(0, color="gray", lw=0.6); plt.xlim(u_Pc[0], u_Pc[-1])
    plt.xlabel(r"retarded time  $t_{ret}/P_c$"); plt.ylabel(r"$(R/M_{ADM})\,h_+$")
    plt.title(fr"summed $h_+$, {MODE_TAG} only  (radius {n}, R$\approx${R_est:.0f} $M_\odot$)")
    plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig(f"{base}.png", dpi=200); plt.close()

    # add to overlay
    plt.figure(1)
    plt.plot(u_Pc, hs, lw=0.8, color=colors[i], label=fr"r{n} (R$\approx${R_est:.0f})")

plt.figure(1)
plt.axhline(0, color="gray", lw=0.5)
plt.xlabel(r"retarded time  $t_{ret}/P_c$")
plt.ylabel(r"$(R/M_{ADM})\,h_+ \;=\; (r\,h_+)/M_{ADM}$")
plt.title(r"four-mode " + MODE_TAG + r" $h_+$ vs radius  (curves collapse $\Rightarrow$ 1/r falloff)")
plt.grid(alpha=0.3); plt.legend(ncol=2, fontsize=8, title="extraction radius"); plt.tight_layout()
plt.savefig(f"{OUT}/hplus4_overlay_allradii.png", dpi=200); plt.close()

# quantitative 1/r readout: peak(r*h) across radii -- flat = 1/r, rising = slower than 1/r
if summary:
    peaks = np.array([s[2] for s in summary]); Rs = np.array([s[1] for s in summary])
    print(f"\npeak(r*h)/M_ADM across radii: min={peaks.min():.3e} max={peaks.max():.3e} "
          f"spread(max/min)={peaks.max()/peaks.min():.2f}x")
    print(f"outer radii (R>=120) peak spread: "
          f"{peaks[Rs>=120].max()/peaks[Rs>=120].min():.2f}x  (~1.0 => clean 1/r in the wave zone)")
    print(f"\nwrote {OUT}/  (per-radius hplus4_r<N>.{{png,dat}} + hplus4_overlay_allradii.png)")
