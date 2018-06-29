. params

#option to reduce number of folders images
all=false 			#Runs all folders if true, if false will run from
firstFolder=1		#	firstFolder to lastFolder.  Can be changed in
lastFolder=100		#	the if-statement below
foldersPerRun=5		#Larger numbers take longer to launch but are preferred by BW
					#Set to 1 for fastest queue times, ~10 is a good amount
#foldersPerRun=$(ls -d h5data/3d_data_* | wc -l) # Submits all folders in one job.  Long time in queue


#job name and directory info
jobName=BHNS6
h5dir=$root/h5data
extrasDir=$root/xml
h5prefix=3d_data_
#run movie variables
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/run_movie_ranks.py
totranks=5

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
picsavefolder=$picsavedir/$(date +%y%m%d_%H%M); mkdir -p $picsavefolder
logfolder=$logdir/$(date +%y%m%d_%H%M); 		mkdir -p $logfolder
cd $logfolder;	mkdir -p $logfolder/joblist;	mkdir -p $logfolder/run;	mkdir -p $logfolder/job
echo "Writing jobs to joblist..."

#loop over 3d_data folders
###Consider writing joblist and run files to log directory instead of scheduler directory
for dir in $(ls -d ${h5dir}"/"$h5prefix* ); do
	xmldir=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
	tosave="$picsavefolder"/movie_$(printf "%03d" $count)_
	#if [ $((count%20)) -eq 0 ]; then 		#Image every 20th folder
	if [ $all = true ] || [ $count -ge $firstFolder -a $count -le $lastFolder ]; then
		#loop over ranks within 3d_data folder
		for rank in `seq 0 $(( $totranks - 1 ))`; do
			#create job script for folder and rank; add to joblist
			jobfile=$logfolder/job/job$count"_"$rank.sh
			echo visit -cli -nowin -forceversion 2.7.3 -s $visitScript $dir $xmldir $tosave$(printf "%03d" $rank)"_" $rank $totranks $streamXML $vecXML $maxdensity > $jobfile
			echo $logfolder $jobfile >> $logfolder/joblist/joblist$((jobcount/foldersPerRun))
		done
		jobcount=$((jobcount+1))
	fi
	count=$((count+1))
done

#finish job setup; create run script
chmod -R 755 $logfolder/job
jobcount=$((jobcount-1))
runcount=$((jobcount/foldersPerRun))
numjobs=$(((foldersPerRun*totranks+1)))
numnodes=$(((numjobs+1)/2))
for i in `seq 0 $runcount`; do
	cat $schdir/run_template | sed 's,JOBNAME,'"$jobName"'_'"$i"',g;
									s,NUMBER_OF_NODES,'"$numnodes"',g;
									s,TOTAL_JOBS,'"$numjobs"',g;
									s,SCH_DIR,'"$schdir"',g;
									s,LOG_DIR,'"$logfolder"',g;
									s,JOBLIST,joblist/joblist'"$i"',g' > $logfolder/run/run$i
	#Submit job
	echo "    Submitting job $i"
	qsub $logfolder/run/run$i
done
echo "    ...Done!"

cd $root
