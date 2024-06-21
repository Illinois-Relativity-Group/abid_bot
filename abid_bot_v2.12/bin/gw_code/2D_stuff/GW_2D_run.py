
#qsub -N $jobName"_"$rank -v VISITSCRIPT=$visitScript,KIND=$kind,GWDIR=$GWdir,SAVEFOLDER=$tosave"_",RANK=$rank,TOTRANKS=$totranks $pbsfile

import random
import csv
import sys
import time

from os import listdir
from os.path import isfile, join
from fnmatch import fnmatch


print(sys.argv)

##### get arguments
kind = sys.argv[1]
GWdir = sys.argv[2]   #gwdata/2D
saveFolder = sys.argv[3]
rank = int(sys.argv[4])
total_ranks = int(sys.argv[5])
#stoptime = int(sys.argv[11])
gw_dt = float(sys.argv[6])
ADM_mass = float(sys.argv[7])
wave_zone_r = float(sys.argv[8])

time.strftime("%Y-%m-%d %H:%M:%S")
print(time.strftime("%Y-%m-%d %H:%M:%S"))

if (GWdir[-1] != '/'):
	GWdir= GWdir +'/'
###### get lists of the files
hcrossfiles = [f for f in listdir(GWdir) if isfile(join(GWdir,f)) and f.find("hcross") != -1 ]
hplusfiles = [f for f in listdir(GWdir) if isfile(join(GWdir,f)) and f.find("hplus") != -1 ]

for i in range(len(hcrossfiles)):
	hcrossfiles[i]=int(round(int(hcrossfiles[i][7:-4])*gw_dt/ADM_mass))

for i in range(len(hplusfiles)):
	hplusfiles[i]=int(round(int(hplusfiles[i][6:-4])*gw_dt/ADM_mass))

hcrossfiles.sort()
hplusfiles.sort()
	
###### load databases
hcrossdir = GWdir + "hcross_*.vtk database"
hplusdir = GWdir + "hplus_*.vtk database"

if kind == "hcross":
	print("Loading hcross....")
	OpenDatabase(hcrossdir,0)
	print("\t Done")

elif kind == "hplus":
	print("Loading hplus....")
	OpenDatabase(hplusdir,0)
	print("\t Done")
else:
	print("error")
	print(kind)
	sys.exit()

DefineScalarExpression("modifiedwave", "<GW-FIELD>/(exp(-polar_radius(mesh)+10)+1)/(exp(-70 +polar_radius(mesh))+1)")

time.strftime("%Y-%m-%d %H:%M:%S")
print(time.strftime("%Y-%m-%d %H:%M:%S"))

##########################################################################
# load the plot
##########################################################################

DeleteAllPlots()


AddPlot("Pseudocolor", "GW-FIELD")
Pseudo = PseudocolorAttributes()
Pseudo.colorTableName = "gw_plane"
Pseudo.minFlag = 1
Pseudo.min = -100
Pseudo.maxFlag = 1
Pseudo.max = 100
Pseudo.smoothingLevel = 1 #(0, NONE); (1, Fast); (2, High)
Pseudo.legendFlag = 0
SetPlotOptions(Pseudo)

plots = [0]

AddPlot("Mesh", "mesh")
m = MeshAttributes()
m.foregroundFlag = 0
m.legendFlag = 0
m.smoothingLevel = m.Fast
SetPlotOptions(m)

plots += [1]

SetActivePlots(tuple(plots))

AddOperator("Resample")
rAtts = ResampleAttributes()
rAtts.is3D = 0
rAtts.samplesX = 200
rAtts.samplesY = 200
SetOperatorOptions(rAtts)

AddOperator("Elevate")
elevAtts = ElevateAttributes()
elevAtts.variable = "GW-FIELD"
elevAtts.useXYLimits = elevAtts.Never
SetOperatorOptions(elevAtts)

AddOperator("Cylinder")
CylinderAtts = CylinderAttributes()
CylinderAtts.point1 = (0, 0, 10000)
CylinderAtts.point2 = (0, 0, -10000)
CylinderAtts.radius = wave_zone_r
CylinderAtts.inverse = 1
SetOperatorOptions(CylinderAtts)


SetActivePlots(0)

 
###############################################################################
#set up the view
###############################################################################

myView = GetView3D()

c0 = View3DAttributes()
c0.viewNormal = (0, 1.2, 1)
c0.focus = (15,10,0)
c0.viewUp = (-0.2, -1.2, 1)
c0.viewAngle = 30
c0.parallelScale = 129.904 #200
c0.nearPlane = -698.12
c0.farPlane = 698.12
c0.imagePan = (0, 0)
c0.imageZoom = 3.2 #2.2
c0.perspective = 1
c0.eyeAngle = 2
c0.centerOfRotationSet = 0
c0.centerOfRotation = (7.2533, 7.2533, 0)
c0.axis3DScaleFlag = 0
c0.axis3DScales = (1, 1, 5000)
c0.shear = (0, 0, 1)


c1 = View3DAttributes()
c1.viewNormal = (0, 1, 1)
c1.focus = (0, 15, 0)
c1.viewUp = (0, -1, 1)
c1.viewAngle = 30
c1.parallelScale = 129.904 #200
c1.nearPlane = -698.12
c1.farPlane = 698.12
c1.imagePan = (0, 0)
c1.imageZoom = 1.2 #2.2
c1.perspective = 1
c1.eyeAngle = 2
c1.centerOfRotationSet = 0
c1.centerOfRotation = (7.2533, 7.2533, 0)
c1.axis3DScaleFlag = 0
c1.axis3DScales = (1, 1, 1)
c1.shear = (0, 0, 1)


SetView3D(c0)

print("start to draw the default plots")
time.strftime("%Y-%m-%d %H:%M:%S")
print(time.strftime("%Y-%m-%d %H:%M:%S"))

DrawPlots()
#######################################################################
# Setup Annotations 
########################################################################
Ann = AnnotationAttributes()

Ann.backgroundMode = Ann.Solid
Ann.backgroundColor = (50,50,50,255)
Ann.foregroundColor = (255,255,255,255)


#Ann.backgroundColor = (55,118,255,255) #stu blue
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

########################################################################
# set up save attributes 
##########################################################################
s = SaveWindowAttributes()
s.format = s.PNG
s.fileName = saveFolder
s.width = 1080
s.height = 960
s.screenCapture = 0
s.family = 1 #TODO set 1 for 3D movie please
s.stereo = 0 #TODO 1 #Setting for 3D movie
s.resConstraint = s.NoConstraint
SetSaveWindowAttributes(s)

#######################################################################
# start the movie
######################################################################

print("start filming")
time.strftime("%Y-%m-%d %H:%M:%S")
print(time.strftime("%Y-%m-%d %H:%M:%S"))

# find the number of frames
if kind == "hcross":
	tot_frames = len(hcrossfiles)

'''	for i in range(len(hcrossfiles)):
		if hcrossfiles[i] >= stoptime:
			tot_frames = i
			break
			'''

if kind == "hplus":
	tot_frames = len(hplusfiles)
'''
        for i in range(len(hplusfiles)):
                if hplusfiles[i] >= stoptime:
                        tot_frames = i
                        break
'''
if tot_frames == 0:
	print("there are no frames to print, make sure you rightly named the files")
	sys.exit()

print("there are " + str(tot_frames) + " frames")


frame_start = int(round((float(rank)/total_ranks)*tot_frames))
frame_end = int(round(((rank+1.0)/total_ranks)*tot_frames))

for i in range(frame_start,frame_end):
	if kind == "hcross":
		tcur = int(hcrossfiles[i])
		#tcur = int(round(hcrossfiles[i]*float(2.4285714286)/float(4.4288)))
	elif kind == "hplus":
		tcur = int(hplusfiles[i])
		#tcur = int(round(hplusfiles[i] *float(2.4285714286)/float(4.4288)))
	print("time = %g" % int(tcur))
	#print("frame = " + str(tindex))
	txt.text = "t/M = %g" % int(tcur)

	SetTimeSliderState(i)
	print(SetView3D(c0))
	print(GetView3D())
	DrawPlots()
	print(SetView3D(c0))
	print(GetView3D())

	#s.fileName = saveFolder+str(tcur)   #TODO comment out the line for 3D movies
	#SetSaveWindowAttributes(s)          #TODO comment out the line for 3D movies
 
	SaveWindow()

sys.exit()
