if [[ -f "params$1" ]];then
        echo "using params$1"
        . params$1
else
        echo "params$1 not found. using params"
        . params
fi

#option to reduce number of folders images
all=false                      #Runs all folders if true, if false will run from
firstFolder=6         #       firstFolder to lastFolder. 
lastFolder=9        #      folder numbers are 1-indexed, so starts at 1
framesPerRun=4   



jobName=bsq2r_movie
h5dir=$root/h5data
extrasDir=$root/xml$1
h5prefix=3d_data_

########run movies variables

templatefile=$root/bin/scheduler/multirun_template_anvil
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/run.py
#totranks=0 -- auto detect, no longer need to set
#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
savefolder=$( echo $savefolder | sed "s,/$,,")
picsavefolder=$( echo $picsavefolder | sed "s,/$,,")

#plotting varibles
PlotDensAsVol=0 # Plot density in a volume plot
PlotDensAsIso=1 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=0 # Plot spin vector
PlotSpinPlane=0 # plot plane perpendicular to spin vector
PlotBsq2rAsVol=0 # Plot B squared over 2 rho in a volume plot
PlotBsq2rAsIso=1 # Plot B squared over 2 rho in a pseudocolor plot as isosurfaces
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="blue" #background color



####### DON'T touch these, are settings only for single frames
PlotVelCustom=0
VelCustomFile="notused"

PlotEvolve=1
PlotZoom=0
PlotFlyOver=0
PlotFlyAround=0

##########This section submits the rest of the files.
# default is first frame
#foldernum=(0 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300)	#starts from 1, list all folders you want to run
foldernum=(101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120) 
ranknum=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)
#ranknum=(0)
#ranknum=(10)		#starts from 0, list all ranks in each folder you want to run
count=1
frame_count=0
job_num=0
DATE=$(date +%y%m%d_%H%M)
picsavefolder=$picsavedir/"$DATE"_"$jobName"; mkdir -p $picsavefolder
#picsavefolder=$picsavedir/"$jobName"; mkdir -p $picsavefolder		#if you don't want date&time in folder name
logfolder=$logdir/"$DATE"_"$jobName"; mkdir -p $logfolder

cd $logfolder
mkdir -p $logfolder/run
mkdir -p $logfolder/job
mkdir -p $logfolder/out 

for dir in $(ls -d ${h5dir}"/"$h5prefix* ); do
	if [ $all = true ] || [ $count -ge $firstFolder -a $count -le $lastFolder ]; then
    		blah=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
   	 	tosave="$picsavefolder"/"$jobName"_$(printf "%03d" $count)_
		totranks=$(ls ${blah}/time_* | wc -l)
		for rank in `seq 0 $(( $totranks - 1 ))`; do
			jobfile=$logfolder/job/job$job_num.sh
			echo visit -cli -nowin -forceversion 3.1.4 -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $blah $tosave$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $g00_pseudoXML $g00_isoXML $maxdensity $rho_pseudoXML $rho_isoXML $PlotSpinVec $spinvecXML $vec2XML $bsq_pseudoXML $bsq_isoXML $PlotBsq2rAsIso $PlotVelCustom $VelCustomFile >> $jobfile
			frame_count=$((frame_count+1))
			if [[ "$frame_count" -ge "$framesPerRun" ]]; then
				frame_count=0
				job_num=$((job_num+1))	
			fi
		done
	fi
    count=$((count+1))
done

totjobs=$(ls $logfolder/job/* | wc -l)
template=
for ((c=0; c<$totjobs; c++)); do
	runfile=$logfolder/run/run$c.sh
	cat $templatefile $logfolder/job/job$c.sh >> $logfolder/run/run$c.sh
	echo "submitting job $c"
	sbatch $logfolder/run/run$c.sh
 	

done
echo " done"
cd $root
