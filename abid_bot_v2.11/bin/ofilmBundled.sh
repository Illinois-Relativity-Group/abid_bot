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
PlotVel= 0  #${11} # Plot velocity arrows
PlotBsq2r=${12} # Plot B squared over 2 rho
Plotg00=${13} # Plot g00 from metric
refPlot=${14} # Reflect plot over xy plane
cutPlot=${15} # only show back half (y>0), needs view like: (0,-x,y)
bgcolor=${16} #background color
PlotZoom=${17}
PlotFlyOver=${18}
PlotFlyAround=${19}

PlotEvolve=0

view1XML=${20} #Overwrite view1XML, vol1XMl, view2XML, vol2XML
vol1XML=${21}
view2XML=${22}
vol2XML=${23}

PlotSpinVec=${24}
spinvecXML=${25}

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

framesPerRun=20
frame_count=0
job_num=0
for rank in `seq 0 $(( $totranks - 1 ))`; do
	jobfile=$logfolder/job/job$job_num.sh
	echo visit -forceversion 3.1.4 -cli -nowin -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $xmldir $picsavefolder$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML $PlotSpinVec $spinvecXML $idx $totframes $view1XML $vol1XML $view2XML $vol2XML $vec2XML $bsq_pseudoXML $bsq_isoXML >> $jobfile
	frame_count=$((frame_count+1))
       	if [[ "$frame_count" -ge "$framesPerRun" ]]; then
        	frame_count=0
                job_num=$((job_num+1))
        fi
done

totjobs=$(ls $logfolder/job/* | wc -l)
templatefile=$root/bin/scheduler/multirun_template_anvil
for ((c=0; c<$totjobs; c++)); do
        runfile=$logfolder/run/run$c.sh
        cat $templatefile $logfolder/job/job$c.sh >> $logfolder/run/run$c.sh
        echo "submitting job $c"
        sbatch $logfolder/run/run$c.sh
done
echo " done"
cd $root

