import sys
sys.path.append("/u/sciteam/skhan/scratch/NSNS2/nsns_extras/bw_many_folder_scripts/misc_codes")
import RotationMatrix as RM
import random
import csv
import sys
from os import listdir
from os.path import isfile, join
import math
import shutil
import time
from fnmatch import fnmatch

###############################################################################
#load in information about folders etc.
###############################################################################
####Rankstuff
print sys.argv
rank = 0
total_ranks = 100
root_dir = "/u/sciteam/skhan/scratch/NSNS3/"
saveDir = root_dir + "nsns_extras/bw_many_folder_scripts/misc_codes/movies/"
h5_folder = "3d_data_201512300658/"
idx = 4
tot_frames = 100 
frame_start = int(round((float(rank)/total_ranks)*tot_frames))
frame_end = int(round(((rank+1.0)/total_ranks)*tot_frames))

print "rank = " + str(rank)
print "total rank = " + str(total_ranks)

##############################################################

h5dir = root_dir + '3d_data_singletime/'
extrasDir = root_dir + 'nsns_extras/xml/' + h5_folder
saveFolder = saveDir + "zoom_" + str(rank).zfill(3) + "_"
vectorXML = "/u/sciteam/skhan/scratch/NSNS3/nsns_extras/bw_many_folder_scripts/misc_codes/vel.xml"
boxXML = "/u/sciteam/skhan/scratch/NSNS3/nsns_extras/bw_many_folder_scripts/misc_codes/box.xml"

#The first line picks out the files that contain "volume_" in the directory, extrasDir
#The sorting should sort in numerical order

volumeXML = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("volume_")  != -1 ]
volumeXML.sort()

print "volumeXML",volumeXML

particlesXML = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("particles_") != -1 ]
particlesXML.sort()

viewXML = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("view_") != -1 ]
viewXML.sort()

timeTXT = [ f for f in listdir(extrasDir) if isfile(join(extrasDir,f)) and f.find("time_") != -1 ]
timeTXT.sort()

if len(set([len(volumeXML),len(particlesXML),len(viewXML)])) <= 1:
    print "\n\nnumber of xml files are the same"
    print "computer happy :)"
    print ";)\n\n"
else:
    print "Number of xml files is not the same"
    print "Computer sad :("
    print "Computer abort"
    sys.exit()

#make a copy of bhXML and turn it into numbers by removing "bh_" and ".xml"
stateList = particlesXML[:]
for i in range(len(stateList)):
    stateList[i] = int(stateList[i][10:-4])

stateList.sort()
print "statList ",stateList


def bh_formed():
        for file in listdir(extrasDir):
            if fnmatch(file, 'bh1_*.3d'):
                return 1
        return 0
print "bh_formed = ", bh_formed()


###############################################################################
#load the databases
###############################################################################
Bxdir = h5dir + "Bx.file_* database"
Bydir = h5dir + "By.file_* database"
Bzdir = h5dir + "Bz.file_* database"
rho_bdir = h5dir + "rho_b.file_* database"
bh1dir = extrasDir + "bh1_*.3d database"
vxdir = h5dir + "vx.file_* database"
vydir = h5dir + "vy.file_* database"
vzdir = h5dir + "vz.file_* database"
smallb2dir = h5dir + "smallb2.file_* database"



print "Loading Bx..."
OpenDatabase(Bxdir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading By..."
OpenDatabase(Bydir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading Bz..."
OpenDatabase(Bzdir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading rho..."
OpenDatabase(rho_bdir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading vx..."
OpenDatabase(vxdir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading vy..."
OpenDatabase(vydir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading vz..."
OpenDatabase(vzdir,0,"CarpetHDF5_2.1")
print "\tDone"

print "Loading smallb2..."
OpenDatabase(smallb2dir,0,"CarpetHDF5_2.1")
print "\tDone"




print "Loading bh's..."
if bh_formed():
        OpenDatabase(bh1dir)
print "\tDone"

DefineScalarExpression("Bx","conn_cmfe(<" + Bxdir + "[0]id:MHD_EVOLVE--Bx>, <Carpet AMR-grid>)")
DefineScalarExpression("By","conn_cmfe(<" + Bydir + "[0]id:MHD_EVOLVE--By>, <Carpet AMR-grid>)")
DefineScalarExpression("Bz","conn_cmfe(<" + Bzdir + "[0]id:MHD_EVOLVE--Bz>, <Carpet AMR-grid>)")
DefineScalarExpression("rho_b","conn_cmfe(<" + rho_bdir + "[0]id:MHD_EVOLVE--rho_b>, <Carpet AMR-grid>)")
DefineScalarExpression("smallb2","conn_cmfe(<" + smallb2dir + "[0]id:MHD_EVOLVE--smallb2>, <Carpet AMR-grid>)")
DefineScalarExpression("vx","conn_cmfe(<" + vxdir + "[0]id:MHD_EVOLVE--vx>, <Carpet AMR-grid>)")
DefineScalarExpression("vy","conn_cmfe(<" + vydir + "[0]id:MHD_EVOLVE--vy>, <Carpet AMR-grid>)")
DefineScalarExpression("vz","conn_cmfe(<" + vzdir + "[0]id:MHD_EVOLVE--vz>, <Carpet AMR-grid>)")

DefineScalarExpression("logrha","log10(<MHD_EVOLVE--rho_b>/0.00043890933920)")
DefineVectorExpression("BVec","{Bx,By,Bz}")
DefineVectorExpression("vVec","{vx,vy,vz}")
DefineScalarExpression("logsmallb2rho","log10(<smallb2>/(2*<rho_b>), -200)")
DefineVectorExpression("less_vel","if(lt(<logsmallb2rho>, -1.5), {0,0,0}, vVec)")

if bh_formed():
        dbs = (Bxdir, Bydir, Bzdir, rho_bdir, bh1dir, vxdir, vydir, vzdir, smallb2dir)
else:
        dbs = (Bxdir, Bydir, Bzdir, rho_bdir, vxdir, vydir, vzdir, smallb2dir)

CreateDatabaseCorrelation("Everything", dbs, 0)

time.strftime("%Y-%m-%d %H:%M:%S")

###############################################################################
#load the plots
###############################################################################
###############################################################################
DeleteAllPlots()

ref = ReflectAttributes()
ref.reflections = (1,0,0,0,1,0,0,0)

#add Density Volume Plot (0)################
ActivateDatabase(rho_bdir)
AddPlot("Volume","logrha")     #plot 0

vol = VolumeAttributes()
SetActivePlots(0)

AddOperator("Reflect")
SetOperatorOptions(ref)

#add Streamline Plot (1)####################
ActivateDatabase(Bxdir)
AddPlot("Streamline","BVec")    #plot 1

SetActivePlots(1)

AddOperator("Reflect")
SetOperatorOptions(ref)

stream_particles = StreamlineAttributes()

#add Vector Plot (2)####################
ActivateDatabase(vxdir)
AddPlot("Vector","less_vel")    #plot 2

SetActivePlots(2)

AddOperator("Reflect")
SetOperatorOptions(ref)

AddOperator("Cylinder")
CylinderAtts = CylinderAttributes()
CylinderAtts.point1 = (-24.8867766360882, -17.7558616923002, -300)
CylinderAtts.point2 = (-24.8867766360882, -17.7558616923002, 300)
CylinderAtts.radius = 150
CylinderAtts.inverse = 0
SetOperatorOptions(CylinderAtts)

vector_atts = VectorAttributes()


#add bhplots (3) ########################
if bh_formed():
        ActivateDatabase(bh1dir)
        AddPlot("Pseudocolor","bh1p")

        Pseudo = PseudocolorAttributes()
        SetActivePlots(3)
        AddOperator("Delaunay")
        AddOperator("Reflect")
        SetOperatorOptions(ref)

        Pseudo.colorTableName = "gray"
        Pseudo.legendFlag = 0
        Pseudo.lightingFlag = 0

        SetPlotOptions(Pseudo)

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

print "Annotations set up"
# Clock
txt = CreateAnnotationObject("Text2D")
txt.position = (0.75, 0.95) # (x,y), where x and y range from 0 to 1
txt.useForegroundForTextColor = 0
txt.textColor = (255, 255, 255, 255)
txt.fontBold = 1
txt.fontFamily = txt.Times # Because I think Times looks cooler

###############################################################################
#save window settings
###############################################################################

s = SaveWindowAttributes()
s.fileName = saveFolder
s.format = s.PNG
s.width = 1920
s.height = 1080
s.screenCapture = 0
s.stereo = 0 #Setting for 3D movie
s.resConstraint = s.NoConstraint
SetSaveWindowAttributes(s)

myView = GetView3D()


#zoomed out view
c0 = View3DAttributes()
c0.viewNormal = (-0.371116, -0.888564, 0.269678)
c0.focus = (-0.072176, 0.1177, 0)
c0.viewUp = (0, 0, 1)
c0.viewAngle = 30
c0.parallelScale = 1800.73
c0.nearPlane = -3601.45
c0.farPlane = 3601.45
c0.imagePan = (0, 0)
c0.imageZoom = 30
c0.perspective = 1
c0.eyeAngle = 2
c0.centerOfRotationSet = 0
c0.centerOfRotation = (1.16217, 1.16217, 0)
c0.axis3DScaleFlag = 0
c0.axis3DScales = (1, 1, 1)
c0.shear = (0, 0, 1)

#zoomed in view
c1 = View3DAttributes()
c1.viewNormal = (0, 0, 1)
c1.focus = (-0.072176, 0.1177, 0)
c1.viewUp = (0, 1, 0)
c1.viewAngle = 30
c1.parallelScale = 1800.73
c1.nearPlane = -3601.45
c1.farPlane = 3601.45
c1.imagePan = (0, 0)
c1.imageZoom = 50
c1.perspective = 1
c1.eyeAngle = 2
c1.centerOfRotationSet = 0
c1.centerOfRotation = (1.16217, 1.16217, 0)
c1.axis3DScaleFlag = 0
c1.axis3DScales = (1, 1, 1)
c1.shear = (0, 0, 1)

#zoomed out out view
c2 = View3DAttributes()
c2.viewNormal = (-0.371116, -0.888564, 0.269678)
c2.focus = (-24.8867766360882, -17.7558616923002, 0)
c2.viewUp = (0, 0, 1)
c2.viewAngle = 30
c2.parallelScale = 1800.73
c2.nearPlane = -3601.45
c2.farPlane = 3601.45
c2.imagePan = (0, 0)
c2.imageZoom = 6.7
c2.perspective = 1
c2.eyeAngle = 2
c2.centerOfRotationSet = 0
c2.centerOfRotation = (1.16217, 1.16217, 0)
c2.axis3DScaleFlag = 0
c2.axis3DScales = (1, 1, 1)
c2.shear = (0, 0, 1)

#GW view
c3 = View3DAttributes()
c3.viewNormal = (0, 0, 1)
c3.focus = (0, 0, 0)
c3.viewUp = (0, 1, 0)
c3.viewAngle = 30
c3.parallelScale = 1800.73
c3.nearPlane = -3601.45
c3.farPlane = 3601.45
c3.imagePan = (0, 0)
c3.imageZoom = 2.2
c3.perspective = 1
c3.eyeAngle = 2
c3.centerOfRotationSet = 0
c3.centerOfRotation = (7.2533, 7.2533, 0)
c3.axis3DScaleFlag = 0
c3.axis3DScales = (1, 1, 1)
c3.shear = (0, 0, 1)

###############################################################################
#start the movie
###############################################################################

print "starting filming"
time.strftime("%Y-%m-%d %H:%M:%S")

#for state in stateList:
state = stateList[idx]

tcur = timeTXT[state][5:-4]
print "t/M = %g" % int(tcur)
txt.text = "t/M = %g" % int(tcur)

print SetTimeSliderState(state)

print LoadAttribute(extrasDir + volumeXML[state], vol), LoadAttribute(extrasDir + particlesXML[state], stream_particles)
print LoadAttribute(vectorXML, vector_atts)

######implement loaded plot settings

print "setting settings"

print SetActivePlots(0), SetPlotOptions(vol)
print SetActivePlots(1), SetPlotOptions(stream_particles)
print SetActivePlots(2), SetPlotOptions(vector_atts)

def rotate(view, nsteps, frame_start, frame_end):
	print "in rotate"
	ctrig = view

	print "frame start: " + str(frame_start) + "frame_end: " + str(frame_end)
	for i in range(frame_start, frame_end,1):
		phi = 2*math.pi*i/(nsteps - 1)

		ctrig.viewNormal, ctrig.viewUp = RM.circle(view.viewNormal, view.viewUp, phi, 0, 0)

		SetView3D(ctrig)
		DrawPlots()
		SaveWindow()
	
print "rotating"
#rotate(c2,tot_frames, frame_start, frame_end)


