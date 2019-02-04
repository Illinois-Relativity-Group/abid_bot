# made by Cunwei Fan
# January 20, 2017 (Trump Era begins)
# prepare for density and GW merger
# this code will make two new folders for density plot and GW movies
# so that GW movies will have the same frame number with density plot. 
# to do this, need the t/M for each frame of density plot and t/M for 
# each frame of GW movie.

import sys
import time
import shutil

from os import listdir
from os.path import isfile, join
from fnmatch import fnmatch

##### list the folder directory ########################
root = "/home/colten1/Desktop/NSNS_high_align/bw_images/" 
src_dir_gw = root+"gw"
dst_dir_gw = root+"gw_dir"
src_dir_rho = root+"density"
dst_dir_rho = root+"rho_dir"
gw_time_file = root+ "gw_time_list.txt"
rho_time_file = root+ "den_time_list.txt"
########################################################

def check_slash(dir_name):
	if dir_name[-1] !="/":
		dir_name = dir_name+"/"
	return dir_name

def get_name(file_dir):
	srcfiles = [f for f in listdir(file_dir) if isfile(join(file_dir,f)) and f.find(".png") != -1 ]
	srcfiles.sort()
	return srcfiles
	
def get_time(time_file):
	tfile = open(time_file,"r")
	time_list = []
	for line in tfile:
		t = int(float(line.split()[0]))
		time_list.append(t)
	time_list.sort()
	tfile.close()
	return time_list
	
def padding_slow_with_fast(file_A_list, file_B_list, src_dir_A, dst_dir_A, src_dir_B, dst_dir_B, A_name, B_name):
	# file_A_list is the list of pngs with small time step, (more in total number)
	# file_B_list is the list of pngs with large time step, (less in total number)
	# elements in file_A_list are of form (file_name, time)
	# elements in file_B_list are of form (file_name, time)
	# src_dir_A is the source directory of file_A_list
	# src_dir_B is the source directory of file_B_list
	# A_name is the name you want for the copied A pngs such as "rho_" or "GW_"
	# B_name is the name you want for the copied B pngs such as "rho_" or "GW_"
	# this function will copy file_A_list to new directory with file named with index
	# and copy file_B_list corresponding to A and padding the gaps with B pngs so that
	# the final movie will be smooth.
	B_start = 0
	B_length = len(file_B_list)
	src_dir_A = check_slash(src_dir_A)
	src_dir_B = check_slash(src_dir_B)
	dst_dir_A = check_slash(dst_dir_A)
	dst_dir_B = check_slash(dst_dir_B)
	logs = open("logs.txt","w")
	logs.write("# \t "+ A_name+ " name \t" + A_name+ " time \t" + B_name+ " name \t" + B_name+ " time \n")
	for i in range(len(file_A_list)):
		time_A = file_A_list[i][1]
		src_A = src_dir_A + file_A_list[i][0]
		dst_A = dst_dir_A +A_name+str(i).zfill(5)+".png"
		while time_A >= file_B_list[B_start][1]:
			# find the frame for B that is the nearest frame after the target A 
			B_start += 1 
			if B_start >= B_length:
				print B_name+" files are exhausted "
				print A_name+" files stops at" +str(time_A)
				return        
		index = B_start
		if B_start >= 1:
			time_before = file_B_list[B_start-1][1] # the nearest B frame before target A
			time_after = file_B_list[B_start][1]
			if time_A-time_before <= time_after- time_A:
				index = B_start - 1
		# so that the chosen B is the nearest frame to the target A 
		src_B = src_dir_B + file_B_list[index][0]
		dst_B = dst_dir_B +B_name+str(i).zfill(5)+".png"
		
		shutil.copy2(src_A,dst_A)
		shutil.copy2(src_B,dst_B)
		logs.write(str(i) + "\t" +  file_A_list[i][0] + "\t" +str(time_A) + "\t" + file_B_list[index][0] + "\t" + str(file_B_list[index][1]) +"\n")
	logs.close()
	return
	
#### the main #########################

print "loading GW images ...."
gw_name = get_name(src_dir_gw)
gw_time = get_time(gw_time_file)
file_gw_list = zip(gw_name, gw_time)
print "\t Done"

print "loading density images ...."
rho_name = get_name(src_dir_rho)
rho_time = get_time(rho_time_file)
file_rho_list = zip(rho_name, rho_time)
print len(file_rho_list)
print "\t Done"

print "start copying ...." 	
padding_slow_with_fast(file_gw_list, file_rho_list, src_dir_gw, dst_dir_gw, src_dir_rho, dst_dir_rho, "gw_", "rho_")
print "\t Done"
print "check logs.txt"








	
		
