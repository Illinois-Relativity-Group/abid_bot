import numpy as np
from sys import argv
import os

def printvtk(fvtk,j,com=(0,0,0)):
    f = open(fvtk, "w")
    f.write("# vtk DataFile Version 2.0\nspin_vector\nASCII\nDATASET STRUCTURED_POINTS\nDIMENSIONS 3 3 3\nORIGIN -3 -3 -3\nSPACING 3 3 3\nPOINT_DATA 27\nVECTORS spinvec float\n")
    for _ in range(27):
        f.write("%e %e %e\n" % j)
    f.close

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


if len(argv)<=2 or len(argv)>=5:
	print("number of arguments incorrect. exiting.")
	exit(1)
	
root=argv[1]
M=float(argv[2])
setupid=""
if len(argv)==4:
	setupid=argv[3]

#dt=0
#it=512
#dtp32?it=dt/it*32?    #gap in spin.mon
#xmldt=dt/M          #gap in xml folders
#print(dtp32it,xmldt)

filelist=[]

spinfile=root+'/h5data/bhns_BHspin.mon'
xmlfolder=root+"/xml"+setupid+"/"

spindata=np.loadtxt(spinfile,comments=['#'])
xmltimelist=spindata[:,0]/M
print(xmltimelist[:10])
print(xmltimelist[-10:])

#print(spindata[0,0])

xmlfollist=[file for file in os.listdir(xmlfolder) if file.startswith("3d_")]

#print(xmlfollist)

for xmlfol in xmlfollist:
    timelist=[file for file in os.listdir(xmlfolder+xmlfol) if file.startswith("time_")]
    timelist.sort()
    #print(timelist)
    for i in range(0,len(timelist)):
        fnlen=len(timelist[i])
        time=float(timelist[i][5:fnlen-4])	#fnlen-4 excluded
        #print(time)
        idx=binsearch(xmltimelist,time,tol=(xmltimelist[1]-xmltimelist[0])/2)
        if idx>=0:
            printvtk(xmlfolder+xmlfol+"/spin_%04d.vtk"%i,tuple(spindata[idx,1:]))
        else:
            print("time %e not found" % time)


