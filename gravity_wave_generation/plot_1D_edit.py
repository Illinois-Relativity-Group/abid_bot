import os
import numpy as np
import matplotlib.pyplot as plt
import shutil

# Define the output directory for frames
output_dir = '/data/codyolson/memory_effect/memory_data_generation/VTKdata/frames_1D'
#data_file_path = '/data/codyolson/memory_effect/memory_data_generation/VTKdata_no_memory/Clm_1D.txt'
data_file_path = '/data/codyolson/memory_effect/memory_data_generation/VTKdata/Clm_1D.txt'
times_filepath = '/data/codyolson/memory_effect/memory_data_generation/psi4_dir/rh_mem_20.3.dat'

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Load the data file
#data = np.loadtxt(data_file_path)
#times = np.loadtxt(times_filepath)[:, 0]
#times = np.loadtxt(times_filepath)

#difference = len(times) - len(data[:, 0])
#times = times[difference:]  # Adjust times to match the length of data

#hp = np.vstack((times, data[:,0])).T
#hp = hp[hp[:,0] >= 600] # t/M offset + r_areal_star - rad_circ
#hp = hp[hp[:,0] < hp[-1,0] - 32] # max_time - (rad_cir + offset)
# Extract time and value columns
hp = np.loadtxt("/data/codyolson/memory_effect/memory_data_generation/VTKdata/clm_sum_vs_time_memory.dat")
x = hp[:, 0] # Time
y = hp[:, 1]  # h_+ values

# Find the number of time steps and the maximum value for scaling
num_times = x.shape[0]
max_h = max(np.abs(y))

# Setup the figure
fig, ax = plt.subplots(1)
plt.xlim(x[0], x[-1])
plt.ylim(-1.2 * max_h, 1.2 * max_h)
graph, = plt.plot([], [], color="white")

# Customizing the style
ax.set_facecolor("green")  #green
fig.patch.set_facecolor("green") #green

ax.spines["bottom"].set_position(("data", 0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlabel(r"$t_{ret}$", fontsize=30, loc="right")
ax.set_ylabel(r"$h_+$", fontsize=30, rotation=0)
ax.yaxis.set_label_coords(-0.07, 0.8)
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")
ax.spines["left"].set_color("white")
ax.spines["bottom"].set_color("white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")

# Add periodic time labels on the x-axis
#tick_interval = (x[-1] - x[0]) // 6  # Divide into 6 evenly spaced ticks
#xticks = np.arange(x[0], x[-1] + tick_interval, tick_interval)
#ax.set_xticks(xticks)
#ax.set_xticklabels([f"{int(t)}" for t in xticks])

# Generate frames
for i in range(800):   #num_times
    # Update data for the plot
    graph.set_data(x[:2*i + 1], y[:2*i + 1])

    # Save the frame
    frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
    plt.savefig(frame_path, facecolor=fig.get_facecolor(), dpi=300)
    print(f"Saved frame {i}")
    
# Close the plot
plt.close(fig)

print(f"Frames saved in directory: {output_dir}")
