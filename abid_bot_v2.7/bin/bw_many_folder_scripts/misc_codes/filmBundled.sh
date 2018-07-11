cur=$(pwd)

#####begin things you have to change TODO

root=$1
misc=$root/bin/bw_many_folder_scripts/misc_codes
jobName=$2
joblistID=$3
h5dir=$root/h5data/$4
idx=$5
extrasdir=$root/xml/$4
picsavedir=$6
pyscript=$7

########set parameters

cd $root
. params
cd $cur

########run movies variables
logdir=$misc/logs
visitScript=$misc/${pyscript}
totranks=50
ranksPerJob=10 # divisor of totranks
#####end things you have to change

#Overwrite the view1XML and view2XML
#You need to pass $8 and $9 from run_zooms_and_rots.sh

if [ -z "$8" ]
then
	echo Using viewXML from params
elif [ -z "$9" ]
then
	echo Warning: Only one view xml is specified. The code will use viewXML from params instead.
else
	echo Zooming from $8 to $9 ...
	view1XML=$8
	view2XML=$9
fi

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
picsavedir=$( echo $picsavedir | sed "s,/$,,")

#scheduler

schdir=$root/bin/scheduler
numjobs=$(($totranks+1))
numnodes=$(($numjobs/2+2))

##########This section submits the rest of the files.

picsavefolder=$picsavedir\_$(date +%y%m%d_%H%M);	mkdir -p $picsavefolder
picsavefolder=$picsavefolder/$jobName\_

logfolder=$logdir/$jobName"_"$(date +%y%m%d_%H%M);	mkdir -p $logfolder
cd $logfolder; 	mkdir -p $logfolder/joblist;		mkdir -p $logfolder/run;	mkdir -p $logfolder/job

for rank in `seq 0 $(( $totranks - 1 ))`
do
	jobfile=$logfolder/job/job_$joblistID$(printf "_%03d" $rank).sh
	echo visit -forceversion 2.7.3 -cli -nowin -s $visitScript $rank $totranks $picsavefolder $root $h5dir $extrasdir $streamXML $vecXML $maxdensity $idx $view1XML $view2XML > $jobfile
	echo $logfolder $jobfile >> $logfolder/joblist/joblist$((rank/ranksPerJob))
done

chmod -R 755 $logfolder/job
tasksPerJob=$((ranksPerJob+1))
nodesPerJob=$(((tasksPerJob+1)/2))
for i in `seq 0 $((totranks/ranksPerJob-1))`;
do
	cat $schdir/run_template | sed 's,NUMBER_OF_NODES,'"$nodesPerJob"',g;
									s,TOTAL_JOBS,'"$tasksPerJob"',g;
									s,LOG_DIR,'"$logfolder"',g;
									s,SCH_DIR,'"$schdir"',g;
									s,JOBLIST,joblist/joblist'"$i"',g;
									s,JOBNAME,'"$jobName\_$i"',g' > $logfolder/run/run$i
	echo qsub $logfolder/run/run$i
done
echo Done!

cd $cur
