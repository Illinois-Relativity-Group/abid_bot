import os
import re
import glob
import numpy as np
import matplotlib.pyplot as plt



# Directory containing Psi4_rad.mon.N and rhphc.N.dat
psi4_dir = "/data/codyolson/memory_effect/chi0.7_spatial_sigma/psi4_dir"

out_dir = "/data/codyolson/memory_effect/chi0.7_spatial_sigma/psi4_rhphc_compare_0.5d_madm"
os.makedirs(out_dir, exist_ok=True)

# Choose how to define the "sim name"
# Option A (default): parent folder name of psi4_dir
sim_name = os.path.basename(os.path.dirname(psi4_dir))

# Regex to capture the extraction number N from Psi4_rad.mon.N
psi4_pat = re.compile(r"Psi4_rad\.mon\.(\d+)$")

psi4_files = sorted(glob.glob(os.path.join(psi4_dir, "Psi4_rad.mon.*")))


for psi_path in psi4_files:
    base = os.path.basename(psi_path)
    m = psi4_pat.match(base)
    if not m:
        # skip anything unexpected (e.g., Psi4_rad.mon.1.bak)
        continue

    mon_n = m.group(1)
    rhphc_path = os.path.join(psi4_dir, f"rhphc.{mon_n}.dat")

    if not os.path.exists(rhphc_path):
        print(f"[warn] Missing rhphc file for mon {mon_n}: {rhphc_path} (skipping)")
        continue

    # Load data
    psi_data = np.loadtxt(psi_path)
    rhphc_data = np.loadtxt(rhphc_path)

    # Basic sanity checks
    if psi_data.ndim != 2 or psi_data.shape[1] < 2:
        print(f"[warn] Unexpected Psi4 format in {psi_path} (shape={psi_data.shape}); skipping")
        continue
    if rhphc_data.ndim != 2 or rhphc_data.shape[1] < 2:
        print(f"[warn] Unexpected rhphc format in {rhphc_path} (shape={rhphc_data.shape}); skipping")
        continue

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=False)

    ax1.plot(psi_data[:, 0], psi_data[:, 1], label=f"Psi4 mon {mon_n}")
    ax1.set_xlabel("Time (code units)")
    ax1.set_ylabel(r"$(R/M_{ADM}) * h_+$")
    ax1.set_title(f"Psi4 vs Time — {sim_name} — mon {mon_n}")
    ax1.grid(True)
    ax1.legend()

    ax2.plot(rhphc_data[:, 0], rhphc_data[:, 1], label=f"rhphc {mon_n}")
    ax2.set_xlabel("Time (code units)")
    ax2.set_ylabel(r"$(R/M_{ADM}) * h_+$")
    ax2.set_title(f"rhphc vs Time — {sim_name} — mon {mon_n}")
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()

    out_name = f"Psi4_vs_rhphc__{sim_name}__mon{mon_n}.png"
    out_path = os.path.join(out_dir, out_name)
    plt.savefig(out_path, dpi=200)
    plt.close(fig)

    print(f"[ok] Wrote {out_path}")