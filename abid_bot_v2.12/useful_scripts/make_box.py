import numpy as np

x_min, x_max = -20, 20
y_min, y_max = -10, 10
z_min, z_max = -10, 10

x_coords = np.linspace(x_min, x_max, num=1000) 
y_coords = np.linspace(y_min, y_max, num=1000)
z_coords = np.linspace(z_min, z_max, num=1000)

border_coords = np.vstack([
    np.column_stack((x_coords, y_min * np.ones_like(x_coords), z_min * np.ones_like(x_coords))),
    np.column_stack((x_coords, y_max * np.ones_like(x_coords), z_min * np.ones_like(x_coords))),
    np.column_stack((x_coords, y_min * np.ones_like(x_coords), z_max * np.ones_like(x_coords))),
    np.column_stack((x_coords, y_max * np.ones_like(x_coords), z_max * np.ones_like(x_coords))),
    np.column_stack((x_min * np.ones_like(y_coords), y_coords, z_min * np.ones_like(y_coords))),
    np.column_stack((x_max * np.ones_like(y_coords), y_coords, z_min * np.ones_like(y_coords))),
    np.column_stack((x_min * np.ones_like(y_coords), y_coords, z_max * np.ones_like(y_coords))),
    np.column_stack((x_max * np.ones_like(y_coords), y_coords, z_max * np.ones_like(y_coords))),
    np.column_stack((x_min * np.ones_like(z_coords), y_min * np.ones_like(z_coords), z_coords)),
    np.column_stack((x_max * np.ones_like(z_coords), y_min * np.ones_like(z_coords), z_coords)),
    np.column_stack((x_min * np.ones_like(z_coords), y_max * np.ones_like(z_coords), z_coords)),
    np.column_stack((x_max * np.ones_like(z_coords), y_max * np.ones_like(z_coords), z_coords))
])

output_filename = 'box.3d'
with open(output_filename, 'w') as f:
    f.write("x y z box\n")
    for point in border_coords:
        f.write(f"{point[0]} {point[1]} {point[2]} 100\n")

