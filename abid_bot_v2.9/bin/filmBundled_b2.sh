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

########run movies variables
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/${pyscript}
totranks=$(((totframes+1)/2))
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

for rank in `seq 0 $(( $totranks - 1 ))`; do
	jobfile=$logfolder/job/job_$(printf "%03d" $rank).sh
	outfile=$logfolder/out/out_$(printf "%03d" $rank).txt
	echo visit -forceversion 3.0.0 -cli -nowin -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $xmldir $picsavefolder$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML $idx $totframes $view1XML $vol1XML $view2XML $vol2XML> $jobfile
	echo "$jobfile >> $outfile" >> $logfolder/joblist/joblist$((rank/ranksPerJob))
done

chmod -R 755 $logfolder/job
tasksPerJob=$((ranksPerJob+1))
nodesPerJob=$(((tasksPerJob+1)/2))
for i in `seq 0 $((totranks/ranksPerJob-1))`; do
	touch $logfolder/joblist/looper$i.sh
    loopfile=$logfolder/joblist/looper$i.sh
    cat $schdir/job_template_b2 | sed 's, LOG_DIR, '"$logfolder"',g;
                    s,JOBLIST,joblist/joblist'"$i"',g'> $loopfile
    chmod 777 $loopfile
    chmod 777 $logfolder/joblist/joblist$i
    loopfile2=$logfolder/joblist/looper$i.sh
	cat $schdir/run_template_b2 | sed 's,JOBNAME,'"$jobName"'_'"$i"',g;
									s,NUMBER_OF_NODES,'"$nodesPerJob"',g;
									s,TOTAL_JOBS,'"$tasksPerJob"',g;
									s,SCH_DIR,'"$schdir"',g;
									s,LOG_DIR,'"$logfolder"',g;
									s,JOBLIST,joblist/joblist'"$i"',g;
									s,LOOPER,'"$loopfile2"',g;
									s,NUM,'"$i"',g' > $logfolder/run/run$i
	qsub $logfolder/run/run$i
done
echo Done!

cd $cur
