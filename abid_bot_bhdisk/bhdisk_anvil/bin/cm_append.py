#This file appends "bhcen.txt" to "cm.txt".  

from sys import argv
from os.path import isfile
from os import rename

rootdir = argv[1]
griddir = rootdir + "bin/grid_code/"

cmFile = rootdir + "cm.txt"
already_made = isfile(rootdir + "cm.txt")

outFile = open(rootdir + "cm_tmp.txt", 'w')
with open(griddir + "bhcen1.txt", 'r') as bhFile:
        if already_made:
                bh_line = bhFile.readline()
                bh_data = bh_line.split()
                bh_time = float(bh_data[0])

                for line in open(cmFile, 'r'):
                        cm_data = line.split()
                        cm_time = float(cm_data[0])
                        if cm_time >= bh_time:
                                break
                        outFile.write(line)

if isfile(griddir + "bhcen2.txt"):
        with open(griddir + "bhcen1.txt", 'r') as bh1File,\
             open(griddir + "bhcen2.txt", 'r') as bh2File:
                for line1, line2 in zip(bh1File, bh2File):
                        bh1_data, bh2_data = line1.split(), line2.split()

                        t = bh1_data[0]
                        x1,y1,z1 = bh1_data[1:4]
                        x2,y2,z2 = bh2_data[1:4]

                        x = (float(x1) + float(x2)) / 2
                        y = (float(y1) + float(y2)) / 2
                        z = (float(z1) + float(z2)) / 2
                        outFile.write(str(t) +"\t"+ str(x) +"\t"+ str(y) +"\t"+ str(z) +"\n")
else:
        with open(griddir + "bhcen1.txt", 'r') as bhFile:
                for line in bhFile:
                        outFile.write(line)
outFile.close()

rename(rootdir + "cm_tmp.txt", rootdir + "cm.txt")
