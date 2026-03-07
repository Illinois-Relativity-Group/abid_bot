. params

if [[ -z $root ]]; then echo error: No root. Aborting. >&2; exit 1; fi

############################# Parameters
zoom_flag=1
zoom2_flag=0
zoom3_flag=0

fly_over_flag=0
fly_around_flag=0

savedir=$root/movies
schdir=$root/bin/scheduler
attsdir=$root/bin/bw_many_folder_scripts/atts
#############################



############################# zoom_1 #############################
jobName=zoom
h5folder=3d_data_201801160650 
idx=5
totframes=100
savefolder=$savedir/$jobName/
pyscript=zoom.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/nsns_view_reg.xml
view2XML=$attsdir/nsns_view_topdown.xml
vol1XML=$attsdir/nsns_vol_dim.xml
vol2XML=$attsdir/nsns_vol_dim.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $zoom_flag -eq 1 ]]; then
	./bin/filmBundled.sh $root $jobName $h5folder $idx $totframes $savefolder $pyscript $view1XML $view2XML $vol1XML $vol2XML
fi
##################################################################



############################# zoom_2 #############################
jobName=zoom2
h5folder=/_/
idx=0
totframes=100
savefolder=$savedir/$jobName/
pyscript=zoom.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/_.xml
view2XML=$attsdir/_.xml
vol1XML=$attsdir/_.xml
vol2XML=$attsdir/_.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $zoom2_flag -eq 1 ]]; then
	./bin/filmBundled.sh $rootdir $jobName $h5folder $idx $totframes $savefolder $pyscript $view1XML $view2XML $vol1XML $vol2XML
fi
##################################################################



############################# zoom_3 #############################
jobName=zoom3
h5folder=/_/
idx=0
totframes=100
savefolder=$savedir/$jobName/
pyscript=zoom.py

#leave this blank if you want to use the viewXML from params
view1XML=$attsdir/_.xml
view2XML=$attsdir/_.xml
vol1XML=$attsdir/_.xml
vol2XML=$attsdir/_.xml

ranksPerJob=5 # divisor of int((totframes+1)/2)

if [[ $zoom3_flag -eq 1 ]]; then
	./bin/filmBundled.sh $rootdir $jobName $h5folder $idx $totframes $savefolder $pyscript $view1XML $view2XML $vol1XML $vol2XML
fi
####################################################################



############################# fly_over #############################
jobName=flyOver
h5folder=/_/
idx=0
totframes=100
savefolder=$savedir/$jobName/
pyscript=fly_over.py
if [[ $fly_over_flag -eq 1 ]]; then
	./bin/filmBundled.sh $rootdir $jobName $h5folder $idx $totframes $savefolder $pyscript
fi
######################################################################


############################# fly_around #############################
jobName=flyAround
h5folder=/_/
idx=0
totframes=100
savefolder=$savedir/$jobName/
pyscript=fly_around.py
if [[ $fly_around_flag -eq 1 ]]; then
	./bin/filmBundled.sh $rootdir $jobName $h5folder $idx $totframes $savefolder $pyscript
fi
######################################################################

