. params
#Use this if you are submitting very few folders (~1-5)
#Otherwise use runBundle.sh
#####begin things you have to change TODO

jobName=bhbh_fields
h5dir=$root/h5data
extrasDir=$root/xml
h5prefix=3d_data_

########run movies variables

pbsfile=$root/bin/bw_many_folder_scripts/singleRun.pbs
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/run_movie_ranks.py
totranks=5
#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
savefolder=$( echo $savefolder | sed "s,/$,,")
picsavefolder=$( echo $picsavefolder | sed "s,/$,,")


##########This section submits the rest of the files.

count=1
DATE=$(date +%y%m%d_%H%M)
picsavefolder=$picsavedir/"$DATE"_"$jobName"; mkdir -p $picsavefolder
logfolder=$logdir/"$DATE"_"$jobName";         mkdir -p $logfolder

cd $logfolder

for dir in $(ls -d ${h5dir}"/"$h5prefix* )
do
    blah=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
    tosave="$picsavefolder"/"$jobName"_$(printf "%03d" $count)_

if [ $count -eq 1 ]
then
    for rank in `seq 0 $(( $totranks - 1 ))`;
    do
            echo submitting job $count with rank = $rank
            qsub -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",RANK=$rank,TOTRANKS=$totranks,STREAMXML=$streamXML,VECXML=$vecXML,BSQXML=$bsqXML,MAXDENS=$maxdensity $pbsfile
    done
fi
    count=$((count+1))
done

cd $root
