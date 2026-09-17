import shutil
import os
import numpy as np


fols = sorted(os.listdir("xml/"))
src1 = "seeds_0.txt"
src2 = "bin/bw_many_folder_scripts/atts/Stream_1.xml"


for fol in fols:
    timelist=[file for file in os.listdir("xml/" + fol) if file.startswith("time_")]
    timelist.sort()
    for i in range(0,len(timelist)):
        dst1 = "xml/" + fol + "/particle_seeds_{}_0.txt".format(str(i).zfill(4))
        dst2 = "xml/" + fol + "/Stream_{}_0.xml".format(str(i).zfill(4))
        shutil.copy(src1, dst1)
        shutil.copy(src2, dst2)




