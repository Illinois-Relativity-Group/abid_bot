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

PlotGW2D=${29} 
PlotGW3D=${30}

PlotShapeCustom=${31}
ShapeCustomFile=${32}
gw3D_volXML=${33}

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
	
	
	echo visit -forceversion 3.1.4 -cli -nowin -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $xmldir $picsavefolder$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $g00_pseudoXML $g00_isoXML $maxdensity $rho_pseudoXML $rho_isoXML $PlotSpinVec $spinvecXML $vec2XML $bsq_pseudoXML $bsq_isoXML $PlotBsq2rAsIso $PlotVelCustom $VelCustomFile $PlotGW2D $PlotGW3D $PlotShapeCustom $ShapeCustomFile $gw3D_volXML $idx $totframes $view1XML $vol1XML $view2XML $vol2XML >> $jobfile
	frame_count=$((frame_count+1))
       	if [[ "$frame_count" -ge "$framesPerRun" ]]; then
        	frame_count=0
                job_num=$((job_num+1))
        fi
done

totjobs=$(ls $logfolder/job/* | wc -l)
templatefile=$root/bin/scheduler/multirun_template_anvil
for ((c=0; c<$totjobs; c++)); do
		# . job$c.sh
        runfile=$logfolder/run/run$c.sh
        cat $templatefile $logfolder/job/job$c.sh >> $logfolder/run/run$c.sh
        echo "submitting job $c"
        sbatch $logfolder/run/run$c.sh
done
echo " done"
cd $root

