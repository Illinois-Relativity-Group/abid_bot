import h5py
import os
import shutil
root="/home1/07525/tg868241/bhdisk_45/h5data/"
outfile="h5log.txt"
rlmax=12
outy=open(outfile,"w")
for filename in os.listdir(root):
	if filename.startswith("3d_data_") and os.path.isdir(root+filename):
		try:
			f=h5py.File(root+filename+"/By.file_0.h5")
		except:
			shutil.move(root+filename, root+"bad_data/"+filename)
			outy.write("moved; "+root+filename+"\n")
outy.close()
