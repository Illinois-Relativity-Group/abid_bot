#####begin things you have to change TODO

jobName=nsns_fields
h5dir=/u/sciteam/skhan/scratch/NSNS/nsns
extrasDir=/u/sciteam/skhan/scratch/NSNS/nsns_extras/xml/ #TODO make this folder
h5prefix=3d_data_

#######seq variables

examplefilename=Bx.file_0.h5
cycle=256

########run movies variables

manypbsfile=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/manyFoldersSubwranks2.pbs
picsavedir=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/clips
visitScript=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/run_frames_ranks.py
totranks=2

FolderDir=$1
reqrank=$2
subrank=$3

#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
savefolder=$( echo $savefolder | sed "s,/$,,")
picsavefolder=$( echo $picsavefolder | sed "s,/$,,")

#echo running script that gives overlap.txt...
#module load cray-hdf5
#./movieSeq_v2_arg.bash -i $cycle -r $h5dir -p $h5prefix -n $examplefilename -f
#echo ...done

##########This section submits the rest of the files.

count=1
picsavefolder=$picsavedir/$(date +%y%m%d_%H%M)
mkdir -p $picsavefolder

for dir in $(ls -d ${h5dir}"/"$h5prefix* )
do
if [ "$count" -eq "$FolderDir" ]
then
    blah=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
    tosave="$picsavefolder"/movie_$(printf "%03d" $count)_

    for rank in `seq 0 $(( $totranks - 1 ))`;
    do
    if [ "$rank" -eq "$reqrank" ]
    then
            echo submitting job $count with rank = $rank
            qsub -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",BH=$blah,RANK=$rank,TOTRANKS=$totranks,IDX=$subrank $manypbsfile
    fi
    done
fi
    count=$((count+1))
done
