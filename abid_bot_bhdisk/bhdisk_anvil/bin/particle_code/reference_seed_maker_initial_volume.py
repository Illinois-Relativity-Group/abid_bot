from math import sin, cos, pi
import numpy as np
'''
file_name = 'seeds_0_volume_full'
centers = [(0.0,0.0,0.0)] * 9
pairs = [(9.0, 0.0), (8.9, 0.0), (8.95, 0.0), (7, 0.0), (6.95, 0.0), (6.99, 0.0), (11, 0.0), (10.95, 0.0), (10.99, 0.0)]
num_seeds_per_ring = [8] * 9
'''
'''
file_name = 'seeds_0_volume_full_zoomin'
centers = [(0.0,0.0,0.0)] * 3
pairs = [(9.0, 0.0), (7, 0.0), (11, 0.0)]
num_seeds_per_ring = [8] * 3
'''

file_name = 'seeds_0_volume_full_no_break'
centers = [(0.0,0.0,0.0)] * 9
#pairs = [(9.0, 0.0), (8.9, 0.0), (8.95, 0.0), (7, 0.0), (6.95, 0.0), (6.99, 0.0), (10.3, 0.0), (10.25, 0.0), (10.29, 0.0)]
#pairs = [(9.0, 0.0), (8.9, 0.0), (8.95, 0.0), (7, 0.0), (6.95, 0.0), (6.99, 0.0), (10.0, 0.0), (9.95, 0.0), (9.99, 0.0)]
#pairs = [(8.0, 0.0), (7.9, 0.0), (7.95, 0.0), (7, 0.0), (6.95, 0.0), (6.99, 0.0), (9, 0.0), (8.95, 0.0), (8.99, 0.0)] # working pair
pairs = [(8.0, 0.0), (7.9, 0.0), (7.95, 0.0), (6.5, 0.0), (6.45, 0.0), (6.49, 0.0), (9, 0.0), (8.95, 0.0), (8.99, 0.0)]
num_seeds_per_ring = [8] * 9
offset = pi/8

# ===== Clip settings =====
enable_clip = False              # <-- ON/OFF switch
clip_normal = (0, 1, 0)        # Normal vector of the clipping plane

def is_kept_by_clip(x, y, z, normal):
    return x * normal[0] + y * normal[1] + z * normal[2] >= 0

# ===== Write seeds =====
with open(file_name + ".txt", "w+") as f:
    for pair, num_seeds, center in zip(pairs, num_seeds_per_ring, centers):
        for phi in np.linspace(0 + offset, 2 * pi + offset, num_seeds, endpoint=False):
            xC, yC, zC = center
            r, h = pair

            x = xC + r * cos(phi)
            y = yC + r * sin(phi)
            z = zC + h

            if not enable_clip or is_kept_by_clip(x, y, z, clip_normal):
                f.write(f"{x} {y} {z}\n")
