# Clean data beforehand! Remove all lines that don't contain data
# For example, try: grep -v -e "^$" -e "#" vy.xy.asc > vy.xy.clean

import numpy as np
from os import listdir
from sys import argv


delta_r=float(argv[1])
M=float(argv[2])
ini_time=float(argv[3])
start_time=float(argv[4])
vxfiles=[]
vyfiles=[]
for fil in listdir("vel_data"):
	if (fil[1]=='x'):
		vxfiles.append(fil)
	if (fil[1]=='y'):
		vyfiles.append(fil)

#Sort
vxfiles.sort()
vyfiles.sort()


cmdata=np.loadtxt("/u/sciteam/liu14/scratch/OMEGAmag/data/bhns.xon")
print("first 10 cmdata:",cmdata[0:10])
cmtrim=[]
for cm in list(cmdata):
	if (cm[0]/M>=start_time):
		cmtrim.append(cm)
cmdata = np.array(cmtrim)
t_cen = cmdata[:,0]+ini_time
#print (t_cen)

t_cen /= M
print ("t_cen:",t_cen)

x_cen = cmdata[:,1]
y_cen = cmdata[:,2]


print ('t,x:',t_cen[0:10],x_cen[0:10])

def calc_w_part(x,y,v,dr,dir):
	w=np.zeros(300)
	weights=np.zeros(300)
	r2=(x**2+y**2)
	r=np.sqrt(r2)
	if (dir=='x'):
		#print('Calculating x contribution')
		omega=-y*v/r2
	else:
		#print('Calculating y contribution')
		omega=x*v/r2
	for i in range(x.size):
		idx1=int(np.floor(r[i]/dr))
		idx2=idx1+1
		weight2=(r[i]-idx1*dr)*1.0/dr
		weight1=1.0-weight2
		if(idx2<300):
			w[idx1]+=omega[i]*weight1
			w[idx2]+=omega[i]*weight2
			weights[idx1]+=weight1
			weights[idx2]+=weight2
	#print('normalizing')
	for i,(omega,weight) in enumerate(zip(w,weights)):
		rad=delta_r*i
		if (weight==0):
			weight=-1
		w[i]=omega*1.0/weight
	return w



for xfile, yfile in zip(vxfiles,vyfiles):
	#print('loading data')
	vx_data = np.loadtxt("vel_data/"+xfile)
	vy_data = np.loadtxt("vel_data/"+yfile)
	
	time=xfile[3:-4]
	if(np.size(vx_data)!=np.size(vy_data)):
		print("BAD DATA!! time="+str(time)+"M")
		with open('err.log','a') as errlog :
			errlog.write(str(time)+'\n')
		continue
	idx = (np.abs(t_cen-float(time))).argmin() #No need to add t_offset here since bhns.xon is shifted as well

	xx = vx_data[:,9]-x_cen[idx]
	xy = vy_data[:,9]-x_cen[idx]
	yx = vx_data[:,10]-y_cen[idx]
	yy = vy_data[:,10]-y_cen[idx]
	vx = vx_data[:,12]
	vy = vy_data[:,12]
	
	print ("Caculating omega at t="+str(time)+"M")
	print ("The center of mass at this time is:" )
	print (x_cen[idx], y_cen[idx])
	w=calc_w_part(xx,yx,vx,delta_r,'x')+calc_w_part(xy,yy,vy,delta_r,'y')	
	savename ="w_data/w_"+time.zfill(6)+".txt"
	savefile=open(savename, 'w')
	for i, omega in enumerate(w):
		rad=delta_r*i
		savefile.write(str(rad)+'\t'+str(omega)+'\n')
	savefile.close()
