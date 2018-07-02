zoom_in_flag=1
zoom_in_2_flag=0
zoom_out_flag=0

fly_over_flag=0
zoom_in_3_flag=0
fly_around_flag=0

rootdir=/u/sciteam/simone1/scratch/BHNS/case5/abid_bot_v2.7		#Update
savedir=$rootdir/bin/bw_many_folder_scripts/misc_codes/movies_zooms_rots/
schdir=$rootdir/bin/scheduler

############################# zoom_in
jobName=zoom_in_end
joblistID=0
h5folder=3d_data_201801160650 #Last #3d_data_201710120940/
idx=5 #3
savefolder=$savedir$jobName/
pyscript=zoom_and_change_vol.py
view1XML=$rootdir/bin/bw_many_folder_scripts/atts/c10.xml
    #leave this blank if you want to use the viewXML from params
view2XML=$rootdir/bin/bw_many_folder_scripts/atts/c8.xml

if [ $zoom_in_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $joblistID $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# zoom_in_2
jobName=zoom_in_2
joblistID=1
h5folder=3d_data_201601120701/
idx=0
savefolder=$savedir$jobName/
pyscript=zoom_and_change_vol.py
view1XML=$rootdir/bin/bw_many_folder_scripts/atts/c10.xml
    #leave this blank if you want to use the viewXML from params
view2XML=$rootdir/bin/bw_many_folder_scripts/atts/c8.xml

if [ $zoom_in_2_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $joblistID $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# zoom_out
jobName=zoom_out
joblistID=2
h5folder=3d_data_201601120701/
idx=0
savefolder=$savedir$jobName/
pyscript=zoom.py
view1XML=    #invert the view1 and view2 from zoom_in to get zoom out.
view2XML=

if [ $zoom_out_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $joblistID $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# fly_over
jobName=fly_over
joblistID=3
h5folder=3d_data_201801160650 #3d_data_201802230414  #3d_data_17_05_22_000000/
idx=5 #7
# fly_over
savefolder=$savedir$jobName/
pyscript=fly_over.py
if [ $fly_over_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $joblistID $h5folder $idx $savefolder $pyscript
fi
#############################



############################# zoom_in_3
jobName=zoom_in_3
joblistID=4
savefolder=$savedir$jobName/
pyscript=zoom.py
view1XML=    #leave this blank if you want to use the viewXML from params
view2XML=

if [ $zoom_in_3_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $joblistID $h5folder $idx $savefolder $pyscript $view1XML $view2XML
fi
#############################



############################# fly_around
jobName=fly_around
joblistID=5
h5folder=3d_data_201801160650 #3d_data_201802230414
idx=5
savefolder=$savedir$jobName/
pyscript=fly_around.py
if [ $fly_around_flag -eq 1 ]
then
	./filmBundled.sh $rootdir $jobName $joblistID $h5folder $idx $savefolder $pyscript
fi
#############################

#qsub $schdir/run
