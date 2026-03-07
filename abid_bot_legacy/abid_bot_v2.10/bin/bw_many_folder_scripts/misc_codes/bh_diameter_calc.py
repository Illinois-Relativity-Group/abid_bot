import numpy as np


#edit "root" and "target_it" 
#this script uses the .3d files in abid_bot/bhdata/ and abid_bot/cm.txt
#to calculate the average diameter of the black hole at the specified it in code units
#the diameter is printed directly to the command line 
root = "/scratch1/08211/ericyu3/bhdisk/abid_bot"
misc_dir = root + "/bin/bw_many_folder_scripts/misc_codes"
target_it = 826880

M = 5.76740922E-002
it = 512
dt = 0.11265
target_dt = dt * (target_it/it)
tM = target_dt / M 

cm_f=open(root + "/cm.txt")
bh_f=open(root +  "/bhdata/ht1_" + str(target_it).zfill(7) + ".3d")

cm_lines = cm_f.readlines()
cm_x = 0
cm_y = 0
cm_z = 0
for line in cm_lines:
        curr_dt = line.split()[0]
        if np.around(float(curr_dt), 3) == np.around(float(target_dt), 3):   #if not found, then just uses (0,0,0)
                cm_x = float(line.split()[1])
                cm_y = float(line.split()[2])
                cm_z = float(line.split()[3])
                print("cm found at: (" + str(cm_x) + "," + str(cm_y) + "," + str(cm_z) + ")")
                break   


bh_lines = bh_f.readlines()
values = []
mag_summed = 0
for i in range(len(bh_lines)):
    if i == 0:
        continue

    line_values = bh_lines[i].split()
    x = float(line_values[0])
    y = float(line_values[1])
    z = float(line_values[2])
    #mag_summed += np.sqrt((x**2 + y**2 + z**2))
    mag= np.sqrt((x-cm_x)**2 + (y-cm_y)**2 + (z-cm_z)**2)
    mag_summed+=mag
    #print(bh_lines[i],line_values, mag)
    
average_radius = mag_summed/len(bh_lines)
print("it: " + str(target_it))
print("t/M: " + str(tM))
print("diameter: " + str(average_radius * 2))
bh_f.close()
