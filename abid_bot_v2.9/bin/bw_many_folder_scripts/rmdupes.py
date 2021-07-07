from shutil import move,rmtree
from os import unlink
from sys import argv

root = argv[1]
duplicate_txt = root + "bin/bw_many_folder_scripts/duplicate.txt"
f = open(duplicate_txt, 'r')
f.readline()
f.readline()
for line in f:
	print("rmdupes: ",line,line[-22:-1])
	try: move(line[:-1],line[:-22] + "bad_data/" + line[-22:-1])
        except: move(line[:-2],line[:-22] + "bad_data/" + line[-22:-2])

	#try: rmtree(line[:-1])		#for actual files
	#except: unlink(line[:-1])	#for symlinks

	try: rmtree(line[:-29]  + "xml/" + line[-22:-1])
	except: unlink(line[:-29]  + "xml/" + line[-22:-1])
