#Splits the tracer output into particle_data abid bot can read

import numpy as np
import os

append=0		#If append seeds to existing ones
dat_folder="dat_new"
ptc_file="ptc_tracer.txt"
u0col=-1e-2	
rmass=2.9085866635E-013	#I don't think the value in these columns matter
if not os.path.exists(dat_folder):
	os.makedirs(dat_folder)
elif not append:
	for f in os.listdir(dat_folder):
		fpath=os.path.join(dat_folder,f)
		try:
			if os.path.isfile(fpath) or os.path.islink(fpath):
				os.unlink(fpath)
		except:
			print("delete failed: %s" %(fpath))

ptc=np.loadtxt(ptc_file)
t=-1
f=-1

for l in ptc:
	if l[1]!=t:
		if f!=-1:
			f.close()
		t=l[1]
		fn="%017.11f.dat"%(t)
		fn=os.path.join(dat_folder,fn)
		if append:
			f=open(fn,"a")
		else:
			f=open(fn,"w")
	f.write("%e %e %e %e %e %e \n" %(t,l[2],l[3],l[4],u0col,rmass))

f.close()
