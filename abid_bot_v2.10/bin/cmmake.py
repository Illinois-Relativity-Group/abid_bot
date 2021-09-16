# This script takes in 'bhns.xon' and returns a text file, 'cm.txt' which is the center of the frame of the system. 
# @params
# 	num_stars: 1 if we're dealing with just one stellar mass (e.g. SMS) or 2 if we're dealing with a binary (e.g. BHNS, NSNS, BHBH).

from sys import argv

num_stars = int(argv[1])
root = argv[2]
in_file = open(root + "h5data/bhns.xon", 'r')
out_file = open(root + "cm.txt", 'w')

for line in in_file:
	data = line.split()
	if data[0] == '#':
		continue
	t = float(data[0])
	if num_stars == 1: 
		x = float(data[1])
		y = float(data[2])
	elif num_stars == 2:
		x = (float(data[1]) + float(data[3]))/2
		y = (float(data[2]) + float(data[4]))/2
	else:
		print("error! num_stars incorrectly inputted")
		out_file.close()
		in_file.close()
		exit()

	out_file.write(str(t) + "\t" + str(x) + "\t" + str(y) + "\t0\n")

out_file.close()
in_file.close()
