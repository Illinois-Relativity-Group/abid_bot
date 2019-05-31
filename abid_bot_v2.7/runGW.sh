#!/bin/bash

. params

###### the type of wave to make
##(hcross or hplus)
kind="hcross"

all=false            #Runs all folders if true, if false will run from
firstVTKFolder=1       #   firstFolder to lastFolder.  Can be changed in
lastVTKFolder=10      #   the if-statement below
foldersPerRun=1     

# begin 

jobName=bhbh_disk_GW_"$kind"
GWdir=$root/gwdata/3D

########run movies variables
pbsfile=$root/bin/gw_code/makeGW_movie_batch.pbs
picsavedir=$root/movies
logdir=$root/log
schdir=$root/bin/scheduler
visitScript=$root/bin/gw_code/GW_up.py  #2D use GW_up.py 3D use GW_3D.py
#totranks=60
frameperrank=5
Stoptime=$( tail -1 $root/gwdata/time_list.txt )  #the t/m you want to stop the movie
totframes=$( awk -v stoptime="$Stoptime" 'BEGIN{FS="\n"}{if ($1>= stoptime){exit}}END{print NR}' $root/gwdata/time_list.txt )
echo "Number of frames: "$totframes
#totranks=$(( $totframes/$frameperrank +1 ))
totranks=5
echo "Number of ranks: "$totranks

### remove trailing '/'
picsavefolder=$(echo $picsavefolder | sed "s,/$,,")

###### make save folders
picsavefolder=$picsavedir/$kind'_'$(date +%y%m%d_%H%M)
mkdir -p $picsavefolder
echo $picsavefolder

###### make log folder
logfolder=$logdir/$kind'_'$(date +%y%m%d_%H%M)
mkdir -p $logfolder
cd $logfolder; 	mkdir -p $logfolder/joblist;	mkdir -p $logfolder/run;	mkdir -p $logfolder/job

count=1
jobcount=0

for dir in $(ls -d ${GWdir}"/"*); do
	tosave="$picsavefolder"/"$jobName"_$(printf -n ${count}p)
	if [ $all = true ] || [ $count -ge $firstVTKFolder -a $count -le $lastFolder ]; then
		for rank in `seq 0 $(( $totranks - 1 ))`; do
			jobfile=$logfolder/job/job$count"_"$rank.sh
			echo visit -cli -nowin -forceversion 2.7.3 -s $visitScript $kind $dir $tosave$(printf "%03d" $rank)"_" $rank $totranks $Stoptime $gw_dt $M > $jobfile
			echo $logfolder $jobfile >> $logfolder/joblist/joblist$((jobcount/foldersPerRun))
		done
		jobcount=$((jobcount+1))
	fi
	count=$((count+1))
done

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
