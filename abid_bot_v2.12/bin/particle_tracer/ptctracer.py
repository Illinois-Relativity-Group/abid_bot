import numpy as np
from h5loader import *
from gridder import *
import time

#seedlist=[]  #if you want to directly input seeds

iscontinued=0			#DONT set manually. In (almost) all cases it is automatically detected.
time_limit=12*3600-300		#12h
root = "/anvil/scratch/x-rnarasimhan/abid_bot_binary_SP/" 
h5dir = root+"h5data/"		#with / at the end
iters_txt = root+"bin/particle_tracer/iters.txt" 
seedfile = root+"bin/particle_tracer/seeds_trace.txt"
savefile = root+"bin/particle_tracer/ptc_tracer.txt"
rl = range(10)
MPI = 128
dt= 1.0590967742E+001


def mul(off,m,base=[]):
	if len(base):
		return [i*m+j for i,j in zip(off,base)]
	return [i*m for i in off]

def get_v(h5dir, it, s, h5dir2="", it2=-1):
	x_list= s[0::3]
	y_list= s[1::3]
	z_list= s[2::3]
	vx, t = make_point_grid(h5dir, "vx", it, rl, MPI, x_list, y_list, z_list)
	vy, _ = make_point_grid(h5dir, "vy", it, rl, MPI, x_list, y_list, z_list)
	vz, _ = make_point_grid(h5dir, "vz", it, rl, MPI, x_list, y_list, z_list)
	if int(it2)>0 and h5dir2!="":
		vx2, t2 = make_point_grid(h5dir2, "vx", it2, rl, MPI, x_list, y_list, z_list)
		vy2, _ = make_point_grid(h5dir2, "vy", it2, rl, MPI, x_list, y_list, z_list)
		vz2, _ = make_point_grid(h5dir2, "vz", it2, rl, MPI, x_list, y_list, z_list)
		vx=mul(mul(vx,1,vx2),0.5)
		vy=mul(mul(vy,1,vy2),0.5)
		vz=mul(mul(vz,1,vz2),0.5)
		t=(t+t2)/2
	r = [None]*(len(vx)+len(vy)+len(vz))
	r[0::3]=vx
	r[1::3]=vy
	r[2::3]=vz 
	return r, t


start_t=time.time()

with open(iters_txt) as f:
	list=f.readlines()
list=[h5dir+x.strip() for x in list]

#s=[]
#if ravel:
#	s=[i for t in seedlist for i in t]
#else:
#	s=seedlist

start=0
s=[]

seed=np.loadtxt(seedfile)
#print(seed)
#print("--------")
if iscontinued or seed[0][2]==291633.0722:
	iscontinued=1
	start=int(seed[0][0])
	s=np.ravel(seed[1:])
else:
	s=np.ravel(seed)
#print(s)

#clear file content
if iscontinued==0:
	f=open(savefile,"w")
	for i in range(int(len(s)/3)):
		f.write("%d %017.11f %e %e %e \n" % (0, 0, s[i*3],s[i*3+1], s[i*3+2]) )
	f.close()

for i in range(start, min(10000, len(list)-1)):		#set how far you want to trace
	h5folder=list[i].split(", ")[0]+"/"
	it=list[i].split(", ")[1]
	h5folder_next=list[i+1].split(", ")[0]+"/"
	it_next=list[i+1].split(", ")[1]
	
	#check h5folder integrity. will NOT check first folder
	while i<len(list)-2 and it_next==list[i+2].split(", ")[1]:
		try:
			D = Dataset(h5folder_next, "vx", it_next, rl[-1], MPI)
			print("removed "+list[i+2]+" due to duplication.")
			list.pop(i+2)
		except:
			print("removed "+list[i+1]+" due to duplication.")
			list.pop(i+1)
			h5folder_next=list[i+1].split(", ")[0]+"/"
			it_next=list[i+1].split(", ")[1]
		
	
	k1,_ =get_v(h5folder,it,s)
	k2,_ =get_v(h5folder, it, mul(k1,dt/2,s),h5folder_next,it_next)
	k3,_ =get_v(h5folder, it, mul(k2,dt/2,s),h5folder_next,it_next)
	k4,t =get_v(h5folder_next,it_next,mul(k3,dt,s))

	s=mul(mul(k1,1,mul(k2,2,mul(k3,2,k4))),dt/6,s)
	#except:
	#print("error data at "+str(it)+",in "+h5folder+"\n")
	#else:
	print(i,it,t,s)
	f=open(savefile,"a")
	for j in range(int(len(s)/3)):
		f.write("%s %017.11f %e %e %e \n" % (it_next, t, s[j*3],s[j*3+1], s[j*3+2]) )
	f.close()

	#update files for continuing
	ft=open(seedfile,"w")
	ft.write("%d %s %f \n" %(i+1, it_next, 291633.0722))
	for j in range(int(len(s)/3)):
		ft.write("%e %e %e \n" % (s[j*3],s[j*3+1], s[j*3+2]) )
	ft.close()
	fl=open(iters_txt,"w")
	for j in list:
		fl.write(j[len(h5dir):]+"\n")
	fl.close()
	
	#check timer
	if time.time()-start_t>time_limit:
		break
		
#f.close()




