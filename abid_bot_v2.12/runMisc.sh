. params

if [[ -z $root ]]; then echo error: No root. Aborting. >&2; exit 1; fi

############################# Parameters
zoom_flag=1
zoom2_flag=0
zoom3_flag=0

fly_over_flag=0
fly_around_flag=0

#plotting variables
PlotDensAsVol=0 # Plot density in a volume plot
PlotDensAsIso=1 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=0 # Plot spin vector
PlotBsq2rAsVol=0 # Plot B squared over 2 rho
PlotBsq2rAsIso=0 # Plot B squared over 2 rho	
Plotg00=0 # Plot g00 from metric
PlotGW2D=0	#Plot 2D gravitational waves
PlotGW3D=1	#Plot 3D gravitational waves
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="black" #background color

PlotShapeCustom=1
ShapeCustomFile=$root/h5data/shape.3d   #make sure 4th column is named 'test' and .3d file is in h5data

####### DON'T touch these, are settings only for single frames
PlotVelCustom=0
VelCustomFile="notused"

savedir=$root/movies
attsdir=$root/bin/bw_many_folder_scripts/atts
#############################



############################# zoom_1 #############################
jobName=Final_runMisc
h5folder=3d_data_23_10_26_191521
idx=0
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/gw_view_bowl.xml
view2XML=$attsdir/gw_view_topdown.xml
#vol1XML=$attsdir/nsns_vol_dim.xml
#vol2XML=$attsdir/nsns_vol_dim.xml


ranksPerJob=10 # divisor of totframes

if [[ $zoom_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $PlotBsq2rAsIso $Plotg00 $refPlot $cutPlot $bgcolor $zoom_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML $PlotSpinVec $spinvecXML $PlotVelCustom $VelCustomFile $PlotGW2D $PlotGW3D $PlotShapeCustom $ShapeCustomFile $gw3D_volXML
fi
##################################################################



############################# zoom_2 #############################
jobName=zoom2
h5folder=3d_data_24_01_23_170525
idx=121
totframes=100
pyscript=nsnsrun.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/zoomin_last.xml
view2XML=$attsdir/zoom2.xml
vol1XML=$attsdir/_.xml
vol2XML=$attsdir/_.xml

ranksPerJob=2 # divisor of totframes

if [[ $zoom2_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor $zoom_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML $PlotSpinVec $spinvecXML
fi
##################################################################



############################# zoom_3 #############################
jobName=zoom3
h5folder=/_/
idx=0
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/zoom1.xml
view2XML=$attsdir/zoom1_top.xml
vol1XML=$attsdir/_.xml
vol2XML=$attsdir/_.xml

ranksPerJob=5 # divisor of totframes

if [[ $zoom3_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor $zoom_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML $PlotSpinVec $spinvecXML
fi
####################################################################



############################# fly_over #############################
jobName=flyOver
h5folder=3d_data_24_01_23_170525
idx=121
totframes=100
pyscript=nsnsrun.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/zoom2.xml

ranksPerJob=1 # divisor of totframes

if [[ $fly_over_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor 0 $fly_over_flag 0 $view1XML $vol1XML 0 0 $PlotSpinVec $spinvecXML
fi
######################################################################


############################# fly_around #############################
jobName=flyAround_massive
h5folder=3d_data_202301031738
idx=0
totframes=100
pyscript=run.py

#$root/bin/bw_many_folder_scripts/atts/bhdisk_view_equatorial_superzoomin_first.xml
#leave this blank if you want to use the viewXML from params
#view1XML=$attsdir
#view1XML=$attsdir/bhdisk_view_equatorial.xml
view1XML=$attsdir/bhdisk_view_equatorial_out.xml
#view1XML=$attsdir/bhdisk_view_equatorial_superzoomin_first.xml


ranksPerJob=20 # divisor of totframes
if [[ $fly_around_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor 0 0 $fly_around_flag $view1XML $vol1XML 0 0 $PlotSpinVec $spinvecXML
fi
######################################################################

