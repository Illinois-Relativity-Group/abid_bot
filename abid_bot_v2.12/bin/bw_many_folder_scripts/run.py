#Run with something like 
#visit -cli -nowin -forceversion 2.7.3 -s $visitScript $dir $xmldir $saveFolder $rank $totranks $streamXML $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML

import random
import csv
import sys
import time
import datetime



from runModule import VisitPlot
from os import listdir, rename
from os.path import isfile, join
from fnmatch import fnmatch

###############################################################################
##### SETTING PARAMETERS
###############################################################################
start_time = time.time()

x = [0,1]
t = 0.5
view_i = View3DAttributes()
view_f = View3DAttributes()
cpts = (view_i, view_f)
print("hello")
c = EvalCubicSpline(t, x, cpts)
print(c)
print("hello2")




PlotDensAsVol	= sys.argv[1] ==  '1'# Plot density in a volume plot
PlotDensAsIso	= sys.argv[2] ==  '1' # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear	= sys.argv[3] ==  '1' # Plot linear scale density rather than log scale
PlotVel  		= sys.argv[4] ==  '1' # Plot velocity arrows
PlotBsq2rAsVol		= sys.argv[5] ==  '1' # Plot B squared over 2 rho as volume
PlotBsq2rAsIso          = sys.argv[32] == '1' # Plot B squared over 2 rho as iso
Plotg00  		= sys.argv[6] ==  '1' # Plot g00 from metric
refPlot			= sys.argv[7] ==  '1' # Reflect plot over xy plane
cutPlot  		= sys.argv[8] ==  '1' # only show back half (y>0), needs view like: (0,-x,y)
bgcolor			= sys.argv[9] #Background color


PlotVelCustom   = sys.argv[33] == '1' # plot vel with custom generated .vtk file
VelCustomFile   = sys.argv[34]        # custom .vtk file

PlotGW2D = sys.argv[35]	== '1'	#Plot 2D GW waves
PlotGW3D = sys.argv[36]	== '1'	#Plot 3D GW waves

PlotShapeCustom = sys.argv[37] == '1' # plot shape with custom generated .3d file
ShapeCustomFile = sys.argv[38]        # custom .3d file

########## EXPERIMENTAL ##########
PlotEvolve 		= sys.argv[10] ==  '1'
PlotZoom 		= sys.argv[11] ==  '1'
PlotFlyOver 	= sys.argv[12] ==  '1'
PlotFlyAround 	= sys.argv[13] ==  '1'
##################################
PlotSpinVec	= sys.argv[27] ==  '1'
SpinVecXML	= sys.argv[28]
##################################

h5dir 			= sys.argv[14]
extrasDir 		= sys.argv[15]
saveFolder 		= sys.argv[16]
rank 			= int(sys.argv[17])
total_ranks 	= int(sys.argv[18])
numBfieldPlots	= int(sys.argv[19])
vector1XML 		= sys.argv[20]
vector2XML		= sys.argv[29]
print(sys.argv)
bsq2rXML 		= sys.argv[21]; print("bsq2rXML = ", bsq2rXML)
bsq2r_pseudoXML         = sys.argv[30]
bsq2r_isoXML            = sys.argv[31]
max_density 	= sys.argv[24]; print("maxdensity = ", max_density)
rho_pseudoXML 	= sys.argv[25]; print("rho_pseudoXML = ", rho_pseudoXML)
rho_isoXML 		= sys.argv[26]; print("rho_isoXML = ", rho_isoXML)
g00_pseudoXML 	= sys.argv[22]; print("g00_pseudoXML = ", g00_pseudoXML)
g00_isoXML 		= sys.argv[23]; print("g00_isoXML = ", g00_isoXML)
gw3D_volXML = sys.argv[39]

########## EXPERIMENTAL ##########
if PlotZoom or PlotFlyOver or PlotFlyAround:
	idx = int(sys.argv[40])
	num_frames = int(sys.argv[41])
	view_initial = sys.argv[42]
	vol_initial = sys.argv[43]
	miscatts = [idx, num_frames, view_initial, vol_initial]
	if PlotZoom:
		view_final = sys.argv[44]
		vol_final = sys.argv[45]
		miscatts += [view_final, vol_final]
		print("view final is ", view_final)

##################################


combos = [PlotEvolve and PlotZoom, PlotEvolve and PlotFlyOver, PlotEvolve and PlotFlyAround, PlotZoom and PlotFlyOver, PlotZoom and PlotFlyAround, PlotFlyOver and PlotFlyAround]
for combo in combos:
	if combo:
		print("Can't have two types of evolution in one plot")
		sys.exit()

print(sys.argv)
PlotOpts = [ PlotDensAsVol, PlotDensAsIso, PlotDensLinear, PlotVel, PlotSpinVec, PlotBsq2rAsVol, PlotBsq2rAsIso, PlotVelCustom, PlotShapeCustom, PlotGW2D, PlotGW3D, Plotg00, refPlot,\
			 cutPlot, bgcolor ]
ArgList  = [ h5dir, extrasDir, saveFolder, rank, total_ranks, numBfieldPlots, vector1XML, vector2XML, SpinVecXML,\
			 bsq2rXML, bsq2r_pseudoXML, bsq2r_isoXML, max_density, rho_pseudoXML, rho_isoXML, g00_pseudoXML, g00_isoXML, VelCustomFile, ShapeCustomFile, gw3D_volXML]

time.strftime("%Y-%m-%d %H:%M:%S")


########## MAIN ##########
myPlot = VisitPlot(PlotOpts, ArgList)
print(myPlot)
myPlot.SetPlots()
if PlotEvolve:
	myPlot.PlotEvolve()
	
if PlotZoom:
	myPlot.PlotZoom(miscatts)
	
if PlotFlyOver:
	myPlot.PlotFlyOver(miscatts)
	
if PlotFlyAround:
	myPlot.PlotFlyAround(miscatts)
##########################

end_time = time.time()
elapsed_time = end_time - start_time
print("Runtime: {} sec".format(datetime.timedelta(seconds=elapsed_time)))

sys.exit()
