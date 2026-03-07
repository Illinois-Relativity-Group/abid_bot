import numpy as np
from sys import argv
import os
import shutil

dlist=[file for file in os.listdir(".") if file.startswith("3d_data_")]

print(dlist[0])

for d in dlist:
    data=[file for file in os.listdir(d) if file.startswith("Bx")]
    #timelist.sort()
    #print(data)
    if len(data)<5:
        print("bad folder "+d)
        try: shutil.move(d,"bad_data/")
        except: os.remove(d)
        continue

    try:
        f=open(d+"/"+data[0],"r")
        f.close()
    except IOError:
        print(d+"/"+data[0])
        shutil.move(d,"bad_data/")
        


