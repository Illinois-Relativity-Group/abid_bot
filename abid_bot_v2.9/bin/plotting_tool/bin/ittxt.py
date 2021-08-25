import h5py
import os
root="/scratch1/07525/tg868241/stable_remnant_full"
outfile="iters.txt"
outy=open(outfile,"w")
bigtimelist=[]
for filename in os.listdir(root):
	timelist=[]
	#print(filename)
	if filename.startswith("3d_data_") and os.path.isdir(root+"/"+filename):
		#print("here")
		#guy=root+"/"+filename+"By.file_0.h5"
		#print(guy)
		f=h5py.File(root+"/"+filename+"/By.file_0.h5")
		for chunk in list(f.keys()):
			#print(chunk)
			it=chunk.split()[1][3:]
			#print(it)
			if it=="":
				continue
			if int(it) not in timelist:	
				#print("append")
				timelist.append(int(it))
		#timelist.sort()
		for time in timelist:
			#outy.write(filename+ ", "+str(time))
			bigtimelist.append((filename, time))
bigtimelist.sort(key=lambda x: x[1])
for i in bigtimelist:
	outy.write(i[0]+ ", "+str(i[1])+"\n")	
outy.close()	
		

