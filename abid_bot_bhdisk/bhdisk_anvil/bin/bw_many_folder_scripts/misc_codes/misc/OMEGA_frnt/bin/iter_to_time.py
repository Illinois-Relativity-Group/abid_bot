from sys import argv
import os

dt=float(argv[1])
M=float(argv[2])
ini_time=str(argv[3])


#print "Initial time is:" + str(int(float(ini_time)/M)) + "M"


def changing_name (dir):
        for file in os.listdir(dir):
                iter=file[2:-4]
                time=int(float(iter)*dt*10/(M))
                path = os.path.join(dir,file)
                amend = ""
                if len(str(time)) == 1:
                        amend="0000"
                elif len(str(time)) == 2:
                        amend = "000"
                elif len(str(time)) == 3:
                        #print("ey")
                        amend = "00"
		elif len(str(time))==4:
			amend="0"
                dst = file.replace(str(file[2:-4]),amend+str(time))
                os.rename(path,dst)
#os.rename(os.path.join(dir2,file), dst)
        return

changing_name("w_data")
