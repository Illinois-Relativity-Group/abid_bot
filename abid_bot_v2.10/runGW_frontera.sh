#!/bin/bash

. params

###### the type of wave to make
##(hcross or hplus)
kind="hcross"

all=false          #Runs all folders if true, if false will run from
firstVTKFolder=1       #   firstFolder to lastFolder.  Can be changed in
lastVTKFolder=3      #   the if-statement below
foldersPerRun=3     

# begin 

jobName=GW_test_"$kind"
GWdir=$root/gwdata/3D
DATE=$(date +%y%m%d_%H%M); echo $DATE

########run movies variables
#pbsfile=$root/bin/gw_code/makeGW_movie_frontera.pbs	#unused
picsavedir=$root/movies
logdir=$root/log
schdir=$root/bin/scheduler
visitScript=$root/bin/gw_code/GW_up_frontera.py  #2D use GW_up.py 3D use GW_3D.py
totranks=5

echo "Number of ranks: "$totranks

### remove trailing '/'
picsavefolder=$(echo $picsavefolder | sed "s,/$,,")

###### make save folders
picsavefolder=$picsavedir/"$DATE"_"$kind"_"$jobName"
mkdir -p $picsavefolder
echo $picsavefolder

###### make log folder
logfolder=$logdir/"$DATE"_"$kind"_"$jobName"
mkdir -p $logfolder
cd $logfolder
	mkdir -p $logfolder/joblist
	mkdir -p $logfolder/run
	mkdir -p $logfolder/job
	mkdir -p $logfolder/out

count=1
jobcount=0

for dir in $(ls -d ${GWdir}"/"*); do
	tosave="$picsavefolder"/"$jobName"_$(printf "%04d" ${count})_
	if [ $all = true ] || [ $count -ge $firstVTKFolder -a $count -le $lastVTKFolder ]; then
		for rank in `seq 0 $(( $totranks - 1 ))`; do
			jobfile=$logfolder/job/job$count"_"$rank.sh
			outfile=$logfolder/out/out$count"_"$rank
			echo visit -cli -nowin -forceversion 3.1.2 -s $visitScript $kind $dir $tosave$(printf "%03d" $rank)"_" $rank $totranks $gw_dt $M > $jobfile #$Stoptime
			echo "$jobfile >> $outfile" >> $logfolder/joblist/joblist$((jobcount/foldersPerRun))
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
    touch $logfolder/joblist/looper$i.sh
    loopfile=$logfolder/joblist/looper$i.sh
    cat $schdir/job_template | sed 's, LOG_DIR, '"$logfolder"',g;
                                        s,JOBLIST,joblist/joblist'"$i"',g'> $loopfile
    chmod 777 $loopfile
    chmod 777 $logfolder/joblist/joblist$i
    loopfile2=$logfolder/joblist/looper$i.sh
    cat $schdir/run_template_frontera | sed 's,JOBNAME,'"$jobName"'_'"$i"',g;
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
    sbatch $logfolder/run/run$i
done
echo "    ...Done!"

cd $root
