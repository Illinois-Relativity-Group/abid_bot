import sys, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DT = 0.056325
MADM = 0.0603349020955639

def read_vtk_2d(path):
    with open(path) as f:
        lines = f.read().split("\n")
    nx = ny = ds = None
    for i, l in enumerate(lines):
        if l.startswith("DIMENSIONS"):
            p = l.split(); nx = int(p[1]); ny = int(p[2])
        if l.startswith("LOOKUP_TABLE"):
            ds = i + 1
            break
    vals = np.array(" ".join(lines[ds:]).split(), dtype=float)
    return vals.reshape(ny, nx)

frames = [int(x) for x in sys.argv[1].split(",")]
out = sys.argv[2] if len(sys.argv) > 2 else "VTKdata/preview.png"
n = len(frames)
ncols = 3
nrows = math.ceil(n / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 5 * nrows), squeeze=False)
axes = list(axes.flat)
for ax, fr in zip(axes, frames):
    a = read_vtk_2d(f"VTKdata/2D/hplus_{fr:06d}.vtk")
    v = np.percentile(np.abs(a), 99.5)
    if v == 0:
        v = (np.max(np.abs(a)) or 1.0)
    im = ax.imshow(a, origin="lower", extent=[-1000, 1000, -1000, 1000],
                   cmap="RdBu_r", vmin=-v, vmax=v)
    ax.set_title(f"frame {fr}   t/M~{fr*DT/MADM:.0f}   front r~{fr*DT:.0f} M_sun   |max|={np.max(np.abs(a)):.2g}")
    ax.set_xlabel("x [M_sun]"); ax.set_ylabel("y [M_sun]")
    plt.colorbar(im, ax=ax, fraction=0.046)
for ax in axes[n:]:
    ax.axis("off")
plt.tight_layout()
plt.savefig(out, dpi=100)
print("saved", out)
