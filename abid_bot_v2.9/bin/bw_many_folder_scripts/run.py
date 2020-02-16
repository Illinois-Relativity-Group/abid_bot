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

########## EXPERIMENTAL ##########
PlotEvolve 		= sys.argv[9] ==  '1'
PlotZoom 		= sys.argv[10] ==  '1'
PlotFlyOver 	= sys.argv[11] ==  '1'
PlotFlyAround 	= sys.argv[12] ==  '1'
##################################

combos = [PlotEvolve and PlotZoom, PlotEvolve and PlotFlyOver, PlotEvolve and PlotFlyAround, PlotZoom and PlotFlyOver, PlotZoom and PlotFlyAround, PlotFlyOver and PlotFlyAround]
for combo in combos:
	if combo:
		print("Can't have two types of evolution in one plot")
		sys.exit()

print(sys.argv)
h5dir 			= sys.argv[13]
extrasDir 		= sys.argv[14]
saveFolder 		= sys.argv[15]
rank 			= int(sys.argv[16])
total_ranks 	= int(sys.argv[17])
numBfieldPlots	= int(sys.argv[18])
vectorXML 		= sys.argv[19]
bsq2rXML 		= sys.argv[20]
max_density 	= sys.argv[21]
rho_pseudoXML 	= sys.argv[22]
rho_isoXML 		= sys.argv[23]
g00_pseudoXML 	= sys.argv[24]
g00_isoXML 		= sys.argv[25]

		
PlotOpts = [ PlotDensAsVol, PlotDensAsIso, PlotDensLinear, PlotVel, PlotBsq2r, Plotg00, refPlot,\
			 cutPlot ]
ArgList  = [ h5dir, extrasDir, saveFolder, rank, total_ranks, numBfieldPlots, vectorXML,\
			 bsq2rXML, max_density, rho_pseudoXML, rho_isoXML, g00_pseudoXML, g00_isoXML ]

time.strftime("%Y-%m-%d %H:%M:%S")


########## EXPERIMENTAL ##########
if PlotZoom or PlotFlyOver or PlotFlyAround:
	idx = int(sys.argv[31])
	num_frames = int(sys.argv[32])
	view_initial = sys.argv[33]
	vol_initial = sys.argv[34]
	miscatts = [idx, num_frames, view_initial, vol_initial]
	if PlotZoom:
		view_final = sys.argv[35]
		vol_final = sys.argv[36]
		miscatts += [view_final, vol_final]

##################################


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
