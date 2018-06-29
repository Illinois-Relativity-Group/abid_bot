#Created by Taylor Brian
#Modified by Lingyi Kong
#This is for q10nc-lr on BW
#Dec 8, 2013

import random
import csv
from os import listdir
from os.path import isfile, join
from time import gmtime, strftime, ctime
import sys

####arguments stuff

print "running script in " + sys.argv[3]
print "running iteration number " + sys.argv[4] + " of " + sys.argv[5]

t1 = ctime()

rank = int(sys.argv[4])
total_ranks = int(sys.argv[5])
savefile = sys.argv[6]

plot_tuple = (0,1,2,3,4)

#Global Variables##########################################

father_dir = "/u/sciteam/akim/scratch/q10nc-lr_merged" #TODO
#father_dir = "/media/4317f8ee-75fd-4b7c-ac9f-312226af76a7/bhbh+disk"

h5dir = father_dir+"/"  #TODO
bhdir = father_dir + "/bhdata/" #TODO

particleseedpath = father_dir + "/seed/"
bhseedpath = father_dir + "/bhseeds/"

savefile = father_dir + "/mov_q10nc_3d_1080_021614/alpha_" + str(rank).zfill(4) + "_"

#Movie zooming scheme TODO

zoomsteps = 100

beginzoom1 = 930
beginzoom2 = 1230
#addgridstep = 287 #timestates that add grid points streamlines

tot_frames = 1449 + zoomsteps#total number of frames - be sure to edit this when code is changed TODO

frame_start = int(round((float(rank)/total_ranks)*tot_frames)) 
frame_end = int(round(((rank+1.0)/total_ranks)*tot_frames))

frame_count = frame_start

#Sort##############################################

filelist_part = [ f for f in listdir(particleseedpath) if isfile(join(particleseedpath,f)) and f.find(".txt") > 0 ]
filelist_part.sort()

filelist_bh = [ f for f in listdir(bhseedpath) if isfile(join(bhseedpath,f)) and f.find(".txt") > 0 ]
filelist_bh.sort()

#Save WindowSettings

s = SaveWindowAttributes()
s.format = s.PNG
s.fileName = savefile
s.width = 1280
s.height = 960 
s.screenCapture = 0
s.stereo = 0 # 3D option TODO
s.resConstraint = s.NoConstraint
SetSaveWindowAttributes(s)

#Load Data #############################################

print "Loading Bx..."
OpenDatabase(h5dir + "Bx.h5")
print "\tDone"

print "Loading By..."
OpenDatabase(h5dir + "By.h5")
print "\tDone"

print "Loading Bz..."
OpenDatabase(h5dir + "Bz.h5")
print "\tDone"

print "Loading rho..."
OpenDatabase(h5dir + "rho_b.h5")
print "\tDone"

print "Loading bh's..."
OpenDatabase(bhdir + "bh1_*.vtk database")
OpenDatabase(bhdir + "bh2_*.vtk database")
print "\tDone"


print "Activating Database..."
ActivateDatabase(h5dir + "rho_b.h5")
print "\tDone"

print "Defining expressions..."
DefineScalarExpression("Bx","conn_cmfe(<" + h5dir + "Bx.h5[0]id:MHD_EVOLVE--Bx>, <Carpet AMR-grid>)")
DefineScalarExpression("By","conn_cmfe(<" + h5dir + "By.h5[0]id:MHD_EVOLVE--By>, <Carpet AMR-grid>)")
DefineScalarExpression("Bz","conn_cmfe(<" + h5dir + "Bz.h5[0]id:MHD_EVOLVE--Bz>, <Carpet AMR-grid>)")
DefineScalarExpression("rho_b","conn_cmfe(<" + h5dir + "rho_b.h5[0]id:MHD_EVOLVE--rho_b>, <Carpet AMR-grid>)")
DefineScalarExpression("log_rho","log(rho_b)")
DefineVectorExpression("BVec","{Bx,By,Bz}")

dbs = (h5dir + "Bx.h5", h5dir + "By.h5", h5dir + "Bz.h5", h5dir + "rho_b.h5", bhdir + "bh1_*.vtk database", bhdir + "bh2_*.vtk database")

ActivateDatabase(h5dir + "Bx.h5")
CreateDatabaseCorrelation("Everything", dbs, 0)

DeleteAllPlots()

#add bhplots (0,1) ##########################################
ActivateDatabase(bhdir + "bh1_*.vtk database")
AddPlot("Pseudocolor","black_hole_1")

ActivateDatabase(bhdir + "bh2_*.vtk database")
AddPlot("Pseudocolor","black_hole_2")

Pseudo = PseudocolorAttributes()
SetActivePlots(0)
AddOperator("Delaunay")

Pseudo.colorTableName = "gray"
Pseudo.legendFlag = 0
Pseudo.lightingFlag = 0

SetPlotOptions(Pseudo)

SetActivePlots(1)
AddOperator("Delaunay")

Pseudo.colorTableName = "gray"
Pseudo.legendFlag = 0
Pseudo.lightingFlag = 0

SetPlotOptions(Pseudo)

#add Density Volume Plot (2)##########################################
ActivateDatabase(h5dir + "rho_b.h5")
AddPlot("Volume","log_rho")     #plot 2

vol = VolumeAttributes()
SetActivePlots(2)

AddOperator("Reflect")
ref = ReflectAttributes()
ref.reflections = (1,0,0,0,1,0,0,0)
SetOperatorOptions(ref)

vol.rendererType = vol.RayCasting
vol.lightingFlag = 0
vol.opacityAttenuation = 1.0 #TODO
vol.resampleTarget = 100000
vol.legendFlag = 0
vol.useColorVarMin = 1
vol.colorVarMin = -8.5
vol.useColorVarMax = 1
vol.colorVarMax = -4.5


vol.samplesPerRay = 2000 #TODO

#vol.freeformOpacity =(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 8, 16, 32, 32, 64, 64, 64, 32, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 8, 16, 32, 32, 64, 32, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

vol.freeformOpacity = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 4, 4, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255)


for i in range (2):
        vol.colorControlPoints.GetControlPoints(i).colors = (255,255,255,255)
        vol.colorControlPoints.GetControlPoints(i).position = 0
vol.colorControlPoints.GetControlPoints(2).colors = (255,255,0,255)
vol.colorControlPoints.GetControlPoints(2).position = 0.499999
vol.colorControlPoints.GetControlPoints(3).colors = (255,255,0,255)
vol.colorControlPoints.GetControlPoints(3).position = 0.500001
vol.colorControlPoints.GetControlPoints(4).colors = (255,0,0,255)
vol.colorControlPoints.GetControlPoints(4).position = 1

SetPlotOptions(vol)
print "volume set up"

#add Streamline Plot (3)##########################################
ActivateDatabase(h5dir + "Bx.h5")
AddPlot("Streamline","BVec")	#plot 3

SetActivePlots(3)

AddOperator("Reflect")
SetOperatorOptions(ref)

stream_part = StreamlineAttributes()
stream_part.streamlineDirection = stream_part.Both
stream_part.sourceType = stream_part.SpecifiedPointList
stream_part.coloringMethod = stream_part.Solid
stream_part.showSeeds = 0
stream_part.integrationType = stream_part.DormandPrince
#stream_part.integrationType = stream_part.RK4
stream_part.maxStepLength = 300
stream_part.issueTerminationWarnings = 0
stream_part.issueStiffnessWarnings = 0
stream_part.issueCriticalPointsWarnings = 0
stream_part.singleColor = (255,255,255,255)
stream_part.forceNodeCenteredData = 1
stream_part.legendFlag = 0
stream_part.relTol = 1e-10
stream_part.absTolBBox = 1e-10
stream_part.maxSteps = 100000
stream_part.terminateByDistance = 1
stream_part.termDistance = 3000
SetPlotOptions(stream_part)

print "Streamline 1 Set up"

#add Streamline Plot (4)##########################################
ActivateDatabase(h5dir + "Bx.h5")
AddPlot("Streamline","BVec")	#plot 4

SetActivePlots(4)

AddOperator("Reflect")
SetOperatorOptions(ref)

stream_bh = StreamlineAttributes()
stream_bh.streamlineDirection = stream_bh.Both
stream_bh.sourceType = stream_bh.SpecifiedPointList
stream_bh.coloringMethod = stream_bh.Solid
stream_bh.showSeeds = 0
#stream.integrationType = stream.DormandPrince
stream_bh.integrationType = stream_bh.RK4
stream_bh.maxStepLength = 300
stream_bh.issueTerminationWarnings = 0
stream_bh.issueStiffnessWarnings = 0
stream_bh.issueCriticalPointsWarnings = 0
stream_bh.singleColor =  (51, 153, 102, 255)
stream_bh.forceNodeCenteredData = 1
stream_bh.legendFlag = 0
stream_bh.relTol = 1e-10
stream_bh.absTolBBox = 1e-10
stream_bh.maxSteps = 50000
SetPlotOptions(stream_bh)

print "Streamline 2 Set up"

#Annotations and View ##########################################

Ann = AnnotationAttributes()

Ann.backgroundMode = Ann.Solid
Ann.backgroundColor = (51,102,255,255) #stu blue

#Ann.legendFlag = 0
Ann.databaseInfoFlag = 0
Ann.userInfoFlag = 0

Ann.axes3D.visible = 0
Ann.axes3D.triadFlag = 0
Ann.axes3D.bboxFlag = 0

SetAnnotationAttributes(Ann)

print "Annotations set up"

#Draw Plots and set up view ##########################################
DrawPlots()

c0 = View3DAttributes()
c0.viewNormal = (0.626095, 0.641987, 0.442558)
c0.focus = (1.5188, 1.5188, 0)
c0.viewUp = (-0.32193, -0.304111, 0.896592)
c0.viewAngle = 30
c0.parallelScale = 371.894
c0.nearPlane = -743.789
c0.farPlane = 743.789
c0.imagePan = (-0.000509062, 0.000332394)
c0.imageZoom = 3.13843
c0.perspective = 1
c0.eyeAngle = 2
c0.centerOfRotationSet = 0
c0.centerOfRotation = (0, 0, 0)
c0.axis3DScaleFlag = 0
c0.axis3DScales = (1, 1, 1)
c0.shear = (0, 0, 1)

#c1 = View3DAttributes()
#c1.viewNormal = (0.455117, 0.432552, 0.778311)
#c1.focus = (1.5188, 1.5188, 0)
#c1.viewUp = (-0.56556, -0.534707, 0.627878)
#c1.viewAngle = 30
#c1.parallelScale = 371.894
#c1.nearPlane = -743.789
#c1.farPlane = 743.789
#c1.imagePan = (-0.000509062, 0.000332394)
#c1.imageZoom = 11.9182
#c1.perspective = 1
#c1.eyeAngle = 2
#c1.centerOfRotationSet = 0
#c1.centerOfRotation = (0, 0, 0)
#c1.axis3DScaleFlag = 0
#c1.axis3DScales = (1, 1, 1)
#c1.shear = (0, 0, 1)

c1 = View3DAttributes()
c1.viewNormal = (0.244506, 0.1776, 0.953244)
c1.focus = (1.5188, 1.5188, 0)
c1.viewUp = (-0.697229, -0.650996, 0.300126)
c1.viewAngle = 30
c1.parallelScale = 371.894
c1.nearPlane = -743.789
c1.farPlane = 743.789
c1.imagePan = (-0.000509062, 0.000332394)
c1.imageZoom = 11.9182
c1.perspective = 1
c1.eyeAngle = 2
c1.centerOfRotationSet = 0
c1.centerOfRotation = (0, 0, 0)
c1.axis3DScaleFlag = 0
c1.axis3DScales = (1, 1, 1)
c1.shear = (0, 0, 1)

#c_close = View3DAttributes()
#c_close.viewNormal = (-0.0517597, 0.065386, 0.996517)
#c_close.focus = (1.5188, 1.5188, 0)
#c_close.viewUp = (-0.694883, -0.719037, 0.0110866)
#c_close.viewAngle = 30
#c_close.parallelScale = 371.894
#c_close.nearPlane = -743.789
#c_close.farPlane = 743.789
#c_close.imagePan = (-0.00012702, -0.00254361)
#c_close.imageZoom = 30.9127
#c_close.perspective = 1
#c_close.eyeAngle = 2
#c_close.centerOfRotationSet = 0
#c_close.centerOfRotation = (0, 0, 0)
#c_close.axis3DScaleFlag = 0
#c_close.axis3DScales = (1, 1, 1)
#c_close.shear = (0, 0, 1)

c_close = View3DAttributes()
c_close.viewNormal = (-0.0517597, 0.065386, 0.996517)
c_close.focus = (1.5188, 1.5188, 0)
c_close.viewUp = (-0.694883, -0.719037, 0.0110866)
c_close.viewAngle = 30
c_close.parallelScale = 371.894
c_close.nearPlane = -743.789
c_close.farPlane = 743.789
c_close.imagePan = (-0.00301987, -0.00603135)
c_close.imageZoom = 80.1796
c_close.perspective = 1
c_close.eyeAngle = 2
c_close.centerOfRotationSet = 0
c_close.centerOfRotation = (0, 0, 0)
c_close.axis3DScaleFlag = 0
c_close.axis3DScales = (1, 1, 1)
c_close.shear = (0, 0, 1)


def updateStreamline_part(indexstep):
	SetActivePlots(3)
	file1 = open(particleseedpath + filelist_part[indexstep],'r')
	print "opening " + filelist_part[indexstep]
	data1 = csv.reader(file1,delimiter='\t')
	table1 = [row for row in data1]
	d1 = []
	for i in range(len(table1)):
		for j in range(len(table1[i])):
			d1.append(table1[i][j])
	d1 = map(float,d1)

	mytuple1 = tuple(d1)
	stream_part.pointList = mytuple1
	SetPlotOptions(stream_part)

def updateStreamline_bh(indexstep):
	SetActivePlots(4)
	file1 = open(bhseedpath + filelist_bh[indexstep],'r')
	print "opening " + filelist_bh[indexstep]
	data1 = csv.reader(file1,delimiter='\t')
	table1 = [row for row in data1]
	d1 = []
	for i in range(len(table1)):
		for j in range(len(table1[i])):
			d1.append(table1[i][j])
	d1 = map(float,d1)

	mytuple1 = tuple(d1)
	stream_bh.pointList = mytuple1
	SetPlotOptions(stream_bh)

def run_mov_fixed_view(first_step,last_step,view):

	print "called run_mov_fixed_view"

	global frame_count

	#if(frame_start > (last_step+zoomsteps)):
	#	print "1"
	#	return
	#if(frame_end < (first_step+zoomsteps)):
	#	print "2"
	#	return

	#for state in range(first_step,last_step,1):
        for frame in range(frame_count,min(frame_end,last_step),1):
		state = frame

		SetActivePlots(plot_tuple)

		SetTimeSliderState(state)

		updateStreamline_part(state)
		updateStreamline_bh(state)

		SetActivePlots(plot_tuple)

		SetView3D(view)

		n = SaveWindow()
		frame_count = frame_count + 1
	
                if(frame_count > frame_end):
                        print "calling return"
                        return
        print "return not called"

	
def run_mov_change_view(first_step,last_step,view_initial,view_final):

	print "called run_mov_change_view"

        global frame_count

	#if(frame_start > (last_step+zoomsteps)):
        #        print "1"
	#	return
        #if(frame_end < (first_step+zoomsteps)):
        #        print "2"
	#	return

	cpts=(view_initial,view_final)
	x=[0,1]
	my_i = frame_count - first_step

	#for state in range(first_step,last_step,1):
	for frame in range(frame_count,min(frame_end,last_step),1):
		state = frame

		SetActivePlots(plot_tuple)

		SetTimeSliderState(state)

		updateStreamline_part(state)
		updateStreamline_bh(state)

		SetActivePlots(plot_tuple)
		t = float(my_i) / float(last_step - first_step - 1)
        	c = EvalCubicSpline(t, x, cpts)
        	SetView3D(c)

		n = SaveWindow()
		frame_count = frame_count + 1
		my_i = my_i + 1
		
                if(frame_count > frame_end):
                        print "calling return"
                        return
        print "return not called"


def zoom_at_fixed_time(time_index,view_initial,view_final):

	print "called zoom_at_fixed_time"

        global frame_count

	print "frame_start ", frame_start
	print "zoomsteps", zoomsteps

       # if((frame_start > (zoomsteps))):
        #        iprint "1"
	#	return

	SetTimeSliderState(time_index)

	updateStreamline_part(time_index)
	updateStreamline_bh(time_index)

	cpts=(view_initial,view_final)
	x=[0,1]

	for my_i in range(frame_count,min(frame_end,zoomsteps+time_index),1):

		t = float(my_i) / float(zoomsteps - 1)
        	c = EvalCubicSpline(t, x, cpts)
        	SetView3D(c)

		n = SaveWindow()
		frame_count = frame_count + 1
		
		print "frame_count",frame_count
		print "frame_end",frame_end

		if(frame_count > frame_end):
			print "calling return"
                        return
	print "return not called"	

#hide bh fieldlines
#SetActivePlots(4)
#HideActivePlots()
SetActivePlots(plot_tuple)
zoom_at_fixed_time(0,c_close,c0)

#film without bhfieldlines


#show bh fieldlines
#SetActivePlots(4)
#HideActivePlots()
#SetActivePlots(plot_tuple)

#film with bhfieldlines

run_mov_fixed_view(0,beginzoom1,c0) 
run_mov_change_view(beginzoom1,beginzoom1+zoomsteps,c0,c1)

run_mov_fixed_view(beginzoom1+zoomsteps,beginzoom2,c1)

run_mov_change_view(beginzoom2,beginzoom2+zoomsteps,c1,c0)
run_mov_fixed_view(beginzoom2+zoomsteps,TimeSliderGetNStates(),c0)

print "Started at ", t1

print "Finished at ", ctime()

sys.exit()
