#Run with something like visit -cli -nowin -forceversion 2.7.3 -np 1 -nn 1 -l aprun -s $VISITSCRIPT $H5 $EXTRAS $SUBMITFOLDER $RANK $TOTRANKS $STREAMXML $VECXML $MAXDEN

import random
import csv
import sys
import time
import datetime

from os import listdir, rename
from os.path import isfile, join
from fnmatch import fnmatch
from runModule import *
###############################################################################
#search for all the necessary data (preprocessing)
###############################################################################
start_time = time.time()

PlotDens = 1 # Plot density
PlotVel  = 0 # Plot velocity arrows
PlotBsq2r= 0 # Plot B squared over 2 rho
Plotg00  = 1 # Plot g00 from metric
cutPlot  = 0 #only show back half (y>0), needs view like: (0,-x,y)

print(sys.argv)

h5dir = sys.argv[6]
extrasDir = sys.argv[7] 
saveFolder = sys.argv[8]
rank = int(sys.argv[9])
total_ranks = int(sys.argv[10])
streamXML = sys.argv[11]
vectorXML = sys.argv[12]
bsq2rXML = sys.argv[13]
rho_pseudoXML = sys.argv[14]
rho_threshXML = sys.argv[15]
rho_isoXML = sys.argv[16]
g00_pseudoXML = sys.argv[17]
g00_threshXML = sys.argv[18]
g00_isoXML = sys.argv[19]
max_density = sys.argv[20]
time.strftime("%Y-%m-%d %H:%M:%S")

#append a '/' if necessary
if(h5dir[-1] != '/'): h5dir += '/'
if(extrasDir[-1] != '/'): extrasDir += '/'

#The first line picks out the files that contain "volume_" in the directory, extrasDir
#The sorting should sort in numerical order

volumeXML, particlesTXT, gridPointsTXT, viewXML, timeTXT,\
bh13D, bh23D, bh33D, trace3D, trace23D, stateList = getLists(extrasDir)
print("stateList: {}".format(stateList))
##################################################
#Choose what to plot
def density(): return PlotDens
#
def bsq2r(): return PlotBsq2r and not density() #Can't have 2 volume plots
#
def bh_formed(): return len(bh13D) > 0 
#
def binary_formed(): return len(bh23D) > 0 
#
def merge_formed(): return len(bh33D) > 0 
#
def trace1(): return len(trace3D) > 0
#
def trace2(): return len(trace23D) > 0
#
def particles(): return len(particlesTXT) > 0
#
def gridPoints(): return len(gridPointsTXT) > 0		
#
def fields(): return particles() or gridPoints()
#
def velocity(): return PlotVel
#
def g00(): return Plotg00
#
##################################################

#This adjusts the bh_*.3d files so that the black hole doesn't show up earlier than it's supposed to
#This will use bh3 data to overwrite the empty bh1 and bh2 files whenever bh1 and bh3 appear together in one folder. Probably won't do anything but necessary for BHBH cases
fill_bh(bh_formed(), '1', extrasDir, stateList)
fill_bh(binary_formed(), '2', extrasDir, stateList)
fill_bh(merge_formed(), '3', extrasDir, stateList)

#Checking bh files again ################
bh13D, bh23D, bh33D = recheckBH(extrasDir)

print("density: {}".format(density()))
print("bsq2r: {}".format(bsq2r()))
print("fields: {}".format(fields()))
print("particles: {}".format(particles()))
print("gridPoints: {}".format(gridPoints()))
print("trace1: {}".format(trace1()))
print("trace2: {}".format(trace2()))
print("velocity: {}".format(velocity()))
print("BH1: {}".format(bh_formed()))
print("BH2: {}".format(binary_formed()))
print("BH3: {}".format(merge_formed()))
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
vxdir = h5dir + "vx.file_* database"
vydir = h5dir + "vy.file_* database"
vzdir = h5dir + "vz.file_* database"
smallb2dir = h5dir + "smallb2.file_* database"
shiftxdir = h5dir + "shiftx.file_* database"
shiftydir = h5dir + "shifty.file_* database"
shiftzdir = h5dir + "shiftz.file_* database"
rho_bdir = h5dir + "rho_b.file_* database"
psidir = h5dir + "psi.file_* database"
gxxdir = h5dir + "gxx.file_* database"
gyydir = h5dir + "gyy.file_* database"
gzzdir = h5dir + "gzz.file_* database"
gxydir = h5dir + "gxy.file_* database"
gxzdir = h5dir + "gxz.file_* database"
gyzdir = h5dir + "gyz.file_* database"
lapm1dir = h5dir + "lapm1.file_* database"

if density():
	LoadandDefine(rho_bdir, "rho_b")
	#DefineScalarExpression("logrho","log10(<MHD_EVOLVE--rho_b>/" + max_density + ")")

if bsq2r():
	LoadandDefine(rho_bdir, "rho_b")
	LoadandDefine(smallb2dir, "smallb2")
	DefineScalarExpression("logbsq2r","log10(<MHD_EVOLVE--smallb2>/(2*<rho_b>), -200)")

if fields():
	LoadandDefine(Bxdir, "Bx")
	LoadandDefine(Bydir, "By")
	LoadandDefine(Bzdir, "Bz")
	DefineVectorExpression("BVec","{Bx,By,Bz}")

if bh_formed():
	print("Loading bh1's...")
	OpenDatabase(bh1dir)

if binary_formed():
	print("Loading bh2's...")
	OpenDatabase(bh2dir)

if merge_formed():
	print("Loading bh3's...")
	OpenDatabase(bh3dir)

if trace1():
	print("Loading Particle Tracer...")
	OpenDatabase(trace1dir)

if trace2():
	print("Loading Particle Tracer 2...")
	OpenDatabase(trace2dir)

if velocity():
	LoadandDefine(vxdir, 'vx')
	LoadandDefine(vydir, 'vy')
	LoadandDefine(vzdir, 'vz')
	DefineVectorExpression("vVec_temp","{vx,vy,vz}")
	DefineVectorExpression("vVec","if(gt(magnitude(vVec_temp),0.1),vVec_temp,{0,0,0})")#Remove small arrows
	#DefineVectorExpression("vVec","if(gt(logbsq2r,-1),vVec_temp,{0,0,0})") #Only show arrows around jet, need to load smallb2 database i

if g00():
	print "Loading g00..."
	LoadandDefine2(psidir,"BSSN","psi")
	LoadandDefine2(shiftxdir,"SHIFT","shiftx")
	LoadandDefine2(shiftydir,"SHIFT","shifty")
	LoadandDefine2(shiftzdir,"SHIFT","shiftz")
	LoadandDefine2(gxxdir,"BSSN","gxx")
	LoadandDefine2(gyydir,"BSSN","gyy")
	LoadandDefine2(gzzdir,"BSSN","gzz")
	LoadandDefine2(gxydir,"BSSN","gxy")
	LoadandDefine2(gxzdir,"BSSN","gxz")
	LoadandDefine2(gyzdir,"BSSN","gyz")
	LoadandDefine2(lapm1dir,"LAPSE","lapm1")
	DefineScalarExpression("g00","psi^4*(gxx*shiftx^2+gyy*shifty^2+gzz*shiftz^2+2.0*(gxy*shiftx*shifty+gxz*shiftx*shiftz+gyz*shifty*shiftz))-(lapm1+1)^2")

print("\tDone")

# Put the additional database into dbs list when you add a new database. 
dbs = []
plot_idx = []
###
if density():
	dbs += [rho_bdir];              plot_idx += ["density"]
if bsq2r():
	dbs += [smallb2dir, rho_bdir];  plot_idx += ["bsq2r"]
###
if fields():
	dbs += [Bxdir, Bydir, Bzdir]
if particles():
    plot_idx += ["particles"]
if gridPoints():
    plot_idx += ["gridPoints"]
###
if bh_formed():
	dbs += [bh1dir];                plot_idx += ["bh1"]
if binary_formed():
	dbs += [bh2dir];                plot_idx += ["bh2"]
if merge_formed():
	dbs += [bh3dir];                plot_idx += ["bh3"]
###
if trace1():
	dbs += [trace1dir];             plot_idx += ["trace1"]
if trace2():
	dbs += [trace2dir];             plot_idx += ["trace2"]
###
if velocity():
	dbs += [vxdir, vydir, vzdir];   plot_idx += ["vel"]
###
if g00():
	dbs += [psidir, shiftxdir, shiftydir, shiftzdir, gxxdir, gyydir, gzzdir, gxydir, gxzdir, gyzdir, lapm1dir];							 plot_idx += ["g00"]

print("Databases loaded: {}\n".format(dbs))
print("Plotting: {}".format(plot_idx))

CreateDatabaseCorrelation("Everything", dbs, 0)
time.strftime("%Y-%m-%d %H:%M:%S")
###############################################################################
#load the plots
###############################################################################

# Use plot_idx.index("plot name") to find its idx
def idx(name):
	return plot_idx.index(name)

DeleteAllPlots()

#add Density Volume Plot#################
if density():
	vol = PlotVol(rho_bdir, "rho_b", idx("density"))
	#rho_atts = PlotPseudo(rho_bdir, "rho_b", idx("density"))
#add bsq2r Plot ##################
if bsq2r():
	bsq_atts = PlotVol(smallb2dir, "logbsq2r", idx("bsq2r"))
#add particles-seeded Streamline Plot#####
if particles():
	stream_particles = PlotB(Bxdir, idx("particles"))
#add gridPoints-seeded Streamline Plot####
if gridPoints():
	stream_gridPoints = PlotB(Bxdir, idx("gridPoints"))
#add bhplots##############################
if bh_formed():
	PlotBH(bh1dir, '1', idx("bh1"))

if binary_formed():
	PlotBH(bh2dir, '2', idx("bh2"))

if merge_formed():
	PlotBH(bh3dir, '3', idx("bh3"))

#add particle tracer plots################
if trace1():
	PlotTrace(trace1dir, '1', idx("trace1"))

if trace2():
	PlotTrace(trace2dir, '2', idx("trace2"))

#Add velocity arrows #####################
if velocity():
	vector_atts = PlotVel(vxdir, "vVec", idx("vel"))

#Add g00 plot ###########################
if g00():
	g00_atts = PlotPseudo(psidir, "g00", idx("g00"))

myView = GetView3D()
##########################################
#set up the annotations
#light list contains [(direction), brightness, type=camera]
lightlist = [[(0, 0, -1), 1], [(0, -1, 0), 0.6 ], [(-0.026, 0.978, -0.207), 0.75]]
#lightlist = [[(0, 0, -1), 1], [(0, 0, -1), 0.75, 0 ]]
txt = setAnnotations(lightlist)

#save window settings
setSave(saveFolder)

##########################################
#start the movie                         #
##########################################

print("Starting filming")
time.strftime("%Y-%m-%d %H:%M:%S")

tot_frames = len(stateList)

firstFrame = int(round((float(rank)/total_ranks)*tot_frames))
lastFrame = int(round(((rank+1.0)/total_ranks)*tot_frames))

#for state in stateList:
for frame in range(firstFrame,lastFrame):

	state = stateList[frame] - stateList[0]
	print("Loading state {}".format(state))
	SetTimeSliderState(frame) #if statelist is [3,4,5], frame=3(h5data) and state=0(xml list).

	tcur = timeTXT[state][5:-4]
	print("t/M = {}".format(int(float(tcur))))
	txt.text = "t/M = {}".format(int(float(tcur)))
	if density(): print(extrasDir + volumeXML[state])
	time.strftime("%Y-%m-%d %H:%M:%S")

	print("Loading Attibutes")
	LoadAttribute(extrasDir + viewXML[state], myView)

	if density():		LoadAttribute(extrasDir + volumeXML[state], vol)
	if bsq2r():			LoadAttribute(bsq2rXML, bsq_atts)
	if velocity():		LoadAttribute(vectorXML, vector_atts)

	if particles():
		LoadAttribute(streamXML, stream_particles)
		stream_particles.pointList = getSeeds(extrasDir + particlesTXT[state])
		if gridPoints():		
			stream_particles.singleColor = (0, 255, 0, 255)			

	if gridPoints():
		LoadAttribute(streamXML, stream_gridPoints)
		stream_gridPoints.pointList = getSeeds(extrasDir + gridPointsTXT[state])

	if g00():			LoadAttribute(g00_pseudoXML, g00_atts) 

	### adjust the cm focus ###
	CoM = getCoM(extrasDir + timeTXT[state])
	myView.focus = CoM
	CoM_x, CoM_y, CoM_z = CoM
	###########################

	######implement loaded plot settings
	print("setting settings")
	if density():
		SetActivePlots(idx("density"))
		SetPlotOptions(vol)
		#SetPlotOptions(rho_atts)
		#threshold(rho_threshXML)
		#iso(rho_isoXML)
		#reflect()
		if cutPlot: box(CoM_y, frame==firstFrame)
	if bsq2r():
		SetActivePlots(idx("bsq2r"))
		SetPlotOptions(bsq_atts)
		if cutPlot: box(CoM_y, frame==firstFrame)
	if particles():
		SetActivePlots(idx("particles"))
		SetPlotOptions(stream_particles)
	if gridPoints():
		SetActivePlots(idx("gridPoints"))
		SetPlotOptions(stream_gridPoints)
	if velocity():
		SetActivePlots(idx("vel"))
		SetPlotOptions(vector_atts)
		cylinder(CoM_x,CoM_y,45, frame==firstFrame)
		if cutPlot: box(CoM_y, frame==firstFrame)
	if g00():
		SetActivePlots(idx("g00"))
		SetPlotOptions(g00_atts)
		#threshold(g00_threshXML)
		iso(g00_isoXML)
		reflect()

	DrawAndSave(myView)
	time.strftime("%Y-%m-%d %H:%M:%S")

	xmltxt='/'.join(saveFolder.split('/')[:-1])+'/xml.txt'
	if(not isfile(xmltxt)):
		xt=open(xmltxt,'w')
		xt.write("View:\n")
		xt.write(str(myView))
		if density():
			xt.write('\n\n\nVol:\n')
			xt.write(str(vol))
		xt.close()

end_time = time.time()
elapsed_time = end_time - start_time
print(str(datetime.timedelta(seconds=elapsed_time)))

sys.exit()
