# params: root M <setupID>

import numpy as np
from sys import argv
import os

def printvtk(fvtk,j,com=(0,0,0)):
    f = open(fvtk, "w")
    f.write("# vtk DataFile Version 2.0\nspin_vector\nASCII\nDATASET STRUCTURED_POINTS\nDIMENSIONS 3 3 3\nORIGIN -30 -30 -30\nSPACING 30 30 30\nPOINT_DATA 27\nVECTORS spinvec float\n")
    for _ in range(27):
        f.write("%e %e %e\n" % j)
    f.close()

def binsearch(listu,target,begin=0,end=-1,tol=1):	#end excluded
    n=len(listu)
    if end==-1:
        end=n
    if end-begin<=0:
        #print("target %e not found in tolerance" % target)
        if end==n or begin==0:
            return -1
        return begin
    mid=int((begin+end)/2)
    if abs(listu[mid]-target)<tol:
        return mid
    elif listu[mid]>target:
        return binsearch(listu,target,begin,mid)
    else:
        return binsearch(listu,target,mid+1,end)

print("setup_spinvtk_dimensionless.py")

if len(argv)<=2 or len(argv)>=5:
	print("number of arguments incorrect. exiting.")
	exit(1)
	
ordered=0	#if h5folders are ordered by data time
root=argv[1]
M=float(argv[2])
setupid=""
if len(argv)==4:
	setupid=argv[3]

filelist=[]

spinfile=root+'/h5data/bhns_BHspin.mon'
xmlfolder=root+"/xml"+setupid+"/"

#load spin data
#spindata=np.loadtxt(spinfile,comments=['#'])
#spindata=spindata.sort(key=lambda x:x[0])	#Assume sorted. If not, sort first.
#xmltimelist=spindata[:,0]/M
#full_data = np.genfromtxt(spinfile, comments='#', filling_values=np.nan)
trusted_times = []
trusted_spins = []

with open(spinfile) as f:
    for i, line in enumerate(f):
        if line.strip().startswith("#") or len(line.strip()) == 0:
            continue
        if i % 2 == 1:  # odd-numbered line = trusted spin
            parts = line.split()
            if len(parts) >= 4:
                t = float(parts[0])
                Sx, Sy, Sz = map(float, parts[1:4])
                trusted_times.append(t / M)  # normalize time
                trusted_spins.append((Sx, Sy, Sz))

spindata = np.array(trusted_spins)
xmltimelist = np.array(trusted_times)


### ADD STUFF FOR DIMENSIONLESS SPIN PROCESSING ###

# Load areal radii from diagnostics file
diagfile = root + "/h5data/horizon/all_horizon/BH_diagnostics.ah1.gp"
areal_radii = []

with open(diagfile) as f:
    for line in f:
        if line.strip().startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 28:
            areal_radii.append(float(parts[27]))

areal_radii = np.array(areal_radii)

# Check for interpolation need
if len(areal_radii) != len(spindata):
    print("Interpolating areal radii to match spin timestamps...")
    diag_times = []
    with open(diagfile) as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 1:
                diag_times.append(float(parts[0]) / M)
    diag_times = np.array(diag_times)

    if len(diag_times) != len(areal_radii):
        print("ERROR: Could not match areal radius times to spin times.")
        exit(1)

    areal_radii = np.interp(xmltimelist, diag_times, areal_radii)

# Compute horizon mass and dimensionless spin
Jmag = np.linalg.norm(spindata, axis=1)
M_horizon = 0.5 * 1/areal_radii * np.sqrt(areal_radii**4 + 4*Jmag**2)  # np.sqrt(0.5 * areal_radii**2 + np.sqrt(0.25 * areal_radii**4 + Jmag**2))
spin_chi = spindata / (M_horizon[:, np.newaxis] ** 2)

### END STUFF FOR DIMENSIONLESS SPIN PROCESSING ###


# Keep only odd-numbered rows (trusted values)
# Keep only rows with 4 valid entries (trusted spin vector rows)
#spindata = full_data[np.sum(~np.isnan(full_data), axis=1) == 4]
#xmltimelist = spindata[:, 0] / M


print(xmltimelist[:10])
print(xmltimelist[-10:])

#print(spindata[0,0])

xmlfollist=[file for file in os.listdir(xmlfolder) if file.startswith("3d_")]

#detect offset
minxml=min(xmlfollist)
#timelist=[file for file in os.listdir(xmlfolder+minxml) if file.startswith("bh1_cm_")]
timelist=[file for file in os.listdir(xmlfolder+minxml) if file.startswith("bh1_cm_")]
mintime=min(timelist)
fnlen=len(mintime)
#firstTdt=float(mintime[5:fnlen-4])-xmltimelist[0]	#Automatically detects firstTime offset. Should be same as in params
firstTdt=float(mintime[7:fnlen-4])-xmltimelist[0]
if not ordered:
    for xmlfol in xmlfollist:
        timelist=[file for file in os.listdir(xmlfolder+xmlfol) if file.startswith("bh1_cm_")]
        if len(timelist)==0: continue
        mintime=min(timelist)
        fnlen=len(mintime)
        firstTdt=min(firstTdt, float(mintime[7:fnlen-4])-xmltimelist[0])
print("time offset: %f" % firstTdt)

firstTdt=0
#print(xmlfollist)

for xmlfol in xmlfollist:
    timelist=[file for file in os.listdir(xmlfolder+xmlfol) if file.startswith("bh1_cm_")]
    timelist.sort()
    #print(timelist)
    for i in range(0,len(timelist)):
        fnlen=len(timelist[i])
        time=float(timelist[i][7:fnlen-4])-firstTdt	#fnlen-4 excluded
        #print(time)
        idx=binsearch(xmltimelist,time,tol=(xmltimelist[1]-xmltimelist[0])/2)
        if idx>=0:
            printvtk(xmlfolder+xmlfol+"/spin_%04d.vtk"%i,tuple(spin_chi[idx])) ### or spindata[idx] for dimension-full spin
        else:
            print("time %e not found" % time)
