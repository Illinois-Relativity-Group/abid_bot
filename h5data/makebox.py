```
import numpy as np
from pathlib import Path

def generate_box_outline(center, size, npts, angle_deg, filename):
    """
    Generate a .3d file containing the edges of a 3D box rotated about the z-axis.

    center : (cx, cy, cz)
    size   : (sx, sy, sz)
    npts   : number of points per edge
    angle_deg : rotation angle in degrees (around z-axis)
    filename : output .3d file path
    """
    cx, cy, cz = center
    sx, sy, sz = size
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0

    # Box corner coordinates before rotation
    corners = np.array([
        [cx - hx, cy - hy, cz - hz],
        [cx + hx, cy - hy, cz - hz],
        [cx + hx, cy + hy, cz - hz],
        [cx - hx, cy + hy, cz - hz],
        [cx - hx, cy - hy, cz + hz],
        [cx + hx, cy - hy, cz + hz],
        [cx + hx, cy + hy, cz + hz],
        [cx - hx, cy + hy, cz + hz],
    ])

    # Rotation about Z-axis
    theta = np.radians(angle_deg)
    Rz = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])

    # Shift to origin, rotate, and shift back
    corners_centered = corners - np.array(center)
    corners_rotated = (Rz @ corners_centered.T).T + np.array(center)

    # Edge connections by corner indices
    edges = [
        (0,1),(1,2),(2,3),(3,0), # bottom
        (4,5),(5,6),(6,7),(7,4), # top
        (0,4),(1,5),(2,6),(3,7)  # verticals
    ]

    pts = []
    for (a, b) in edges:
        start, end = corners_rotated[a], corners_rotated[b]
        for t in np.linspace(0, 1, npts, endpoint=True):
            p = (1 - t) * start + t * end
            pts.append(p)

    # Write to .3d text file
    p = Path(filename)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        f.write("x y z c\n")
        for (x, y, z) in pts:
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {100}\n")

    print(f"Wrote rotated box outline to {p.resolve()}")
    return str(p.resolve())


if __name__ == "__main__":
    # Example usage
    generate_box_outline(center=(0, 0, 0), size=(2, 2, 1), npts=1000,
                         angle_deg=20, filename="box.3d")
```