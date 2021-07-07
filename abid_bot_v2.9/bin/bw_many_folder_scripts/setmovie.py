# This script sets up the xml files for each frame. This must be done before filming.

# Created by Abid Khan

import sys
import glob
from os import listdir
from os.path import isfile, join
import shutil
from distutils.util import strtobool
import xml.etree.ElementTree as ET
from scipy.interpolate import CubicSpline 

###############################################################################
#load in information about folders etc.
###############################################################################

print(sys.argv)

rootdir = sys.argv[1]
it = int(sys.argv[2])
dt = float(sys.argv[3])
M = float(sys.argv[4])
offset = int(sys.argv[5])
fields = strtobool(sys.argv[6])
numBfieldPlots = int(sys.argv[7])
g00=strtobool(sys.argv[8])
time_offset = float(sys.argv[9])
vol_xml = sys.argv[10]
vol2_xml = sys.argv[11]
view_xml = sys.argv[12]
view2_xml = sys.argv[13]
twoColorsSeeds = strtobool(sys.argv[14])
tracer = strtobool(sys.argv[15])
twoColorsTracer = strtobool(sys.argv[16])
xmldir = sys.argv[17]

rootdir = rootdir if rootdir[-1] == '/' else rootdir + '/'

overlapFile = rootdir + "bin/bw_many_folder_scripts/overlap.txt"
bhdir = rootdir + "bhdata/"
particleseedpath = rootdir + "seeds/"
gridseedpath = rootdir + "seeds/gridseeds/"
trace1path = rootdir + "trace1/"
trace2path = rootdir + "trace2/"
#xmldir = rootdir + "xml/"
cm_file = rootdir + "cm.txt"
attsdir = rootdir + "bin/bw_many_folder_scripts/atts/"

in_file = open(cm_file, 'r')
timeList = []
cmList = []
for line in in_file:
	data = line.split()
	t = float(data[0])
	x = float(data[1])
	y = float(data[2])
	z = float(data[3])
	timeList.append(t)
	cmList.append((x, y, z))
in_file.close()

### These assume that if two color option is true, filenames in the other folder must be the same.
if fields:
	filelist_part = [ f for f in listdir(particleseedpath) if isfile(join(particleseedpath,f)) and f.find(".txt") > 0 ]
	filelist_part.sort()

if tracer:
	filelist_trace = [ f for f in listdir(trace1path) if isfile(join(trace1path,f)) and f.find(".3d") > 0 ]
	filelist_trace.sort()


###############################################################################
#movie functions
###############################################################################

def getFolder(state):
	frame_state=state+1					# Plus 1 for frame_count
	overlap_txt=overlapFile			  
	f_overlap=open(overlap_txt,'r')
	frame_gap = 0
	for n in range(5):					# Skip the first 3 header lines
		f_overlap.readline()
	for line in f_overlap:
		line_str=line.split()
		frame_skip=int(line_str[0])
		if frame_skip < 0:				# Check gap flag
			print("Warning: gap's found in data")
			frame_gap = - frame_skip 
			frame_skip = 0
		frame_total=int(line_str[1])
		folder_path=line_str[2]
		frame_count=frame_total - frame_skip
		if frame_state <= frame_count and frame_state > 0:	
			return folder_path,frame_state - 1	 
		frame_state=frame_state - frame_gap - frame_count
		frame_gap = 0
	print("{} has no corresponding folder due to the gap or the density folder is not complete!".format(state))
	return -1,-1				  # Bad input argument
	f_overlap.close()

# Only get the changing variables
def getViewVariables(viewXML):
	tree = ET.parse(viewXML)
	data = tree.getroot()
	mylist = []
	for i in [0,1,2]:
		mylist += [ float(f) for f in data[i].text.split() ]	#viewNormal	
	#mylist += [ float(f) for f in data[0].text.split() ]	#viewNormal
	#mylist += [ float(f) for f in data[1].text.split() ]	#focus
	#mylist += [ float(f) for f in data[2].text.split() ]	#viewUp
	for i in [4,5,6,8]:
		mylist.append(float(data[i].text))	#parallelScale
	#mylist.append(float(data[4].text))	#parallelScale
	#mylist.append(float(data[5].text))	#nearPlane
	#mylist.append(float(data[6].text))	#farPlane
	#mylist.append(float(data[8].text))	#imageZoom
	return mylist

# Only get opacity attenuation and free form opacity.
def getVolVariables(volXML):
	tree = ET.parse(volXML)
	data = tree.getroot()
	mylist = []
	mylist += [ int(f) for f in data[10].text.split() ]	#freeformOpacity (postion 0-255) 
	mylist.append(float(data[3].text))	#opacityAttenuation (position 256)
	return mylist

# Load an existing viewXML to copy the structure of the view xml file.
# Then write the values in varlist to outputXML.
def writeViewVariables(varlist, viewXML, outputXML):
	if not len(varlist) == 13:
		print("Error! : total numbers of variables is not 13. len = ", len(varlist))
		return 0
	tree = ET.parse(viewXML)
	data = tree.getroot()
	data[0].text = str(varlist[0]) + " " + str(varlist[1]) + " " + str(varlist[2])
	data[1].text = str(varlist[3]) + " " + str(varlist[4]) + " " + str(varlist[5])
	data[2].text = str(varlist[6]) + " " + str(varlist[7]) + " " + str(varlist[8])
	data[4].text = str(varlist[9])
	data[5].text = str(varlist[10])
	data[6].text = str(varlist[11])
	data[8].text = str(varlist[12])
	# Change empty elements to whitespace. This is necessary because VisIt does not understand
	# that in XML <Field /> and <Field></Field> are equivalent.
	for field in data.iter('Field'):
		if field.text == None:
			field.text = " "
	tree.write(outputXML, encoding='UTF-8', xml_declaration=True)
	print("View File: {}".format(viewXML))
	print("XML File:  {}\n".format(outputXML))
	return 1

def writeVolVariables(varlist, volXML, outputXML):
	if not len(varlist) == 257:
		print("Error! : total numbers of varibles is not 257. len = ", len(varlist))
		return 0
	tree = ET.parse(volXML)
	data = tree.getroot()
	freeform = [ str(int(f)) for f in varlist[0:256] ]
	data[10].text = " ".join(freeform)
	data[3].text = str(varlist[256])
	# Change empty elements to whitespace. This is necessary because VisIt does not understand
	# that in XML <Field /> and <Field></Field> are equivalent.
	for field in data.iter('Field'):
		if field.text == None:
			field.text = " "
	tree.write(outputXML, encoding='UTF-8', xml_declaration=True)
	print("Vol File: {}".format(volXML))
	print("XML File: {}".format(outputXML))
	print() #space to make it look pretty

# cpts should be (<initial variable list>, <final variable list>)
def evalCubicSpline(t, x, cpts):
	Cubic = CubicSpline(x, cpts)
	return Cubic.__call__(t)


def run_mov_change_attribute(first_frame, last_frame, view_initial, view_final, vol_initial, vol_final):

	first_step = first_frame + offset
	last_step = last_frame + offset

	for state in range(first_step,last_step,1):
		
		gotFolder,index = getFolder(state)
		if gotFolder == -1:
			continue
		print("Folder: {}".format(gotFolder))
		print("Index:  {}\n".format(index))
		h5_idx = gotFolder.find("3d_data")
		saveFolder = xmldir + gotFolder[h5_idx:]

		####copy bhdata###
		for idx in ['1', '2', '3']:
			src = bhdir + 'ht' + idx + '_' + str(it*state).zfill(7) + '.3d'
			dst = saveFolder + 'bh' + idx + '_' + str(index).zfill(6) + '.3d'
			if isfile(src):
				print("BH found\n")
				shutil.copy2(src, dst)
		##################

		###copy particle seed data###
		if fields: #need '- offset' as first file is at first time with particle data,
			indexstep = state - offset #filelist[0] = seeds[firsttime]
			if(indexstep >= len(filelist_part)):
				indexstep = len(filelist_part) - 1
			src_list = sorted(glob.glob(particleseedpath + "{:0>7d}*".format(state)))
			stream_src_list = sorted(glob.glob(attsdir + "Stream_?.xml"))
			for src,stream_src in zip(src_list,stream_src_list):
				append_str = "_" + src[-5]
				dst = saveFolder + "particle_seeds_" + str(index).zfill(4) + append_str + ".txt"
				if isfile(src):
					print("Seed File: {}".format(src))
					print("XML File:  {}\n".format(dst))
					shutil.copy2(src,dst)
				
				stream_dst = saveFolder + "Stream_" + str(index).zfill(4) + append_str + ".xml"
				if isfile(stream_src):
					print("Stream File: {}".format(stream_src))
					print("XML File: {}\n".format(stream_dst))
					shutil.copy2(stream_src,stream_dst)
		
			if twoColorsSeeds:
				src = gridseedpath + "{:0>7d}.txt".format(state)
				#src = gridseedpath + filelist_part[indexstep]
				dst = saveFolder + "grid_seeds_" + str(index).zfill(4) + ".txt"
				if isfile(src):
					print("Second Color Seed File: {}".format(src))
					print("Second Color XML File:  {}\n".format(dst))
					shutil.copy2(src,dst)

		#############################

		###copy particle tracer data###
		if tracer:
			indexstep = state #- offset #might need -offset
			if(indexstep >= len(filelist_trace)):
				indexstep = len(filelist_trace) - 1

			src = trace1path + filelist_trace[indexstep]
			dst = saveFolder + "trace1_" + str(index).zfill(4) + ".3d"
			print("Trace File: {}".format(src))
			print("XML File:   {}\n".format(dst))
			shutil.copy2(src,dst)
		
			if twoColorsTracer:
				src = trace2path + filelist_trace[indexstep]
				dst = saveFolder + "trace2_" + str(index).zfill(4) + ".3d"
				print("Trace2 File: {}".format(src))
				print("XML2 File:   {}\n".format(dst))
				shutil.copy2(src,dst)
			
		#############################
		
		### write time varying view and vol ###
		view_cpts = (getViewVariables(view_initial), getViewVariables(view_final))
		vol_cpts = (getVolVariables(vol_initial), getVolVariables(vol_final))
		current_t = float(state - first_step)/float(last_step - first_step)
		x = [0,1]
		
		view_c = evalCubicSpline(current_t, x, view_cpts)
		viewpath = saveFolder + "view_" + str(index).zfill(4) + ".xml"
		writeViewVariables(view_c, view_initial, viewpath)

		vol_c = evalCubicSpline(current_t, x, vol_cpts)
		volpath = saveFolder + "volume_" + str(index).zfill(4) + ".xml"
		writeVolVariables(vol_c, vol_initial, volpath)
		#######################################

		###copy cm and time data###
		myTime = state*dt + time_offset
		tList = [ abs(x - myTime) for x in timeList ]
		pos = tList.index(min(tList))
		cm = cmList[pos]

		tidex = "{:07.2f}".format(float(myTime/M))
		timeTXT = "{}time_{}.txt".format(saveFolder,tidex) 
		f = open(timeTXT, 'w')
		f.write(str(cm[0]) + "\t" + str(cm[1]) + "\t" + str(cm[2]))
		f.close()
		###########################

def run_mov_fixed_view(first_frame,last_frame,view,vol):
	run_mov_change_attribute(first_frame, last_frame, view, view, vol, vol)

def getTotalNumberOfFrames():
	f_overlap=open(overlapFile,'r')
	#skip the header
	for n in range(5):					# Skip the first 3 header lines
		f_overlap.readline()

	#iterate through each line of the file. 
	#Subtract the first column from the second
	#to get the number of frames filmed in that 
	#folder. repeat and sum for all of the folders 
	tot_number_of_frames = 0

	for line in f_overlap:
		line_str=line.split()
		col1 = max(int(line_str[0]),0)
		col2 = int(line_str[1])
		tot_number_of_frames += col2 - col1

	print("There are {} frames!\n".format(tot_number_of_frames))
	f_overlap.close()
	return tot_number_of_frames


###############################################################################
#run movie functions
###############################################################################
# if you want you can do something like 
#
#run_mov_fixed_view(0, 30, view_xml, vol_xml)
#run_mov_change_attribute(30, 60, view_xml, view2_xml, vol_xml, vol2_xml)
#run_mov_fixed_view(60, getTotalNumberOfFrames(), view2_xml, vol2_xml)
#


run_mov_fixed_view(0, getTotalNumberOfFrames(), view_xml, vol_xml)
