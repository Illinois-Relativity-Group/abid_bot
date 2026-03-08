import numpy as np
import matplotlib.pyplot as plt
from gwbot import gw

clm = np.loadtxt(gw.root + '/VTKdata/Clm_1D.txt')[:,1]
data = np.loadtxt(gw.rhphc_file) /gw.M_ADM
if gw.plot_memory_effect:
    for mode, mem_file in zip(gw.memory_modes, gw.memory_files):
        l, m = int(str(mode)[0]), int(str(mode)[1])
        globals()[f"clm{l}{m}"] = np.loadtxt(mem_file, dtype=float)[:, 1] / gw.M_ADM
    dmem = min(len(clm20), len(clm40), len(data[:, 0]))
    print(f"Memory data length: {dmem}")


# Load the full dataset in one shot:
#   - column 0 is time,
#   - columns 1,3,5,… are the modes you want to sum.

# Column 0 = times
times = data[:, 0]

# Extract every odd column (1, 3, 5, …) and sum them along axis=1
odd_columns = data[:, 1::2] #/ 2.7       # slices out col 1,3,5,...
summed_modes = np.sum(odd_columns, axis=1)
# Plot each odd column vs time in subplots with two columns
num_modes = odd_columns.shape[1]
ncols = 3
nrows = (num_modes + ncols - 1) // ncols
fig, axes = plt.subplots(nrows, ncols, figsize=(12, 2.5*nrows), sharex=True)
axes = axes.flatten()
for i in range(num_modes):
    # Compute l and m for each mode: l starts at 2, m goes from l to -l
    # For the first 5 modes: (2,2),(2,1),(2,0),(2,-1),(2,-2), then (3,3),(3,2),...
    l = 2
    count = 0
    while count <= i:
        m_range = list(range(l, -l-1, -1))
        if i < count + len(m_range):
            m = m_range[i - count]
            break
        count += len(m_range)
        l += 1
    axes[i].plot(times, odd_columns[:, i], label=f'({l},{m})')
    axes[i].set_ylabel('Mode value')
    axes[i].legend()
for j in range(num_modes, len(axes)):
    fig.delaxes(axes[j])  # Remove unused axes
for ax in axes[-ncols:]:
    ax.set_xlabel('Time (code units)')
fig.suptitle('Each hp mode vs Time', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig(gw.root + '/VTKdata/each_mode_vs_time.png')
plt.close()
output_data = np.column_stack((times, summed_modes))
np.savetxt(gw.root + '/VTKdata/clm_sum_vs_time.dat', output_data)
if gw.plot_memory_effect:  
    summed_modes_memory = summed_modes[:dmem] + clm20[:dmem] + clm40[:dmem]
    # Save the times and summed_modes to a .dat file
    times = times[:dmem]  # Adjust times to match the length of summed_modes
    output_data_memory = np.column_stack((times, summed_modes_memory))
    np.savetxt(gw.root + '/VTKdata/clm_sum_vs_time_memory.dat', output_data_memory)
    # Save just the 20 mode summed with the 20 memory
    mode20 = odd_columns[:, 2]  # Assuming first odd column is (2,0)
    mode20_memory = mode20[:dmem] + clm20[:dmem]
    output_data_20 = np.column_stack((times, mode20[:dmem] + mode20_memory))
    np.savetxt(gw.root + '/VTKdata/clm_20_vs_time_memory.dat', output_data_20)
    # Now plot time vs. the summed array
    plt.plot(times, summed_modes[:dmem], label=r'$h_+$', c='red', alpha=0.75)
    plt.plot(times, summed_modes_memory, label=r'$h_+ + h_{mem}$', c='blue', alpha=0.75)
    plt.plot(times, clm20[:dmem] + clm40[:dmem], label=r'$h_{mem}$', linestyle='--', c='black')
    plt.legend()
    plt.grid()
    plt.xlabel('Time (code units)')
    plt.ylabel(r'$(R/M_{ADM}) * h_+$')
    plt.savefig(gw.root + '/VTKdata/clm_sum_mem_vs_time.png')
    plt.close()
else:
    plt.plot(times, summed_modes, label=r'$h_+$', c='red', alpha=0.75)
    plt.legend()
    plt.grid()
    plt.xlabel('Time (code units)')
    plt.ylabel(r'$(R/M_{ADM}) * h_+$')
    plt.savefig(gw.root + '/VTKdata/clm_sum_vs_time.png')
    plt.close()
