import shutil
import os
import numpy as np

#plcae this script in abid_bot/
#run this script like
#python3 copy_seeds.py
#after setup to replace the particle_seeds.txt files with 
#grid seeds
#set the parameters below; the center of mass is read from bhns.xon


ns_r = 7.5

# merger_fol = "3d_data_23_11_06_234744" #first folder that contains merger data
merger_fol = "3d_data_24_01_23_170522"
r1 = 1.5   #radius of ring
h1 = 4.5   #height of ring


#original bh params
#r1 = 0.5*ns_r
#h1 = 1.5*ns_r
#test1
#r1 = 0.5*ns_r
#h1 = 1.0*ns_r
#r2 = 0.75*ns_r
#h2 = 1.0*ns_r
#test2
#r1 = 0.25*ns_r
#h1 = 1.5*ns_r
#test3
#r1 = 0.25*ns_r
#h1 = 1.0*ns_r
#test4
#r1 = 0.75*ns_r
#h1 = 1.5*ns_r
#test5
#r1 = 0.75*ns_r
#h1 = 1.0*ns_r




num_per = 10    #num points per ring
ref_z = True    
M = 2.59   #ADM mass




##################################
def binsearch(listu,target,begin=0,end=-1,tol=1):       #end excluded
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

def write_seeds(f_name, pairs, num_seeds_per_ring, centers, offset):
    with open(f_name, "w") as f:
        for pair,num_seeds,center in zip(pairs, num_seeds_per_ring, centers):
            for phi in np.linspace(0+offset,2*np.pi+offset,num_seeds, endpoint=False):
                xC,yC,zC = center
                r,h = pair
                x = xC + r * np.cos(phi)
                y = yC + r * np.sin(phi)
                z = zC + h
                if ref_z:
                    loc = tuple(map(str, (x,y,z,x,y,-z)))
                    f.write("%s %s %s\n%s %s %s\n" % loc)
                else:
                    loc = tuple(map(str, (x,y,z)))
                    f.write("%s %s %s\n" % loc)


pairs = [(r1, h1)]
#pairs = [(r1, h1), (r2, h2)]
num_seeds_per_ring = [num_per]
#num_seeds_per_ring = [num_per, num_per]
offset = 0.0


fols = []
past_merger = False
for fol in sorted(os.listdir("xml/")):
    if fol == merger_fol:
        past_merger = True
    if past_merger:
        fols.append(fol)



xon = np.loadtxt("h5data/bhns.xon",comments=['#'])
xmltimelist = xon[:,0]/M
src1 = "seeds_0.txt"
src2 = "bin/bw_many_folder_scripts/atts/Stream_1.xml"


for fol in fols:
    timelist=[file for file in os.listdir("xml/" + fol) if file.startswith("time_")]
    timelist.sort()
    for i in range(0,len(timelist)):
        dst1 = "xml/" + fol + "/particle_seeds_{}_0.txt".format(str(i).zfill(4))
        dst2 = "xml/" + fol + "/Stream_{}_0.xml".format(str(i).zfill(4))
        shutil.copy(src2, dst2)

        fnlen=len(timelist[i])
        time=float(timelist[i][5:fnlen-4])     #fnlen-4 excluded
        idx=binsearch(xmltimelist,time,tol=(xmltimelist[1]-xmltimelist[0])/2) 
        if idx >= 0:
            xC, yC = xon[idx,1:3]
        #    print(xC, yC)
            zC = 0
            centers = [(xC, yC, zC)]
#            centers = [(xC, yC, zC), (xC, yC, zC)]
            write_seeds(dst1, pairs, num_seeds_per_ring, centers, offset)
        else:
            print("time {} not found".format(str(time)))




