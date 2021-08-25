from shutil import move,rmtree
from os import unlink
from sys import argv

root = argv[1]
duplicate_txt = root + "bin/bw_many_folder_scripts/duplicate.txt"
f = open(duplicate_txt, 'r')
f.readline()
f.readline()
for line in f:
	headerlen=line[:-2].rfind('/')	#root/h5data
	headerlen2=line[:headerlen].rfind('/')	#root
        print("rmdupes: ",line,line[:headerlen],line[headerlen:-1])
	
	try: move(line[:-1],line[:headerlen] + "/bad_data" + line[headerlen:-1])
	except: move(line[:-2],line[:headerlen] + "/bad_data" + line[headerlen:-2])	#for symlinks

	#try: rmtree(line[:-1])		#for actual files
	#except: unlink(line[:-1])	#for symlinks

	try: rmtree(line[:headerlen2]  + "/xml" + line[headerlen:-1])
	except: unlink(line[:headerlen2]  + "/xml" + line[headerlen:-2])
