# riemann: VisIt 3.3.3 is installed system-wide, no module system
export PATH=/data/shared/visit/bin:$PATH

# honour the same setN argument as setup.sh and the other run scripts:
# ". runMisc.sh 2" reads params2 and renders from xml2/
setN=$1
if [[ -f "params$setN" ]];then
	echo "using params$setN"
	. params$setN
else
	[[ -n "$setN" ]] && echo "params$setN not found. using params"
	setN=""
	. params
fi

# sourced, not executed (README says ". runMisc.sh"), so an exit here would
# close the user's shell -- return when we can, exit only if run as a script.
if [[ -z $root ]]; then echo "error: No root. Aborting." >&2; return 1 2>/dev/null || exit 1; fi

############################# Parameters
zoom_flag=0


fly_over_flag=0
# All three flags ship OFF. Turn exactly one on, and set the h5folder for
# that section below to a folder that exists in YOUR h5data -- the names
# shipped here are from the case this file was inherited from.
fly_around_flag=0


#plotting varibles
PlotDensAsVol=0 # Plot density in a volume plot
PlotDensAsIso=1 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=1 # Plot spin vector
PlotBsq2rAsVol=0 # Plot B squared over 2 rho in a volume plot
PlotBsq2rAsIso=0 # Plot B squared over 2 rho in a pseudocolor plot as isosurfaces
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xylplane
cutPlot=1 # only show back half; set cutNormal in params
bgcolor="blue" #background color

PlotVelCustom=0
VelCustomFile=$root/h5data/test.vtk


savedir=$root/movies
attsdir=$root/bin/bw_many_folder_scripts/atts
#############################



############################# zoom #############################
jobName=my_case_misc
h5folder=3d_data_25_11_01_051428   # CHANGE ME: inherited example, almost certainly not in your h5data
idx=15
totframes=100
pyscript=run.py

#leave this blank if you want to use the viewXML from params
# view1XML=$attsdir/zoom1.xml
# view2XML=$attsdir/zoom2.xml
view1XML=$attsdir/bhdisk_view_30deg.xml
view2XML=$attsdir/bhdisk_view_30deg_zoomin.xml
# view1XML=$attsdir/zoom2.xml
# view2XML=$attsdir/zoom_cut_upper.xml
#vol1XML=$attsdir/nsns_vol_dim.xml
#vol2XML=$attsdir/nsns_vol_dim.xml


ranksPerJob=20 # divisor of totframes

if [[ $zoom_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $PlotBsq2rAsIso $Plotg00 $refPlot $cutPlot $bgcolor $zoom_flag 0 0 $view1XML $vol1XML $view2XML $vol2XML $PlotSpinVec $spinvecXML $PlotVelCustom $VelCustomFile
fi
##################################################################





############################# fly_over #############################
jobName=my_case_misc
h5folder=3d_data_24_02_13_144642   # CHANGE ME: inherited example, almost certainly not in your h5data
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
jobName=my_case_misc
h5folder=3d_data_25_12_05_035059   # CHANGE ME: inherited example, almost certainly not in your h5data
idx=26
totframes=100
pyscript=run.py

#$root/bin/bw_many_folder_scripts/atts/bhdisk_view_equatorial_superzoomin_first.xml
#leave this blank if you want to use the viewXML from params
#view1XML=$attsdir
#view1XML=$attsdir/bhdisk_view_equatorial.xml
view1XML=$attsdir/bhdisk_view_30deg_zoomin.xml
#view1XML=$attsdir/bhdisk_view_equatorial_superzoomin_first.xml


ranksPerJob=5 # divisor of totframes
if [[ $fly_around_flag -eq 1 ]]; then
	. bin/filmBundled.sh $jobName $h5folder $idx $totframes $ranksPerJob $savedir $pyscript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $PlotBsq2rAsIso $Plotg00 $refPlot $cutPlot $bgcolor 0 0 $fly_around_flag $view1XML $vol1XML 0 0 $PlotSpinVec $spinvecXML $PlotVelCustom $VelCustomFile
fi
######################################################################

