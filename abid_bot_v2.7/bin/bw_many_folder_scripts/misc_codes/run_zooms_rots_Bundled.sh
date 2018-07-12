zoom_in_flag=1
zoom_in_2_flag=0
zoom_out_flag=0

fly_over_flag=0
zoom_in_3_flag=0
fly_around_flag=0

rootdir=/u/sciteam/simone1/scratch/BHNS/case5/abid_bot_v2.7		#Update
savedir=$rootdir/bin/bw_many_folder_scripts/misc_codes/movies_zooms_rots/
schdir=$rootdir/bin/scheduler

lastFolder=3d_data_201710120940
lastIdx=5
############################# zoom_in
jobName=zoomIn
h5folder=3d_data_201801160650 #Last #3d_data_201710120940/
idx=5
savefolder=$savedir$jobName/
pyscript=zoom_and_change_vol.py
view1XML=$rootdir/bin/bw_many_folder_scripts/atts/c10.xml
    #leave this blank if you want to use the viewXML from params
view2XML=$rootdir/bin/bw_many_folder_scripts/atts/c8.xml

if [ $zoom_in_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# zoom_in_2
jobName=zoomIn2
h5folder=3d_data_201601120701/
idx=0
savefolder=$savedir$jobName/
pyscript=zoom_and_change_vol.py
view1XML=$rootdir/bin/bw_many_folder_scripts/atts/c10.xml
    #leave this blank if you want to use the viewXML from params
view2XML=$rootdir/bin/bw_many_folder_scripts/atts/c8.xml

if [ $zoom_in_2_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# zoom_out
jobName=zoomOut
h5folder=3d_data_201601120701/
idx=0
savefolder=$savedir$jobName/
pyscript=zoom.py
view1XML=    #invert the view1 and view2 from zoom_in to get zoom out.
view2XML=

if [ $zoom_out_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# fly_over
jobName=flyOver
h5folder=lastFolder 
idx=lastIdx
savefolder=$savedir$jobName/
pyscript=fly_over.py
if [ $fly_over_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $h5folder $idx $savefolder $pyscript
fi
#############################



############################# zoom_in_3
jobName=zoomIn3
h5folder=lastFolder
idx=lastIdx
savefolder=$savedir$jobName/
pyscript=zoom.py
view1XML=    #leave this blank if you want to use the viewXML from params
view2XML=

if [ $zoom_in_3_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# fly_around
jobName=flyAround
h5folder=lastFolder
idx=lastIdx
savefolder=$savedir$jobName/
pyscript=fly_around.py
if [ $fly_around_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $h5folder $idx $savefolder $pyscript
fi
#############################

