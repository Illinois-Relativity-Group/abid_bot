from shutil import rmtree
from sys import argv

root = argv[1]
f = open(root + "bin/bw_many_folder_scripts/duplicate.txt", 'r')
f.readline()
f.readline()
for line in f:
	rmtree(line[:-1])	
	rmtree(line[:-29]  + "xml/" + line[-22:-1])
