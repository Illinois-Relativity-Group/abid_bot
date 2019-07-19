from sys import argv
import os

dt=float(argv[1])
M=float(argv[2])
ini_time=str(argv[3])


print "Initial time is:" + str(int(float(ini_time)/M)) + "M"


def changing_name (dir):
        for file in os.listdir(dir):
                iter=file[3:-4]
                time=int((float(iter)*dt+float(ini_time))/M)
                path = os.path.join(dir,file)
                dst = file.replace(str(file[3:-4]),str(time))
                os.rename(path,dst)
#os.rename(os.path.join(dir2,file), dst)
        return

changing_name("vel_data_iter_clean")
