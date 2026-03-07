from shutil import move,rmtree
from os import unlink
from sys import argv

root = argv[1]
f = open(root + "bin/bw_many_folder_scripts/duplicate.txt", 'r')
f.readline()
f.readline()
for line in f:
	move(line[:-1],line[:-22] + "bad_data/" + line[-22:-1])

	#try: rmtree(line[:-1])		#for actual files
	#except: unlink(line[:-1])	#for symlinks

	try: rmtree(line[:-29]  + "xml/" + line[-22:-1])
	except: unlink(line[:-29]  + "xml/" + line[-22:-1])
