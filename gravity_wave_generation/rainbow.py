#!/usr/bin/env python3

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from gwbot import gw

OUT = gw.root + "/VTKdata"
M_ADM = gw.M_ADM

# ---------------- CONFIG ----------------
FILES = [f"{gw.root}/psi4_dir/rhphc.{i}.dat" for i in range(1, 10)]

EXCLUDE_M = (0, 4, -4)   # set to None to disable filtering
COLORMAP = "turbo"   # try: viridis, plasma, inferno, turbo
# ---------------------------------------


def build_lm(nmodes):
    lm = []
    l = 2
    while len(lm) < nmodes:
        for m in range(l, -l - 1, -1):
            lm.append((l, m))
            if len(lm) == nmodes:
                break
        l += 1
    return lm


def compute_sum(file, pos_only=False):
    data = np.loadtxt(file)

    u_code = data[:, 0]
    sel = u_code >= 0 if pos_only else np.ones(len(u_code), dtype=bool)

    lm = build_lm(data[:, 1::2].shape[1])

    keep = np.array([
        i for i, (_, m) in enumerate(lm)
        if EXCLUDE_M is None or m not in EXCLUDE_M
    ])

    md = data[sel, 1::2][:, keep] / M_ADM
    hs = np.sum(md, axis=1)

    u = (u_code[sel] / M_ADM) / 259.3

    return u, hs


def plot_all(pos_only=False, suffix="full"):
    plt.figure(figsize=(10, 5))

    cmap = cm.get_cmap(COLORMAP, len(FILES))
    colors = [cmap(i / (len(FILES) - 1)) for i in range(len(FILES))]

    for i, f in enumerate(FILES):
        if not os.path.exists(f):
            print(f"Missing: {f}")
            continue

        u, hs = compute_sum(f, pos_only=pos_only)
        plt.plot(u, hs, lw=0.9, color=colors[i], label=f"rhphc.{i+1}")

    plt.axvline(0, color="gray", lw=0.6)
    plt.xlabel(r"retarded time $t_{ret}/P_c$")
    plt.ylabel(r"$(R/M_{ADM}) h_+$ (summed)")
    plt.title(f"Summed waveform comparison rhphc.1–9 ({suffix})")
    plt.grid(alpha=0.3)
    plt.legend(ncol=3, fontsize=8)
    plt.tight_layout()

    outname = f"{OUT}/rhphc_1_to_9_sum_{suffix}_{COLORMAP}.png"
    plt.savefig(outname, dpi=200)
    plt.close()

    print(f"Wrote {outname}")


if __name__ == "__main__":
    print("Plotting rhphc.1–9 comparison (rainbow colormap)...")

    plot_all(pos_only=False, suffix="full")
    plot_all(pos_only=True, suffix="pos")
