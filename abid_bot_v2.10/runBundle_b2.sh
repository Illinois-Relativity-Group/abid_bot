. params

#option to reduce number of folders images
all=false 			#Runs all folders if true, if false will run from
firstFolder=1		#	firstFolder to lastFolder.  Can be changed in
lastFolder=1		#	the if-statement below
foldersPerRun=1		#Larger numbers take longer to launch but are preferred by BW
					#Set to 1 for fastest queue times, ~10 is a good amount
#foldersPerRun=$(ls -d h5data/3d_data_* | wc -l) # Submits all folders in one job.  Long time in queue


#job name and directory info
jobName=batchtest
h5dir=$root/h5data
extrasDir=$root/xml
h5prefix=3d_data_
#run movie variables
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/run.py
totranks=16

#plotting varibles
PlotDensAsVol=1 # Plot density in a volume plot
PlotDensAsIso=0 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotBsq2r=0 # Plot B squared over 2 rho
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="blue" #background color

PlotEvolve=1
PlotZoom=0
PlotFlyOver=0
PlotFlyAround=0

#scheduler variables
schdir=$root/bin/scheduler
if [ $all = false ]; then
	echo Submitting $((lastFolder-firstFolder+1)) folders
else
	echo Submitting all folders
fi

#set up directories
count=1 #nth folder
jobcount=0 #nth submitted folder
DATE=$(date +%y%m%d_%H%M); echo $DATE
picsavefolder=$picsavedir/"$DATE"_"$jobName"; mkdir -p $picsavefolder
logfolder=$logdir/"$DATE"_"$jobName";		 mkdir -p $logfolder
cd $logfolder
	mkdir -p $logfolder/joblist
	mkdir -p $logfolder/run
	mkdir -p $logfolder/job
	mkdir -p $logfolder/out
echo "Writing jobs to joblist..."

#loop over 3d_data folders
###Consider writing joblist and run files to log directory instead of scheduler directory
for dir in $(ls -d ${h5dir}"/"$h5prefix* ); do
	xmldir=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
	tosave="$picsavefolder"/"$jobName"_$(printf "%03d" $count)_
	#if [ $((count%20)) -eq 0 ]; then 		#Image every 20th folder
	if [ $all = true ] || [ $count -ge $firstFolder -a $count -le $lastFolder ]; then
		#loop over ranks within 3d_data folder
		for rank in `seq 0 $(( $totranks - 1 ))`; do
			#create job script for folder and rank; add to joblist
			jobfile=$logfolder/job/job$count"_"$rank.sh
			outfile=$logfolder/out/out$count"_"$rank
			echo visit -cli -nowin -forceversion 3.1.2 -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2r $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $xmldir $tosave$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML > $jobfile
			echo "$jobfile >> $outfile" >> $logfolder/joblist/joblist$((jobcount/foldersPerRun))
		done
		jobcount=$((jobcount+1))
	fi
	count=$((count+1))
done

#finish job setup; create run script
chmod -R 777 $logfolder/job
jobcount=$((jobcount-1))
runcount=$((jobcount/foldersPerRun))
numjobs=$(((foldersPerRun*totranks+1)))
numnodes=$(((numjobs+1)/2))
for i in `seq 0 $runcount`; do
	touch $logfolder/joblist/looper$i.sh
	loopfile=$logfolder/joblist/looper$i.sh
	cat $schdir/job_template_b2 | sed 's, LOG_DIR, '"$logfolder"',g;
					s,JOBLIST,joblist/joblist'"$i"',g'> $loopfile
	chmod 777 $loopfile
	chmod 777 $logfolder/joblist/joblist$i
	loopfile2=$logfolder/joblist/looper$i.sh
	cat $schdir/run_template_b2 | sed 's,JOBNAME,'"$jobName"'_'"$i"',g;
									s,NUMBER_OF_NODES,'"$numnodes"',g;
									s,TOTAL_JOBS,'"$numjobs"',g;
									s,SCH_DIR,'"$schdir"',g;
									s,LOG_DIR,'"$logfolder"',g;
									s,JOBLIST,joblist/joblist'"$i"',g;
									s,LOOPER,'"$loopfile2"',g;
									s,NTASKS,'"$totranks"',g;
									s,NUM,'"$i"',g' > $logfolder/run/run$i
	#Submit job
	echo "    Submitting job $i"
	chmod -R 777 $logfolder
	sbatch $logfolder/run/run$i
done
echo "$runcount"
echo "$numjobs"
echo "$numnodes"
echo "    ...Done!"

cd $root
