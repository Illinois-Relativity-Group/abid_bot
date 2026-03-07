import numpy as np
from pathlib import Path

def generate_line(center, length, direction, npts, filename):
    """
    Generate a .3d file containing a single straight line in 3D.

    center    : (cx, cy, cz)
    length    : total length of the line
    direction : direction vector (will be normalized)
    npts      : number of points
    filename  : output .3d file
    """

    cx, cy, cz = center
    direction = np.array(direction, dtype=float)

    # Normalize direction vector
    norm = np.linalg.norm(direction)
    if norm == 0:
        raise ValueError("Direction vector cannot be zero.")
    direction = direction / norm

    # Half-length vector
    half_vec = (length / 2.0) * direction

    # Endpoints
    p0 = np.array(center) - half_vec
    p1 = np.array(center) + half_vec

    # Generate points
    pts = [(1 - t) * p0 + t * p1 for t in np.linspace(0, 1, npts)]

    # Write to .3d file
    p = Path(filename)
    p.parent.mkdir(parents=True, exist_ok=True)

    with open(p, "w") as f:
        f.write("x y z c\n")
        for (x, y, z) in pts:
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {100}\n")

    print(f"Wrote line to {p.resolve()}")
    return str(p.resolve())


if __name__ == "__main__":
    # Example: line of length 5, pointing along (1,1,0)
    generate_line(center=(0.3,0,0.1),
                  length=0.25, #0.5
                  direction=(0,0,1),
                  npts=500,
                  filename="line.3d")
