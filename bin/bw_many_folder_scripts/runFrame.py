#Run with something like 
#visit -cli -nowin -forceversion 2.7.3 -s $visitScript $dir $xmldir $saveFolder $rank $totranks $streamXML $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML $viewXML $volXML

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

PlotDensAsVol	= 1 # Plot density in a volume plot
PlotDensAsIso	= 0 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear	= 0 # Plot linear scale density rather than log scale
PlotVel  		= 0 # Plot velocity arrows
PlotBsq2r		= 0 # Plot B squared over 2 rho
Plotg00  		= 0 # Plot g00 from metric
refPlot			= 1 # Reflect plot over xy plane
cutPlot  		= 0 # only show back half (y>0), needs view like: (0,-x,y)

##################################

print(sys.argv, len(sys.argv))
sysargv_start = 1
print(len(sys.argv[sysargv_start:]))
h5dir, extrasDir, saveFolder, rank, total_ranks, numBfieldPlots, vectorXML, bsq2rXML, max_density, rho_pseudoXML, rho_isoXML, g00_pseudoXML, g00_isoXML, viewXML, volXML, frame_idx, seed_file, streamXML = sys.argv[sysargv_start:]

rank 			= int(rank)
total_ranks 	= int(total_ranks)
numBfieldPlots	= int(numBfieldPlots)
frame_idx		= int(frame_idx)
		
PlotOpts = [ PlotDensAsVol, PlotDensAsIso, PlotDensLinear, PlotVel, PlotBsq2r, Plotg00, refPlot,\
			 cutPlot ]
ArgList  = [ h5dir, extrasDir, saveFolder, rank, total_ranks, numBfieldPlots, vectorXML,\
			 bsq2rXML, max_density, rho_pseudoXML, rho_isoXML, g00_pseudoXML, g00_isoXML ]

time.strftime("%Y-%m-%d %H:%M:%S")

########## MAIN ##########
myPlot = VisitPlot(PlotOpts, ArgList)
print(myPlot)
attributes = [ viewXML, volXML, myPlot.rho_pseudoXML, myPlot.bsq2rXML, myPlot.vectorXML, myPlot.g00_pseudoXML, seed_file, streamXML ]
myPlot.SetPlots()
view3D = GetView3D()
myPlot.SetAtts(view3D, myPlot.txt, frame_idx, attributes)
myPlot.PlotFrame(view3D, frame_idx)
##########################

end_time = time.time()
elapsed_time = end_time - start_time
print("Runtime: {} sec".format(datetime.timedelta(seconds=elapsed_time)))

sys.exit()
