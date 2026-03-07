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
#for i in range(1, 35):
    #print(sys.argv[i])

PlotDensAsVol	= sys.argv[1]  # Plot density in a volume plot
PlotDensAsIso	= sys.argv[2]  # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear	= sys.argv[3]  # Plot linear scale density rather than log scale
PlotVel  		= sys.argv[4]  # Plot velocity arrows
PlotBsq2rAsVol		= sys.argv[5]  # Plot B squared over 2 rho as volume
PlotBsq2rAsIso          = 0#sys.argv[32] # Plot B squared over 2 rho as iso
Plotg00  		= sys.argv[6]  # Plot g00 from metric
refPlot			= sys.argv[7]  # Reflect plot over xy plane
cutPlot  		= sys.argv[8]  # only show back half (y>0), needs view like: (0,-x,y)
bgcolor			= sys.argv[9] #Background color

########## EXPERIMENTAL ##########
PlotEvolve 		= 0 #sys.argv[10] 
PlotZoom 		= sys.argv[11]
PlotFlyOver 	= sys.argv[12]
PlotFlyAround 	= sys.argv[13] 
##################################
PlotSpinVec	= sys.argv[27]
SpinVecXML	= sys.argv[28]
##################################

h5dir 			= sys.argv[14]
extrasDir 		= sys.argv[15]
saveFolder 		= sys.argv[16]
rank 			= int(sys.argv[17])
total_ranks 	= int(sys.argv[18])
numBfieldPlots	= int(sys.argv[19])
vector1XML 		= sys.argv[20]
vector2XML		= sys.argv[35]

bsq2rXML 		= sys.argv[21]
bsq2r_pseudoXML         = sys.argv[36]
bsq2r_isoXML            = sys.argv[37]
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
    print(combo)

for combo in combos:
	if combo:
		print("Can't have two types of evolution in one plot")
		#sys.exit()

print(sys.argv)
PlotOpts = [ PlotDensAsVol, PlotDensAsIso, PlotDensLinear, PlotVel, PlotSpinVec, PlotBsq2rAsVol, PlotBsq2rAsIso, Plotg00, refPlot,\
			 cutPlot, bgcolor ]
ArgList  = [ h5dir, extrasDir, saveFolder, rank, total_ranks, numBfieldPlots, vector1XML, vector2XML, SpinVecXML,
			 bsq2rXML, bsq2r_pseudoXML, bsq2r_isoXML, max_density, rho_pseudoXML, rho_isoXML, g00_pseudoXML, g00_isoXML ] #bsq2r_psedoXML, bsq2r_isoXML was between bsq2r_pXML and max_density

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
