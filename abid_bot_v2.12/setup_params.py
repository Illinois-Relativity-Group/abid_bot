#This script requires setup_params.py to be in the root directory, so in your abid_bot/.
#It also requires the following files to be present in your h5data directory - bhns.mon and bhns.xon


import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "sultan"])

from sultan.api import Sultan
import os
import re
import numpy as np

print("Setting up params")
s = Sultan()

root = str(s.pwd().run())
print("Root is " + str(root))

h5dir = root + "/" + "h5data/"
dir_3d_path = ""
for dir_3d in os.listdir(h5dir):
    dir_3d_path = os.path.join(h5dir, dir_3d)
    if os.path.isdir(dir_3d_path) and dir_3d.startswith("3d"):
        break
print(dir_3d_path)




#-------------------------------------Finding it (iteration timestep)--------------------------------------------
h5dat = ""
with Sultan.load(logging=False, cwd=dir_3d_path) as s:
    h5dat = str(s.h5dump("-N", "timestep", dir_3d_path + "/" + "rho_b.file_0.h5").run())

pattern = r'\(0\): (\d+)'
matches = re.findall(pattern, h5dat)
values = [int(match) for match in matches]
sortedvals = np.unique(np.sort(np.array(values)))

it = sortedvals[1]-sortedvals[0] if len(sortedvals) > 1 else sortedvals[0]

print("it = " + str(it))

#-------------------------------------------Finding dt------------------------------------------------------

header = False
with Sultan.load(logging=False, cwd=h5dir) as s:
    dt_file = str(s.head("bhns.xon").run())
lines = dt_file.strip().split('\n')
column_row1 = lines[0].strip().split()
column_row2 = lines[1].strip().split()
column_row4 = lines[3].strip().split()
column_row5 = lines[4].strip().split()
dt = 0
if column_row1[0].startswith('#') or column_row1[0].startswith('T'):
    dt = float(column_row5[0]) - float(column_row2[0])
    header = True
else:
    dt = float(column_row4[0]) - float(column_row1[0])
print("dt = " + str(dt))

#-------------------------------------------Finding first time------------------------------------------------------

firstTime = format(float(column_row2[0]), '011.11f')[-17:] if header else format(float(column_row1[0]), '011.11f')[-17:]
firstTimestr = str(firstTime)
integer_part, decimal_part = firstTimestr.split('.')
integer_part = integer_part.zfill(5)
firstTime = '.'.join([integer_part, decimal_part])
print("firstTime = " + str(firstTime))


#-------------------------------------------Finding max density and M_adm------------------------------------------------------

header = False
with Sultan.load(logging=False, cwd=h5dir) as s:
    md_file = str(s.head("bhns.mon").run())
lines = md_file.strip().split('\n')
column_row1 = lines[0].strip().split()
column_row2 = lines[1].strip().split()
column_row3 = lines[2].strip().split()
max_density = 0
M_adm = 0
if column_row1[0].startswith('#') or column_row1[0].startswith('T'):
    max_density = float(column_row2[8])
    M_adm = float(column_row2[11]) + float(column_row2[12])
    header = True
else:
    max_density = float(column_row1[8])
    M_adm = float(column_row1[11]) + float(column_row1[12])

print("Max Density = " + str(max_density))
print("M_adm = " + str(M_adm))

#-------------------------------------------Editing params------------------------------------------------------

#I already wrote this in bash and I'm too lazy to switch it so all this does is creates a bash script runs it and deletes it

bash_script = """
#!/bin/bash


echo "Editing params"
newroot='root=\"""" + str(root) + """\" '
newit='it=\"""" + str(it) + """\" '
newdt='dt=\"""" + str(dt) + """\" '
newft='firstTime=\"""" + str(firstTime) + """\" '
newmax='maxdensity=\"""" + str(max_density) + """\" '
newM='M=\"""" + str(M_adm) + """\" '

prevroot=$(sed -n -e '/^[^#]*root=/p' params | sed 's/#.*//')
previt=$(sed -n -e '/^[^#]*it=/p' params | sed 's/#.*//')
prevdt=$(sed -n -e '/^[^#]*dt="/p' params | sed 's/#.*//')
prevft=$(sed -n -e '/^[^#]*firstTime="/p' params | sed 's/#.*//')
prevmax=$(sed -n -e '/^[^#]*maxdensity="/p' params | sed 's/#.*//')
prevM=$(sed -n -e '/^[^#]*M="/p' params | sed 's/#.*//')

sed -i -e "s|$prevroot|$newroot|g" params
sed -i -e "s|$previt|$newit|g" params
sed -i -e "s|$prevdt|$newdt|g" params
sed -i -e "s|$prevft|$newft|g" params
sed -i -e "s|$prevmax|$newmax|g" params
sed -i -e "s|$prevM|$newM|g" params"""

with open("edit_params.sh", 'w') as f:
        f.write(bash_script)

os.chmod("edit_params.sh", 0o755)

with Sultan.load(logging=False, cwd=root) as s:
    s.bash(f"./edit_params.sh").run()

os.remove("edit_params.sh")

