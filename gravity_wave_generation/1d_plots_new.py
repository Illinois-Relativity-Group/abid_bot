"""make_1d_plots.py -- 1D strain plots from rhphc, vs retarded time.

The rhphc.N.dat time column is retarded time u = t_coord - r_* (spans -r_* .. T_end-r_*).
u = source emission time, so u=0 = simulation start; u<0 is the (negligible ~1e-10) recording
lead-in / initial-data transient.

By default produces BOTH versions (TRET_MODE in config.sh: both | pos | full):
  *_full.*  -- the whole record, including the negative-retarded-time lead-in
  *_pos.*   -- cropped to u >= 0 (the physical signal; matches the mesh-movie start)
x-axis is physical t/M (= u / M_ADM). Config (paths, M_ADM, which rhphc.N) comes from
config.sh -> params_gw -> gwbot.

Optionally (MAKE_1D_OVERLAY=1) also emits progressive "drawing-in" animation frames for
compositing the waveform onto the GW-mesh movie -- transparent or green background per
OVERLAY_BG; one frame set per produced range -> VTKdata/overlay_1d_<suffix>/.
"""
import os
import shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gwbot import gw

OUT   = gw.root + "/VTKdata/NEW"
M_ADM = gw.M_ADM
MODE  = os.environ.get("TRET_MODE", "both").lower()   # both | pos | full

# Optional: also emit the progressive "drawing-in" h_+ animation frames used to
# composite the 1D waveform onto the GW-mesh movie (off by default; see config.sh).
MAKE_OVERLAY      = os.environ.get("MAKE_1D_OVERLAY", "0") == "1"
OVERLAY_BG        = os.environ.get("OVERLAY_BG", "transparent").lower()  # transparent | green
OVERLAY_MAXFRAMES = int(os.environ.get("OVERLAY_MAXFRAMES", "0"))        # 0 = all; >0 = preview cap

#data   = np.loadtxt(gw.rhphc_file)
data = np.loadtxt("/anvil/scratch/x-oscanio/gravity_wave_generation/psi4_dir/rhphc.5.dat")
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


def make_overlay_frames(u, hs, suffix):
    """Progressive 'drawing-in' h_+ animation frames for compositing onto the GW-mesh movie.
    White curve + axes on a TRANSPARENT (alpha; default) or GREEN (chroma-key) background --
    set with OVERLAY_BG. Two data points per output frame: the cadence that matches the mesh
    movie's frame count. Reproduces the look of legacy/plot_1D_edit.py from the in-memory arrays
    (no .dat round-trip). Writes VTKdata/overlay_1d_<suffix>/frame_NNNN.png."""
    odir = f"{OUT}/overlay_1d_new_{suffix}"
    if os.path.exists(odir):
        shutil.rmtree(odir)
    os.makedirs(odir)
    bg    = "green" if OVERLAY_BG == "green" else "none"   # "none" -> transparent on save
    max_h = np.max(np.abs(hs)) or 1.0

    fig, ax = plt.subplots(1)
    ax.set_xlim(u[0]/259.3, u[-1]/259.3)
    ax.set_ylim(-1.2 * max_h, 1.2 * max_h)
    graph, = ax.plot([], [], color="white")
    ax.set_facecolor(bg)
    fig.patch.set_facecolor(bg)
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlabel(r"$t_{ret}$", fontsize=30, loc="right")
    ax.set_ylabel(r"$h_+$", fontsize=30, rotation=0)
    ax.yaxis.set_label_coords(-0.07, 0.8)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["left"].set_color("white")
    ax.spines["bottom"].set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")

    nframes = (len(u) + 1) // 2
    if OVERLAY_MAXFRAMES:
        nframes = min(nframes, OVERLAY_MAXFRAMES)
    for i in range(nframes):
        graph.set_data(u[:2 * i + 1], hs[:2 * i + 1])
        fp = os.path.join(odir, f"frame_{i:04d}.png")
        if bg == "none":
            plt.savefig(fp, transparent=True, dpi=300)
        else:
            plt.savefig(fp, facecolor=fig.get_facecolor(), dpi=300)
    plt.close(fig)
    print(f"  [{suffix}] overlay: {nframes} {OVERLAY_BG} frame(s) -> overlay_1d_{suffix}/")


def make_set(sel, suffix, note):
    u = (u_code[sel] / M_ADM) / 259.3                  # retarded time in P_c

    # Keep all modes except m=0 and m=4
    keep_modes = [i for i, (l, m) in enumerate(lm) if m != 0 and abs(m) != 4]

    excluded_label = r"(excluding $m=0,\pm4$ modes)"

    md = data[sel, 1::2][:, keep_modes] / M_ADM
    hs = np.sum(md, axis=1)

    # (1) summed h_+
    plt.figure(figsize=(9, 4))
    plt.plot(u, hs, c="red", lw=0.9, label=r"$h_+$ (summed modes)")
    plt.axvline(0, color="gray", lw=0.6)
    plt.xlim(u[0], u[-1])
    plt.xlabel(r"retarded time  $t_{ret}/P_c$")
    plt.ylabel(r"$(R/M_{ADM})\,h_+$")
    plt.title(f"summed $h_+$ vs retarded time {excluded_label} {note}")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{OUT}/clm_sum_vs_tret_{suffix}.png", dpi=200)
    plt.close()

    # (2) each retained mode
    nplot = len(keep_modes)
    ncols = 3
    nrows = (nplot + ncols - 1) // ncols

    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(12, 2.3 * nrows),
        sharex=True
    )
    axes = axes.flatten()

    for j, idx in enumerate(keep_modes):
        axes[j].plot(u, md[:, j], lw=0.7)
        axes[j].set_title(f"({lm[idx][0]},{lm[idx][1]})", fontsize=9)
        axes[j].grid(alpha=0.3)
        axes[j].set_xlim(u[0], u[-1])

    for j in range(nplot, len(axes)):
        fig.delaxes(axes[j])

    for ax in axes[max(0, nplot - ncols):nplot]:
        ax.set_xlabel(r"$t_{ret}/P_c$")

    fig.suptitle(
        f"each $h_+$ mode vs retarded time {excluded_label} {note}",
        fontsize=14
    )
    plt.tight_layout(rect=[0, 0.02, 1, 0.97])
    plt.savefig(f"{OUT}/each_mode_vs_tret_{suffix}.png", dpi=150)
    plt.close()

    np.savetxt(
        f"{OUT}/clm_sum_vs_tret_{suffix}.dat",
        np.column_stack((u, hs)),
        header="t_ret/P_c    (R/M_ADM)*h_plus_summed"
    )

    print(
        f"  [{suffix}] wrote clm_sum_vs_tret_{suffix}.{{png,dat}}, "
        f"each_mode_vs_tret_{suffix}.png "
        f"({int(sel.sum())} rows, t_ret/P_c {u[0]:.0f}..{u[-1]:.0f})"
    )

    if MAKE_OVERLAY:
        make_overlay_frames(u, hs, suffix)


allmask = np.ones(len(u_code), dtype=bool)
posmask = u_code >= 0.0
print(f"make_1d_plots: TRET_MODE={MODE}  (rows total={len(u_code)}, u>=0={int(posmask.sum())})")
if MODE in ("both", "full"):
    make_set(allmask, "full", "(full record, incl. negative lead-in)")
if MODE in ("both", "pos"):
    make_set(posmask, "pos", "(cropped to u >= 0)")
