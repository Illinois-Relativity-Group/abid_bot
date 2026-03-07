#Created by Brian Taylor

#This script runs the movie once you have created all the necessary xml files
#It's still being writen, obviously.

#Source("/home/projects/bhbh_mag_inspiral_extras/many_folders_code/run_movie.py")

#Run with something like visit -cli -nowin -s run_movie.py "h5dir" "extrasDir" "bhdir" "savefolder"

import random
import csv
import sys
import time
import RotationMatrix as RM

from os import listdir, rename
from os.path import isfile, join
from fnmatch import fnmatch
from math import pi, sin, cos, tan, atan2, sqrt

###############################################################################
#search for all the necessary data (preprocessing)
###############################################################################

print(sys.argv)

rank = int(sys.argv[6])
total_ranks = int(sys.argv[7])
saveFolder=sys.argv[8]
root_dir = sys.argv[9]
h5dir = sys.argv[10]
extrasDir = sys.argv[11] 
streamXML = sys.argv[12]
vectorXML = sys.argv[13]
max_density = sys.argv[14]
index = int(sys.argv[15])

tot_frames = 10
frame_start = int(round((float(rank)/total_ranks)*tot_frames))
frame_end = int(round(((rank+1.0)/total_ranks)*tot_frames))

saveFolder = saveFolder + str(rank).zfill(3)+"_"

time.strftime("%Y-%m-%d %H:%M:%S")


#append a '/' if necessary
if(h5dir[-1] != '/'):
	h5dir = h5dir + '/'
if(extrasDir[-1] != '/'):
	extrasDir = extrasDir + '/'

#The first line picks out the files that contain "volume_" in the directory, extrasDir
#The sorting should sort in numerical order

volumeXML = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("volume_")	!= -1 ]
volumeXML.sort()
print("volumeXML",volumeXML)

particlesTXT = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("particle_seeds_") != -1 ]
particlesTXT.sort()

gridPointsTXT = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("grid_seeds_") != -1 ]
gridPointsTXT.sort()

viewXML = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("view_") != -1 ]
viewXML.sort()

timeTXT = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("time_") != -1 ]
timeTXT.sort()

bh3D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh1_") != -1 ]
bh3D.sort()

bh23D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh2_") != -1 ]
bh23D.sort()

bh33D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh3_") != -1 ]
bh33D.sort()

trace3D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("trace1_") != -1 ]
trace3D.sort()

trace23D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("trace2_") != -1 ]
trace23D.sort()


#make a copy of viewXML and turn it into numbers by removing "view_" and ".xml"
stateList = viewXML[:]
for i in range(len(stateList)):
	stateList[i] = int(stateList[i][-8:-4])

stateList.sort()
print("statList ",stateList)

def bh_formed():
	return len(bh3D) > 0 

def binary_formed():
	return len(bh23D) > 0 

def merge_formed():
	return len(bh33D) > 0 

def trace1():
	return len(trace3D) > 0

def trace2():
	return len(trace23D) > 0

def particles():
	return len(particlesTXT) > 0

def gridPoints():
	return len(gridPointsTXT) > 0		

def fields():
	return particles() or gridPoints()


#This adjusts the bh_*.3d files so that the black hole doesn't show up earlier than it's supposed to
#This will use bh3 data to overwrite the empty bh1 and bh2 files whenever bh1 and bh3 appear together in one folder. 
def fill_bh(bh_func, stri):
	if bh_func:
		for i in stateList:
			bhFile = extrasDir + 'bh' + stri + '_' + str(i).zfill(6) + '.3d'
			if stri == '3' and bh_formed() and isfile(bhFile):
				f = open(bhFile, 'r')
				g = open( extrasDir + 'bh1_' + str(i).zfill(6) + '.3d', 'w')
				h = open( extrasDir + 'bh2_' + str(i).zfill(6) + '.3d', 'w')
				f.readline()
				g.write("x\ty\tz\tbh1p\n")
				h.write("x\ty\tz\tbh2p\n")
				for line in f:
					g.write(line)
					h.write(line)
				f.close()
				g.close()
				h.close()
				rename(bhFile, extrasDir + 'unused3_' + str(i).zfill(6) + '.3d')
			elif not stri == '3' and not isfile(bhFile):
				f = open(bhFile, 'w')
				f.write("x\ty\tz\tbh" + stri + "p\n")
				f.write("0\t0\t0\t0")
				f.close()

fill_bh(bh_formed(), '1')
fill_bh(binary_formed(), '2')
fill_bh(merge_formed(), '3')

#Checking bh files again ################
bh3D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh1_") != -1 ]
bh3D.sort()

bh23D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh2_") != -1 ]
bh23D.sort()

bh33D = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("bh3_") != -1 ]
bh33D.sort()



print("bh_formed: ", bh_formed())
print("fields: ", fields())
print("particles: ", particles())
print("gridPoints: ", gridPoints())
print("trace1: ", trace1())
print("trace2: ", trace2())

###############################################################################
#load the databases
###############################################################################

Bxdir = h5dir + "Bx.file_* database"
Bydir = h5dir + "By.file_* database"
Bzdir = h5dir + "Bz.file_* database"
rho_bdir = h5dir + "rho_b.file_* database"
bh1dir = extrasDir + "bh1_*.3d database"
bh2dir = extrasDir + "bh2_*.3d database"
bh3dir = extrasDir + "bh3_*.3d database"
trace1dir = extrasDir + "trace1_*.3d database"
trace2dir = extrasDir + "trace2_*.3d database"


print("Loading rho...")
OpenDatabase(rho_bdir,0,"CarpetHDF5_2.1")
print("\tDone")
DefineScalarExpression("rho_b","conn_cmfe(<" + rho_bdir + "[0]id:MHD_EVOLVE--rho_b>, <Carpet AMR-grid>)")
DefineScalarExpression("logrha","log10(<MHD_EVOLVE--rho_b>/" + max_density + ")")

if fields():
	print("Loading Bx...")
	OpenDatabase(Bxdir,0,"CarpetHDF5_2.1")
	print("\tDone")

	print("Loading By...")
	OpenDatabase(Bydir,0,"CarpetHDF5_2.1")
	print("\tDone")

	print("Loading Bz...")
	OpenDatabase(Bzdir,0,"CarpetHDF5_2.1")
	print("\tDone")

	DefineScalarExpression("Bx","conn_cmfe(<" + Bxdir + "[0]id:MHD_EVOLVE--Bx>, <Carpet AMR-grid>)")
	DefineScalarExpression("By","conn_cmfe(<" + Bydir + "[0]id:MHD_EVOLVE--By>, <Carpet AMR-grid>)")
	DefineScalarExpression("Bz","conn_cmfe(<" + Bzdir + "[0]id:MHD_EVOLVE--Bz>, <Carpet AMR-grid>)")
	DefineVectorExpression("BVec","{Bx,By,Bz}")

if bh_formed():
	print("Loading bh's...")
	OpenDatabase(bh1dir)
if binary_formed():
	print("Loading bh's 2...")
	OpenDatabase(bh2dir)
if merge_formed():
	print("Loading bh's 3...")
	OpenDatabase(bh3dir)
if trace1():
	print("Loading Particle Tracer...")
	OpenDatabase(trace1dir)
if trace2():
	print("Loading Particle Tracer 2...")
	OpenDatabase(trace2dir)

print("\tDone")

dbs = [rho_bdir]
if fields():
	dbs += [Bxdir, Bydir, Bzdir]
if bh_formed():
	dbs += [bh1dir] 
if binary_formed():
	dbs += [bh2dir]
if merge_formed():
	dbs += [bh3dir] 
if trace1():
	dbs += [trace1dir]
if trace2():
	dbs += [trace2dir]
print("Database loaded: ", dbs)

CreateDatabaseCorrelation("Everything", dbs, 0)

time.strftime("%Y-%m-%d %H:%M:%S")
###############################################################################
#load the plots
###############################################################################

plot_idx = ["density"]
if particles():
	plot_idx += ["particles"]
if gridPoints():
	plot_idx += ["gridPoints"]
if bh_formed():
	plot_idx += ["bh"]
if binary_formed():
	plot_idx += ["bh2"]
if merge_formed():
	plot_idx += ["bh3"]
if trace1():
	plot_idx += ["trace1"]
if trace2():
	plot_idx += ["trace2"]
print("Plotting: ", plot_idx)
# Use plot_idx.index("plot name") to find its idx
def idx(name):
	return plot_idx.index(name)

DeleteAllPlots()

ref = ReflectAttributes()
ref.reflections = (1,0,0,0,1,0,0,0)

#add Density Volume Plot (0)################
ActivateDatabase(rho_bdir)
AddPlot("Volume","logrha")	   #plot 0
print("Add density volume plot with index = ", idx("density"))

vol = VolumeAttributes()
SetActivePlots(idx("density"))

AddOperator("Reflect")
SetOperatorOptions(ref)

#add particles-seeded Streamline Plot (1)####################
if particles():
	ActivateDatabase(Bxdir)
	AddPlot("Streamline","BVec")	#plot 1
	print("Add particles-seeded streamline plot with index = ", idx("particles"))

	SetActivePlots(idx("particles"))

	AddOperator("Reflect")
	SetOperatorOptions(ref)

	stream_particles = StreamlineAttributes()

#add gridPoints-seeded Streamline Plot (gridPoints_idx)#######
if gridPoints():
	ActivateDatabase(Bxdir)
	AddPlot("Streamline","BVec")	#plot 1
	print("Add gridPoints-seeded streamline plot with index = ", idx("gridPoints"))

	SetActivePlots(idx("gridPoints"))

	AddOperator("Reflect")
	SetOperatorOptions(ref)

	stream_gridPoints = StreamlineAttributes()


#add bhplots (bh_idx) ########################
if bh_formed():
	ActivateDatabase(bh1dir)
	AddPlot("Pseudocolor","bh1p")
	print("Add bh1 plot with index = ", idx("bh"))

	Pseudo = PseudocolorAttributes()
	SetActivePlots(idx("bh"))
	AddOperator("Delaunay")
	AddOperator("Reflect")
	SetOperatorOptions(ref)

	Pseudo.colorTableName = "gray"
	Pseudo.legendFlag = 0
	Pseudo.lightingFlag = 0

	SetPlotOptions(Pseudo)

if binary_formed():
	ActivateDatabase(bh2dir)
	AddPlot("Pseudocolor","bh2p")
	print("Add bh2 plot with index = ", idx("bh2"))

	Pseudo = PseudocolorAttributes()
	SetActivePlots(idx("bh2"))
	AddOperator("Delaunay")
	AddOperator("Reflect")
	SetOperatorOptions(ref)

	Pseudo.colorTableName = "gray"
	Pseudo.legendFlag = 0
	Pseudo.lightingFlag = 0

	SetPlotOptions(Pseudo)

if merge_formed():
	ActivateDatabase(bh3dir)
	AddPlot("Pseudocolor","bh3p")
	print("Add bh3 plot with index = ", idx("bh3"))

	Pseudo = PseudocolorAttributes()
	SetActivePlots(idx("bh3"))
	AddOperator("Delaunay")
	AddOperator("Reflect")
	SetOperatorOptions(ref)

	Pseudo.colorTableName = "gray"
	Pseudo.legendFlag = 0
	Pseudo.lightingFlag = 0

	SetPlotOptions(Pseudo)
	

#add particle tracer plots ###############
if trace1():
	ActivateDatabase(trace1dir)
	AddPlot("Pseudocolor", "rho")
	print("Add trace1 plot with index = ", idx("trace1"))

	SetActivePlots(idx("trace1"))
	pointAtt = PseudocolorAttributes()
	pointAtt.pointType = pointAtt.Sphere
	pointAtt.pointSizePixels = 8   #8 or 10 if you use 2 colors 
	pointAtt.minFlag = 1
	pointAtt.min = -1
	pointAtt.maxFlag = 1
	pointAtt.max = 0
	pointAtt.legendFlag = 0
	pointAtt.lightingFlag = 0
	SetPlotOptions(pointAtt)

#add smaller green particle tracer ########	
if trace2():
	ActivateDatabase(trace2dir)
	AddPlot("Pseudocolor", "rho")
	print("Add trace2 plot with index = ", idx("trace2"))

	SetActivePlots(idx("trace2"))
	pointAtt = PseudocolorAttributes()
	pointAtt.pointType = pointAtt.Sphere
	pointAtt.pointSizePixels = 4
	pointAtt.colorTableName = "PiYG" #Green at position 1
	pointAtt.minFlag = 1
	pointAtt.min = -1
	pointAtt.maxFlag = 1
	pointAtt.max = 0
	pointAtt.legendFlag = 0
	pointAtt.lightingFlag = 0
	SetPlotOptions(pointAtt)

myView = GetView3D()
DrawPlots()
###############################################################################
#set up the annotations
###############################################################################

#Annotations and View ########################

Ann = AnnotationAttributes()
Ann.backgroundMode = Ann.Solid
Ann.backgroundColor = (55,118,255,255) #stu blue
#Ann.backgroundColor = (0,0,0,255) #black
#Ann.legendFlag = 0
Ann.databaseInfoFlag = 0
Ann.userInfoFlag = 0
Ann.axes3D.visible = 0
Ann.axes3D.triadFlag = 0
Ann.axes3D.bboxFlag = 0
SetAnnotationAttributes(Ann)

# Clock
txt = CreateAnnotationObject("Text2D")
txt.position = (0.75, 0.95) # (x,y), where x and y range from 0 to 1
txt.useForegroundForTextColor = 0
txt.textColor = (255, 255, 255, 255)
txt.fontBold = 1
txt.fontFamily = txt.Times # Because I think Times looks cooler

print("Annotations set up")

###############################################################################
#save window settings
###############################################################################

s = SaveWindowAttributes()
s.format = s.PNG
s.fileName = saveFolder
s.width = 1920 
s.height = 1080
s.screenCapture = 0
s.stereo = 0 #Setting for 3D movie
s.resConstraint = s.NoConstraint
SetSaveWindowAttributes(s)

###############################################################################
#start the movie
###############################################################################

print("starting filming")
time.strftime("%Y-%m-%d %H:%M:%S")

state = stateList[index]

print("loading state ", state)
SetTimeSliderState(state)

tcur = timeTXT[state][5:-4]
print("t/M = %g" % int(float(tcur)))
txt.text = "t/M = %g" % int(float(tcur))

print(extrasDir + volumeXML[state])
time.strftime("%Y-%m-%d %H:%M:%S")

print("loading options")

print(LoadAttribute(extrasDir + volumeXML[state], vol) )
print(LoadAttribute(extrasDir + viewXML[state], myView))
if particles():
	print(LoadAttribute(streamXML, stream_particles))
	### change point particles ###
	file1 = open(extrasDir + particlesTXT[state],'r')
	data1 = csv.reader(file1,delimiter='\t')
	table1 = [row for row in data1]
	d1 = []
	for i in range(len(table1)):
		for j in range(len(table1[i])):
			d1.append(table1[i][j])
	d1 = map(float,d1)
	mytuple1 = tuple(d1)
	stream_particles.pointList = mytuple1
	#Change color to green when both grid points and particles appear.
	if gridPoints():		
		stream_particles.singleColor = (0, 255, 0, 255)			
	############################
		
if gridPoints():
	print(LoadAttribute(streamXML, stream_gridPoints))
	### change point particles ###
	file1 = open(extrasDir + gridPointsTXT[state],'r')
	data1 = csv.reader(file1,delimiter='\t')
	table1 = [row for row in data1]
	d1 = []
	for i in range(len(table1)):
		for j in range(len(table1[i])):
			d1.append(table1[i][j])
	d1 = map(float,d1)
	mytuple1 = tuple(d1)
	stream_gridPoints.pointList = mytuple1
	############################

### adjust the cm focus ###
cmfile = open(extrasDir + timeTXT[state], 'r')
cmarray = cmfile.readline().split()
x = float(cmarray[0])
y = float(cmarray[1])
z = float(cmarray[2])
CoM = (x,y,z)
###########################Load view

c1 = View3DAttributes()
LoadAttribute(extrasDir + viewXML[state], c1)


######implement loaded plot settings
print("setting settings")
print(SetActivePlots(idx("density")), SetPlotOptions(vol))
if particles():
	print(SetActivePlots(idx("particles")), SetPlotOptions(stream_particles))
if gridPoints():
	print(SetActivePlots(idx("gridPoints")), SetPlotOptions(stream_gridPoints))


def cross(a,b):
	x=a[1]*b[2]-a[2]*b[1]
	y=a[2]*b[0]-a[0]*b[2]
	z=a[0]*b[1]-a[1]*b[0]
	return (x,y,z)

def newton(x,f,y):#	adjust initial theta to match new theta not theta0, newtons method on eqn
	#				x+f*sin(2x)-y=0
	for i in range (0,10):
		x=x-(x+f*sin(2*x)-y)/(1+2*f*cos(2*x))
	return x


def rotate(view, nsteps, frame_start, frame_end):
	print("Rotating")

	ctrig = view
	myViewNormal = ctrig.viewNormal
	myViewUp = ctrig.viewUp


	print("frame start: " + str(frame_start) + "\tframe_end: " + str(frame_end))
	for i in range(frame_start, frame_end,1):
		#TODO: Change factor as wanted
		factor=0.4#factor slows down rotation when looking into jet,
		#			higher value slows down more.  0<factor<0.5
		#			factor=0: spins at constant rate
		#			factor=0.5: comes to instantaeneous stop at top & bottom
		theta = 2*pi*i/(nsteps)#(n-1) makes last frame same as first

		xhat=myViewNormal[0]
		yhat=myViewNormal[1]
		zhat=myViewNormal[2]

		rhat=sqrt(xhat*xhat+yhat*yhat)
		theta0=atan2(zhat,rhat)
		theta0=newton(theta0,factor,theta0)

		theta_temp=theta0+theta
		theta_new=theta_temp+factor*sin(2*theta_temp)
		

		z_new=sin(theta_new)
		y_new=cos(theta_new)*(yhat/rhat)
		x_new=cos(theta_new)*(xhat/rhat)
		viewNormal = (x_new, y_new, z_new)
		print("Normal ", viewNormal)
		perp=cross((xhat,yhat,0),(0,0,zhat))
		print("perp ", perp)
		viewUp=cross(perp,viewNormal)
		print("up: ", viewUp)
		#viewNormal = (myViewNormal[0]*(cos(theta) - sin(theta)), myViewNormal[1]*(cos(theta) - sin(theta)), myViewNormal[2]*(cos(theta) + sin(theta)))
		#viewUp = (myViewUp[0]*(cos(theta) + sin(theta)), myViewUp[1]*(cos(theta) + sin(theta)), myViewUp[2]*(cos(theta) - sin(theta)))



		c= View3DAttributes()
		c = view
		c.viewNormal = viewNormal
		c.focus = CoM
		c.viewUp = viewUp
		#c.viewAngle = 30
		#c.parallelScale = 1800.73
		#c.nearPlane = -3601.45
		#c.farPlane = 3601.45
		#c.imagePan = (0, 0)
		#c.imageZoom = 6.7
		#c.perspective = 1
		#c.eyeAngle = 2
		#c.centerOfRotationSet = 0
		#c.centerOfRotation = (1.16217, 1.16217, 0)
		#c.axis3DScaleFlag = 0
		#c.axis3DScales = (1, 1, 1)
		#c.shear = (0, 0, 1)

		SetView3D(c)
		DrawPlots()
		SaveWindow()

DrawPlots()
SetView3D(c1)
rotate(c1, tot_frames, frame_start, frame_end)


xmltxt='/'.join(saveFolder.split('/')[:-1])+'/xml.txt'
if(isfile(xmltxt)==0):
	xt=open(xmltxt,'w')
	xt.write('vol:\n')
	xt.write(str(vol))
	xt.write('\n\n\n\nview:\n')
	xt.write(str(myView))
	xt.close

sys.exit()
