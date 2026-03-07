
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
GWdir = sys.argv[2]
saveFolder = sys.argv[3]
rank = int(sys.argv[4])
total_ranks = int(sys.argv[5])
#stoptime = int(sys.argv[11])
gw_dt = float(sys.argv[6])
ADM_mass = float(sys.argv[7])

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

ref = ReflectAttributes()
ref.reflections = (1,0,0,0,1,0,0,0)
ref.octant = ref.PXPYNZ  # PXPYPZ, NXPYPZ, PXNYPZ, NXNYPZ, PXPYNZ, NXPYNZ, PXNYNZ, NXNYNZ
ref.useXBoundary = 1
ref.specifiedX = 0
ref.useYBoundary = 1
ref.specifiedY = 0
ref.useZBoundary = 1
ref.specifiedZ = 0
ref.reflections = (1, 0, 0, 0, 1, 0, 0, 0)

AddPlot("Volume","modifiedwave")

vol= VolumeAttributes()

#AddOperator("Reflect")
#SetOperatorOptions(ref)

ccp_gw=ColorControlPointList() # Define ColorControlPointList Object
for i in range (8):
        ccp_gw.AddControlPoints(ColorControlPoint())# Add colorControlPoints

ccp_gw.GetControlPoints(0).colors = (0, 0, 255, 255)
ccp_gw.GetControlPoints(0).position = 0
ccp_gw.GetControlPoints(1).colors = (0, 0, 255, 255)
ccp_gw.GetControlPoints(1).position = 0.25   #0.15  #0.25
ccp_gw.GetControlPoints(2).colors = (0, 255, 255, 255)
ccp_gw.GetControlPoints(2).position = 0.375    #0.30   #0.375
ccp_gw.GetControlPoints(3).colors = (0, 255, 255, 255)
ccp_gw.GetControlPoints(3).position = 0.5
ccp_gw.GetControlPoints(4).colors = (255, 255, 0, 255)
ccp_gw.GetControlPoints(4).position = 0.5
ccp_gw.GetControlPoints(5).colors = (255, 255, 0, 255)
ccp_gw.GetControlPoints(5).position = 0.625   #0.7    #0.625
ccp_gw.GetControlPoints(6).colors = (0, 255, 0, 255)
ccp_gw.GetControlPoints(6).position = 0.75  #0.85   #0.75
ccp_gw.GetControlPoints(7).colors = (0, 255, 0, 255)
ccp_gw.GetControlPoints(7).position = 1

vol.colorControlPoints=ccp_gw # Set colorcontrolpoints for volumeattributes object


#vol_gw= VolumeAttributes()
vol.legendFlag = 0 #1
vol.lightingFlag = 0

vol.opacityAttenuation = 0.12  #0.07

vol.opacityMode = 0 # FreeformMode, GaussianMode, ColorTableMode
vol.opacityVariable = "default"
vol.compactVariable = "default"

#vol.freeformOpacity = (202, 203, 203, 204, 204, 204, 205, 206, 206, 206, 207, 207, 208, 208, 209, 209, 210, 210, 211, 211, 211, 212, 212, 212, 212, 213, 213, 214, 214, 214, 215, 215, 215, 215, 216, 216, 216, 217, 217, 217, 217, 218, 218, 218, 218, 219, 219, 219, 219, 220, 220, 220, 220, 220, 220, 221, 221, 221, 221, 221, 221, 221, 221, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 206, 180, 140, 125, 83, 50, 30, 26, 9, 0, 0, 0, 0, 0, 0, 0, 24, 87, 120, 173, 140, 100, 80, 50, 5, 0, 0, 0, 0, 0, 0, 0, 3, 25, 34, 61, 103, 93, 47, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 47, 93, 103, 61, 34, 25, 3, 0, 0, 0, 0, 0, 0, 0, 5, 50, 80, 100, 140, 173, 120, 87, 24, 0, 0, 0, 0, 0, 0, 0, 9, 26, 30, 50, 83, 125, 140, 180, 206, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 221, 221, 221, 221, 221, 221, 221, 221, 220, 220, 220, 220, 220, 220, 219, 219, 219, 219, 218, 218, 218, 218, 217, 217, 217, 217, 216, 216, 216, 215, 215, 215, 215, 214, 214, 214, 213, 213, 212, 212, 212, 212, 211, 211, 211, 210, 210, 209, 209, 208, 208, 207, 207, 206, 206, 206, 205, 204, 204, 204, 203, 203, 202)
 #with 18 as the maximum value, hard cut at 0.85, and the drop starts at 6.5 


vol.freeformOpacity = (202, 203, 203, 204, 204, 204, 205, 205, 206, 206, 206, 207, 207, 207, 208, 208, 209, 209, 209, 210, 210, 210, 211, 211, 211, 212, 212, 212, 212, 213, 213, 213, 214, 214, 214, 215, 215, 215, 215, 216, 216, 216, 216, 217, 217, 217, 217, 217, 218, 218, 218, 218, 218, 219, 219, 219, 219, 219, 220, 220, 220, 220, 220, 220, 220, 221, 221, 221, 221, 221, 221, 221, 221, 221, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 206, 170, 125, 83, 50, 26, 9, 0, 0, 0, 0, 0, 24, 87, 173, 140, 100, 50, 5, 0, 0, 0, 0, 0, 0, 0, 45, 65, 143, 65, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 65, 143, 65, 45, 0, 0, 0, 0, 0, 0, 0, 5, 50, 100, 140, 173, 87, 24, 0, 0, 0, 0, 0, 9, 26, 50, 83, 125, 170, 206, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 221, 221, 221, 221, 221, 221, 221, 221, 221, 220, 220, 220, 220, 220, 220, 220, 219, 219, 219, 219, 219, 218, 218, 218, 218, 218, 217, 217, 217, 217, 217, 216, 216, 216, 216, 215, 215, 215, 215, 214, 214, 214, 213, 213, 213, 212, 212, 212, 212, 211, 211, 211, 210, 210, 210, 209, 209, 209, 208, 208, 207, 207, 207, 206, 206, 206, 205, 205, 204, 204, 204, 203, 203, 202)
# with 24 as the maximum value, hard cut at 0.75, and the drop starts at 9  #TODO this may be a good one

#vol.freeformOpacity = (203, 203, 204, 204, 204, 205, 205, 205, 206, 206, 206, 207, 207, 207, 208, 208, 209, 209, 209, 210, 210, 210, 211, 211, 211, 212, 212, 212, 212, 212, 213, 213, 213, 214, 214, 214, 214, 215, 215, 215, 215, 215, 216, 216, 216, 216, 216, 217, 217, 217, 218, 218, 218, 219, 219, 219, 219, 219, 220, 220, 220, 220, 220, 220, 220, 221, 221, 221, 221, 221, 221, 221, 221, 222, 222, 222, 222, 222, 222, 222, 222, 221, 220, 210, 200, 190 , 180, 170, 160, 150, 140, 130, 120, 90, 80, 70, 60, 40, 20, 0, 0, 0, 0, 0, 40, 90, 113, 153, 186, 186, 153, 123, 80, 29, 0, 0, 0, 0, 29, 70, 96, 45, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 45, 96, 70, 29, 0, 0, 0, 0, 29, 80, 123, 153, 186, 186, 153, 113, 90, 40, 0, 0, 0, 0, 0, 20, 40, 60, 70, 80, 90, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 221, 222, 222, 222, 222, 222, 222, 222, 222, 221, 221, 221, 221, 221, 221, 221, 221, 220, 220, 220, 220, 220, 220, 220, 219, 219, 219, 219, 219, 218, 218, 218, 217, 217, 217, 216, 216, 216, 216, 216, 215, 215, 215, 215, 215, 214, 214, 214, 214, 213, 213, 213, 212, 212, 212, 212, 212, 211, 211, 211, 210, 210, 210, 209, 209, 209, 208, 208, 207, 207, 207, 206, 206, 206, 205, 205, 205, 204, 204, 204, 203, 203)    
# new test with max =40; drop at 15-18, second peak at 6 , first peak at 2;  below 1, the opacity is 0 


#vol.freeformOpacity = (202, 203, 203, 204, 204, 204, 205, 205, 206, 206, 206, 207, 207, 207, 208, 208, 209, 209, 209, 210, 210, 210, 211, 211, 211, 212, 212, 212, 212, 213, 213, 213, 214, 214, 214, 215, 215, 215, 215, 216, 216, 216, 216, 217, 217, 217, 217, 217, 218, 218, 218, 218, 218, 219, 219, 219, 219, 219, 220, 220, 220, 220, 220, 220, 220, 221, 221, 221, 221, 221, 221, 221, 221, 221, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 206, 170, 125, 83, 50, 26, 9, 0, 0, 0, 0, 19, 87, 163, 126, 40, 5, 0, 0, 0, 0, 0, 0, 0, 3, 25, 76, 93, 47, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 67, 93, 38, 4, 0, 0, 0, 0, 0, 0, 0, 0, 6, 59, 158, 123, 27, 0, 0, 0, 0, 9, 26, 50, 83, 125, 170, 206, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 222, 221, 221, 221, 221, 221, 221, 221, 221, 221, 220, 220, 220, 220, 220, 220, 220, 219, 219, 219, 219, 219, 218, 218, 218, 218, 218, 217, 217, 217, 217, 217, 216, 216, 216, 216, 215, 215, 215, 215, 214, 214, 214, 213, 213, 213, 212, 212, 212, 212, 211, 211, 211, 210, 210, 210, 209, 209, 209, 208, 208, 207, 207, 207, 206, 206, 206, 205, 205, 204, 204, 204, 203, 203, 20) # Abid color bar
vol.useColorVarMin = 1
vol.colorVarMin = -0.0046 #-0.005055 #-0.00001875
vol.useColorVarMax = 1
vol.colorVarMax = 0.0046 #0.005055 #0.00001875
vol.samplesPerRay = 350
#vol.rendererType = 2 # Splatting, Texture3D, RayCasting, RayCastingIntegration, SLIVR, Tuvok	#different in visit 3.x.x
 
SetPlotOptions(vol)
SetActivePlots(0)

 
###############################################################################
#set up the view
###############################################################################

myView = GetView3D()

c0 = View3DAttributes()
c0.viewNormal = (0, 0, 1)
c0.focus = (0, 0, 0)
c0.viewUp = (0, 1, 0)
c0.viewAngle = 30
c0.parallelScale = 120 #200
c0.nearPlane = -698.12
c0.farPlane = 698.12
c0.imagePan = (0, 0)
c0.imageZoom = 2.5 #2.2
c0.perspective = 1
c0.eyeAngle = 2
c0.centerOfRotationSet = 0
c0.centerOfRotation = (7.2533, 7.2533, 0)
c0.axis3DScaleFlag = 0
c0.axis3DScales = (1, 1, 1)
c0.shear = (0, 0, 1)

c1 = View3DAttributes()
c1.viewNormal = (-0.371116, -0.888564, 0.269678) 
c1.focus = (-0.072176, 0.1177, 0)
c1.viewUp = (0, 0, 1) 
c1.viewAngle = 30
c1.parallelScale = 1800.73
c1.nearPlane = -3601.45
c1.farPlane = 3601.45
c1.imagePan = (0, 0)
c1.imageZoom =15 #5 #40
c1.perspective = 1
c1.eyeAngle = 2
c1.centerOfRotationSet = 0
c1.centerOfRotation = (1.16217, 1.16217, 0)
c1.axis3DScaleFlag = 0
c1.axis3DScales = (1, 1, 1)
c1.shear = (0, 0, 1)

c2 = View3DAttributes()
c2.viewNormal = (0, -0.945035, 0.326932)
c2focus = (-0.5, -0.5, -8)
c2.viewUp = (0, 0.326967, 0.944963)
c2.viewAngle = 30
c2.parallelScale = 200
c2.nearPlane = -400
c2.farPlane = 400
c2.imagePan = (0, 0)
c2.imageZoom = 3.8
c2.perspective = 1
c2.eyeAngle = 2
c2.centerOfRotationSet = 0
c2.centerOfRotation = (-0.5, -0.5, -1)
c2.axis3DScaleFlag = 0
c2.axis3DScales = (1, 1, 1)
c2.shear = (0, 0, 1)

c3 = View3DAttributes()
c3.viewNormal = (0, -0.986, 0.1)
c3.focus = (-0.5, -0.5, -25)
c3.viewUp = (0, 0.1, 0.986)
c3.viewAngle = 30
c3.parallelScale = 128.75
c3.nearPlane = -257.5
c3.farPlane = 257.5
c3.imagePan = (0, 0)
c3.imageZoom = 5
c3.perspective = 1
c3.eyeAngle = 2.2
c3.centerOfRotationSet = 0
c3.centerOfRotation = (-0.5, -0.5, -1)
c3.axis3DScaleFlag = 0
c3.axis3DScales = (1, 1, 1)
c3.shear = (0, 0, 1)

c4 = View3DAttributes()
c4.viewNormal = (0, -0.98, 0.15)
c4.focus = (-0.5, -0.5, -80)
c4.viewUp = (0, 0.15, 0.98)
c4.viewAngle = 30
c4.parallelScale = 200
c4.nearPlane = -698.12
c4.farPlane = 698.12
c4.imagePan = (0, 0)
c4.imageZoom = 4.8
c4.perspective = 1
c4.eyeAngle = 2
c4.centerOfRotationSet = 0
c4.centerOfRotation = (-0.5, -0.5, -1)
c4.axis3DScaleFlag = 0
c4.axis3DScales = (1, 1, 1)
c4.shear = (0, 0, 1)

c5 = View3DAttributes()
c5.viewNormal = (0, -0.986, 0.06)
c5.focus = (-0.5, -0.5, -22)
c5.viewUp = (0, 0.06, 0.986)
c5.viewAngle = 30
c5.parallelScale = 128.75
c5.nearPlane = -257.5
c5.farPlane = 257.5
c5.imagePan = (0, 0)
c5.imageZoom = 5.5
c5.perspective = 1
c5.eyeAngle = 2.2
c5.centerOfRotationSet = 0
c5.centerOfRotation = (-0.5, -0.5, -1)
c5.axis3DScaleFlag = 0
c5.axis3DScales = (1, 1, 1)
c5.shear = (0, 0, 1)


c6 = View3DAttributes()
c6.viewNormal = (0.833427, 0.507226, 0.219365)
c6.focus = (0, 0, 0)
c6.viewUp = (-0.190766, -0.108488, 0.975622)
c6.viewAngle = 30
c6.parallelScale = 100
c6.nearPlane = -698.12
c6.farPlane = 698.12
c6.imagePan = (0, 0.08)
c6.imageZoom = 4
c6.perspective = 1
c6.eyeAngle = 2
c6.centerOfRotationSet = 0
c6.centerOfRotation = (7.2533, 7.2533, 0)
c6.axis3DScaleFlag = 0
c6.axis3DScales = (1, 1, 1)
c6.shear = (0, 0, 1)

#view 1
c7 = View3DAttributes()
c7.viewNormal = (-0.159614, -0.98078, 0.11222)
c7.focus = (-0.5, -0.5, -25)
c7.viewUp = (0.0116261, 0.111802, 0.993662)
c7.viewAngle = 30
c7.parallelScale = 111.667
c7.nearPlane = -223.334
c7.farPlane = 223.334
c7.imagePan = (0, 0)
c7.imageZoom = 3.22102
c7.perspective = 1
c7.eyeAngle = 2
c7.centerOfRotationSet = 0
c7.centerOfRotation = (-0.5, -0.5, -38)
c7.axis3DScaleFlag = 0
c7.axis3DScales = (1, 1, 1)
c7.shear = (0, 0, 1)

#view2
c8 = View3DAttributes()
c8.viewNormal = (-0.178185, -0.983921, 0.0122522)
c8.focus = (-0.5, -0.5, -25)
c8.viewUp = (-0.000627972, 0.0125652, 0.999921)
c8.viewAngle = 30
c8.parallelScale = 111.667
c8.nearPlane = -223.334
c8.farPlane = 223.334
c8.imagePan = (0, 0)
c8.imageZoom = 3.22102
c8.perspective = 1
c8.eyeAngle = 2
c8.centerOfRotationSet = 0
c8.centerOfRotation = (-0.5, -0.5, -38)
c8.axis3DScaleFlag = 0
c8.axis3DScales = (1, 1, 1)
c8.shear = (0, 0, 1)

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
Ann.backgroundColor = (192,192,192,255)
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
