from shutil import rmtree
from os import unlink
from sys import argv

root = argv[1]
f = open(root + "bin/bw_many_folder_scripts/duplicate.txt", 'r')
f.readline()
f.readline()
for line in f:
	try: rmtree(line[:-1])	
	except: unlink(line[:-1])	

	try: rmtree(line[:-29]  + "xml/" + line[-22:-1])
	except: unlink(line[:-29]  + "xml/" + line[-22:-1])
