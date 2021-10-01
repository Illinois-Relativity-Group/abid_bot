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

PlotDensAsVol	= sys.argv[1] ==  '1' # Plot density in a volume plot
PlotDensAsIso	= sys.argv[2] ==  '1' # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear	= sys.argv[3] ==  '1' # Plot linear scale density rather than log scale
PlotVel  		= sys.argv[4] ==  '1' # Plot velocity arrows
PlotBsq2r		= sys.argv[5] ==  '1' # Plot B squared over 2 rho
Plotg00  		= sys.argv[6] ==  '1' # Plot g00 from metric
refPlot			= sys.argv[7] ==  '1' # Reflect plot over xy plane
cutPlot  		= sys.argv[8] ==  '1' # only show back half (y>0), needs view like: (0,-x,y)
bgcolor			= sys.argv[9] #Background color

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
vectorXML 		= sys.argv[20]
bsq2rXML 		= sys.argv[21]
max_density 	= sys.argv[22]
rho_pseudoXML 	= sys.argv[23]
rho_isoXML 		= sys.argv[24]
g00_pseudoXML 	= sys.argv[25]
g00_isoXML 		= sys.argv[26]

########## EXPERIMENTAL ##########
if PlotZoom or PlotFlyOver or PlotFlyAround:
	idx = int(sys.argv[29])
	num_frames = int(sys.argv[30])
	view_initial = sys.argv[31]
	vol_initial = sys.argv[32]
	miscatts = [idx, num_frames, view_initial, vol_initial]
	if PlotZoom:
		view_final = sys.argv[33]
		vol_final = sys.argv[34]
		miscatts += [view_final, vol_final]

##################################


combos = [PlotEvolve and PlotZoom, PlotEvolve and PlotFlyOver, PlotEvolve and PlotFlyAround, PlotZoom and PlotFlyOver, PlotZoom and PlotFlyAround, PlotFlyOver and PlotFlyAround]
for combo in combos:
	if combo:
		print("Can't have two types of evolution in one plot")
		sys.exit()

print(sys.argv)
PlotOpts = [ PlotDensAsVol, PlotDensAsIso, PlotDensLinear, PlotVel, PlotSpinVec, PlotBsq2r, Plotg00, refPlot,\
			 cutPlot, bgcolor ]
ArgList  = [ h5dir, extrasDir, saveFolder, rank, total_ranks, numBfieldPlots, vectorXML, SpinVecXML,\
			 bsq2rXML, max_density, rho_pseudoXML, rho_isoXML, g00_pseudoXML, g00_isoXML ]

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
