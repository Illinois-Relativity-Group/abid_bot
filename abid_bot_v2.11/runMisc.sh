. params

if [[ -z $root ]]; then echo error: No root. Aborting. >&2; exit 1; fi

############################# Parameters
zoom_flag=1


fly_over_flag=0
fly_around_flag=0


#plotting varibles
PlotDensAsVol=0 # Plot density in a volume plot
PlotDensAsIso=1 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=0 # Plot spin vector
PlotBsq2rAsVol=0 # Plot B squared over 2 rho in a volume plot
PlotBsq2rAsIso=0 # Plot B squared over 2 rho in a pseudocolor plot as isosurfaces
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xylplane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="blue" #background color

PlotVelCustom=0
VelCustomFile=$root/h5data/test.vtk


savedir=$root/movies
attsdir=$root/bin/bw_many_folder_scripts/atts
#############################



############################# zoom #############################
jobName=uncut_zoom
h5folder=3d_data_24_02_13_144642
idx=71
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
# view1XML=$attsdir/zoom1.xml
# view2XML=$attsdir/zoom2.xml
view1XML=$attsdir/zoom2.xml
view2XML=$attsdir/zoomin_last.xml
# view1XML=$attsdir/zoom2.xml
# view2XML=$attsdir/zoom_cut_upper.xml
#vol1XML=$attsdir/nsns_vol_dim.xml
#vol2XML=$attsdir/nsns_vol_dim.xml


ranksPerJob=5 # divisor of totframes

if [[ $zoom_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $PlotBsq2rAsIso $Plotg00 $refPlot $cutPlot $bgcolor $zoom_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML $PlotSpinVec $spinvecXML $PlotVelCustom $VelCustomFile
fi
##################################################################





############################# fly_over #############################
jobName=final_fly_over
h5folder=3d_data_24_02_13_144642
idx=71
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/zoom2.xml

ranksPerJob=5 # divisor of totframes

if [[ $fly_over_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $PlotBsq2rAsIso $Plotg00 $refPlot $cutPlot $bgcolor 0 $fly_over_flag 0 $view1XML $vol1XML $view2XML $vol2XML $PlotSpinVec $spinvecXML $PlotVelCustom $VelCustomFile
fi
######################################################################


############################# fly_around #############################
jobName=final_fly_around
h5folder=3d_data_24_02_13_144642
idx=71
totframes=100
pyscript=run.py

#$root/bin/bw_many_folder_scripts/atts/bhdisk_view_equatorial_superzoomin_first.xml
#leave this blank if you want to use the viewXML from params
#view1XML=$attsdir
#view1XML=$attsdir/bhdisk_view_equatorial.xml
view1XML=$attsdir/zoom2.xml
#view1XML=$attsdir/bhdisk_view_equatorial_superzoomin_first.xml


ranksPerJob=20 # divisor of totframes
if [[ $fly_around_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $PlotBsq2rAsIso $Plotg00 $refPlot $cutPlot $bgcolor 0 0 $fly_around_flag $view1XML $vol1XML 0 0 $PlotSpinVec $spinvecXML $PlotVelCustom $VelCustomFile
fi
######################################################################

