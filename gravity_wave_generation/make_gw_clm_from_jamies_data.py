import numpy as np
from gwbot import gw

# === PARAMETERS ===
infile  = gw.rhphc_file  # replace with your actual filename
outfile = 'gw.clm'          # output filename
output_dir_final = gw.root + '/VTKdata/Clm_1D.txt'
if gw.plot_memory_effect:
    for mode, mem_file in zip(gw.memory_modes, gw.memory_files):
        l, m = int(str(mode)[0]), int(str(mode)[1])
        globals()[f"clm{l}{m}"] = np.loadtxt(mem_file, dtype=float)[:, 1] / gw.M_ADM
else:
    for mode, mem_file in zip(gw.memory_modes, gw.memory_files):
        l, m = int(str(mode)[0]), int(str(mode)[1])
        globals()[f"clm{l}{m}"] = 0.0

# === LOAD & PREP ===
data = np.loadtxt(infile) / gw.M_ADM     # shape = (n_times, 1 + 2*n_modes)
pairs = data[:, 1:]            # drop time column → shape = (n_times, 2*n_modes)
n_modes = pairs.shape[1] // 2

hp = pairs[:, 0::2]            # real parts (hp)
hc = pairs[:, 1::2]          # imag parts (hc)
clm = hp + 1j * hc             # complex array shape = (n_times, n_modes)

# === WRITE OUT ===
with open(outfile, 'w') as f:
    for row in clm:
        # for each z, format as "(<real>+<imag>j)" with 18 decimal places in e-notation
        fields = [
            f"({z.real:.18e}{z.imag:+.18e}j)"
            for z in row
        ]
        f.write("  ".join(fields) + "\n")

print(f"Wrote {clm.shape[0]} lines × {n_modes} modes to {outfile}")


odd_columns = data[:, 1::2]        # slices out col 1,3,5,...
even_columns = data[:, 2::2]      # slices out col 2,4,6,...
if gw.plot_memory_effect:
    min_len = min(len(clm20), len(clm40)) 
    dmem = abs(len(min_len) - len(odd_columns))
    summed_modes_odd = np.sum(odd_columns[dmem:], axis=1) + clm20[:min_len] + clm40[:min_len]
else:
    dmem = 0
print(dmem)
summed_modes_odd = np.sum(odd_columns[dmem:], axis=1)
summed_modes_even = np.sum(even_columns[dmem:], axis=1)
output_data = np.column_stack((summed_modes_odd, summed_modes_even))
np.savetxt(output_dir_final, output_data)
