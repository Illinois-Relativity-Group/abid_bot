. local_params
#Use this if you are submitting very few folders (~1-5)
#Otherwise use runBundle.sh
#####begin things you have to change TODO

jobName=test_frame
h5dir=$root/h5data
extrasDir=$root/xml
h5prefix=3d_data_
foldernum=1 #1 indexed
ranknum=0 #0 indexed, frame you want to image

########run movies variables

pbsfile=$root/bin/bw_many_folder_scripts/singleRun.pbs
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/local_run.py
totranks=5 #total number of frames
#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
savefolder=$( echo $savefolder | sed "s,/$,,")
picsavefolder=$( echo $picsavefolder | sed "s,/$,,")

#plotting varibles
PlotDensAsVol=1 # Plot density in a volume plot
PlotDensAsIso=0 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotBsq2r=0 # Plot B squared over 2 rho
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)

PlotEvolve=1
PlotZoom=0
PlotFlyOver=0
PlotFlyAround=0

##########This section submits the rest of the files.
# default is first frame
count=1
DATE=$(date +%y%m%d_%H%M)
picsavefolder=$picsavedir/"$DATE"_"$jobName"; mkdir -p $picsavefolder
logfolder=$logdir/"$DATE"_"$jobName";         mkdir -p $logfolder
logfile=$logfolder/output_runModule.txt

cd $logfolder

for dir in $(ls -d ${h5dir}"/"$h5prefix* ); do
    blah=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
    tosave="$picsavefolder"/"$jobName"_$(printf "%03d" $count)_

	if [ $count -eq $foldernum ]; then
		for rank in `seq 0 $(( $totranks - 1 ))`; do
				if [ $rank -eq $ranknum ]; then
		        		echo running folder $count frame $rank
					visit -cli -nowin -forceversion 2.9.2 -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $blah $tosave$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML >> $logfile
					echo "done :)"
				fi
		done
	fi
    count=$((count+1))
done

cd $root
