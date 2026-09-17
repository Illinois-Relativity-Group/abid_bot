cur=$PWD

#####begin things you have to change TODO



jobName=$1
dir=$root/h5data/$2
xmldir=$root/xml/$2
idx=$3
totframes=$4
ranksPerjob=$5
picsavedir=$6
visitScript=$7
PlotDensAsVol=$8 # Plot density in a volume plot
PlotDensAsIso=$9 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=${10} # Plot linear scale density rather than log scale
PlotVel=${11} # Plot velocity arrows
PlotBsq2rAsVol=${12} # Plot B squared over 2 rho
PlotBsq2rAsIso=${13} # Plot B squared over 2 rho
Plotg00=${14} # Plot g00 from metric
refPlot=${15} # Reflect plot over xy plane
cutPlot=${16} # only show back half (y>0), needs view like: (0,-x,y)
bgcolor=${17} #background color
PlotZoom=${18}
PlotFlyOver=${19}
PlotFlyAround=${20}

PlotEvolve=0

view1XML=${21} #Overwrite view1XML, vol1XMl, view2XML, vol2XML
vol1XML=${22}
view2XML=${23}
vol2XML=${24}

PlotSpinVec=${25}
spinvecXML=${26}


PlotVelCustom=${27}
VelCustomFile=${28}

########run movies variables
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/${pyscript}
totranks=$((totframes))
#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,," )
h5dir=$( echo $h5dir | sed "s,/$,," )
picsavedir=$( echo $picsavedir | sed "s,/$,," )

#scheduler
schdir=$root/bin/scheduler
##########This section submits the rest of the files.
DATE=$(date +%y%m%d_%H%M);
picsavefolder=$picsavedir/"$DATE"_$jobName;	mkdir -p $picsavefolder
picsavefolder=$picsavefolder/$jobName"_"

logfolder=$logdir/$DATE"_"$jobName;	mkdir -p $logfolder
cd $logfolder; 	
	mkdir -p $logfolder/joblist
	mkdir -p $logfolder/run
	mkdir -p $logfolder/job
	mkdir -p $logfolder/out
echo "Writing jobs to joblist..."

framesPerRun=5
frame_count=0
job_num=0
for rank in `seq 0 $(( $totranks - 1 ))`; do
	jobfile=$logfolder/job/job$job_num.sh
	
	
	echo visit -forceversion 3.3.3 -cli -nowin -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $xmldir $picsavefolder$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $g00_pseudoXML $g00_isoXML $maxdensity $rho_pseudoXML $rho_isoXML $PlotSpinVec $spinvecXML $vec2XML $bsq_pseudoXML $bsq_isoXML $PlotBsq2rAsIso $PlotVelCustom $VelCustomFile $idx $totframes $view1XML $vol1XML $view2XML $vol2XML >> $jobfile
	frame_count=$((frame_count+1))
       	if [[ "$frame_count" -ge "$framesPerRun" ]]; then
        	frame_count=0
                job_num=$((job_num+1))
        fi
done

totjobs=$(ls $logfolder/job/* | wc -l)
templatefile=$root/bin/scheduler/multirun_template_riemann
for ((c=0; c<$totjobs; c++)); do
        runfile=$logfolder/run/run$c.sh
        cat $templatefile $logfolder/job/job$c.sh >> $runfile
        chmod +x $runfile
done

# riemann: no batch scheduler and no compute nodes -- run the job scripts here,
# $maxParallel at a time. Each job's stdout/stderr goes to run<c>.sh.out.
echo "running $totjobs jobs locally, $maxParallel at a time"
ls $logfolder/run/run*.sh | sort -V | \
        xargs -P $maxParallel -I{} bash -c 'bash "$1" > "$1".out 2>&1; echo "finished $(basename "$1")"' _ {}
echo " done"
cd $root

