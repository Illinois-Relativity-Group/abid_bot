#more straightforward bh_diameter calc script
#more cumbersome but you don't need entire abid bot


import numpy as np

bh_f=open("bh1_000000.3d", "r")   # change file name here
bh_lines = bh_f.readlines()
cm_x = 0.; cm_y = 0.; cm_z = 0.
for i in range(len(bh_lines)):
    if i == 0: continue
    line_values = bh_lines[i].split()
    cm_x += float(line_values[0])
    cm_y += float(line_values[1])
    cm_z += float(line_values[2])
cm_x /= len(bh_lines) - 1
cm_y /= len(bh_lines) - 1
cm_z /= len(bh_lines) - 1
values = []
mag_summed = 0.
for i in range(len(bh_lines)):
    if i == 0: continue
    line_values = bh_lines[i].split()
    x = float(line_values[0])
    y = float(line_values[1])
    z = float(line_values[2])
    mag= np.sqrt((x-cm_x)**2 + (y-cm_y)**2 + (z-cm_z)**2)
    mag_summed+=mag
average_radius = mag_summed/(len(bh_lines) - 1)
print("diameter: " + str(average_radius * 2))
bh_f.close()
