#This file appends "bhcen.txt" to "cm.txt".  

from sys import argv
from os.path import isfile
from os import rename

rootdir = argv[1]
griddir = rootdir + "bin/grid_code/"

cmFile = rootdir + "cm.txt"
already_made = isfile(rootdir + "cm.txt")
outFile = open(rootdir + "cm_tmp.txt", 'w')

bhFile = open(griddir + "bhcen1.txt", 'r')
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
bhFile.close()

if isfile(griddir + "bhcen2.txt"):
	bh1File = open(griddir + "bhcen1.txt", 'r')
	bh2File = open(griddir + "bhcen2.txt", 'r')
	for line1, line2 in zip(bh1File, bh2File):
		bh1_data = line1.split()
		bh2_data = line2.split()
		x = 0.5*(float(bh1_data[1]) + float(bh2_data[1]))
		y = 0.5*(float(bh1_data[2]) + float(bh2_data[2]))
		z = 0.5*(float(bh1_data[3]) + float(bh2_data[3]))
		outFile.write(str(bh1_data[0]) + "\t" + str(x) + "\t" + str(y) + "\t" + str(z) + "\n")
	bh2File.close()
else:
	bhFile = open(griddir + "bhcen1.txt", 'r')
	for line in bhFile:
		outFile.write(line)
	bhFile.close()
outFile.close()
rename(rootdir + "cm_tmp.txt", rootdir + "cm.txt")

