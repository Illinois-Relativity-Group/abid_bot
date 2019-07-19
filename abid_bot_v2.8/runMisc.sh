. params

if [[ -z $root ]]; then echo error: No root. Aborting. >&2; exit 1; fi

############################# Parameters
zoom_flag=1
zoom2_flag=0
zoom3_flag=0

fly_over_flag=0
fly_around_flag=0

#plotting varibles
PlotDensAsVol=1 # Plot density in a volume plot
PlotDensAsIso=0 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotBsq2r=0 # Plot B squared over 2 rho
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)

savedir=$root/movies
attsdir=$root/bin/bw_many_folder_scripts/atts
#############################



############################# zoom_1 #############################
jobName=zoom
h5folder=3d_data_201801160650 
idx=5
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/nsns_view_reg.xml
view2XML=$attsdir/nsns_view_topdown.xml
vol1XML=$attsdir/nsns_vol_dim.xml
vol2XML=$attsdir/nsns_vol_dim.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $zoom_flag -eq 1 ]]; then
	./bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $zoom_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML
fi
##################################################################



############################# zoom_2 #############################
jobName=zoom2
h5folder=/_/
idx=0
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/_.xml
view2XML=$attsdir/_.xml
vol1XML=$attsdir/_.xml
vol2XML=$attsdir/_.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $zoom2_flag -eq 1 ]]; then
	./bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $zoom2_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML
fi
##################################################################



############################# zoom_3 #############################
jobName=zoom3
h5folder=/_/
idx=0
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/_.xml
view2XML=$attsdir/_.xml
vol1XML=$attsdir/_.xml
vol2XML=$attsdir/_.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $zoom3_flag -eq 1 ]]; then
	./bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $zoom3_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML
fi
####################################################################



############################# fly_over #############################
jobName=flyOver
h5folder=/_/
idx=0
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/nsns_view_zoom_out.xml
vol1XML=$attsdir/nsns_vol_bright.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $fly_over_flag -eq 1 ]]; then
	./bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot 0 $fly_over_flag 0 $view1XML $vol1XML
fi
######################################################################


############################# fly_around #############################
jobName=flyAround
h5folder=/_/
idx=0
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/nsns_view_zoom_out.xml
vol1XML=$attsdir/nsns_vol_bright.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)
if [[ $fly_around_flag -eq 1 ]]; then
	./bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot 0 0 $fly_around_flag $view1XML $vol1XML
fi
######################################################################

