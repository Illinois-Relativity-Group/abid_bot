#This WILL RUN EVEYRHTINGSDFSDFSDFSDFs

#####begin things you have to change TODO

jobName=nsns
h5dir=/u/sciteam/skhan/scratch/NSNS/nsns
extrasDir=/u/sciteam/skhan/scratch/NSNS/nsns_extras/xml/ #TODO make this folder
h5prefix=3d_data_

#######seq variables

examplefilename=Bx.file_0.h5
cycle=256

######setXML variables

setxmlpbsfile=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/setXMLwargs.pbs
setxmlscript=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/set_xml_wargs.py
particledir=/u/sciteam/skhan/scratch/NSNS/nsns_extras/seeds
bhfulldata=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bhdata

########run movies variables

manypbsfile=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/manyFoldersSubwranks.pbs
picsavedir=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/movies
visitScript=/u/sciteam/skhan/scratch/NSNS/nsns_extras/bw_many_folder_scripts/run_movie_ranks.py
totranks=1

#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
savefolder=$( echo $savefolder | sed "s,/$,,")
picsavefolder=$( echo $picsavefolder | sed "s,/$,,")


echo running script that gives overlap.txt...

module load cray-hdf5

echo ./movieSeq_v2_arg.bash -i $cycle -r $h5dir -p $h5prefix -n $examplefilename -f

# finds overlaps in the h5 files
./movieSeq_v2_arg.bash -i $cycle -r $h5dir -p $h5prefix -n $examplefilename -f

echo ...done

#########This submits the setXML

rm $extrasDir/$h5prefix*/*
echo files in $extrasDir/$h5prefix*/* deleted

##########This section submits the rest of the files.
##########The files submitted here will not run until setxml completes

count=1

picsavefolder=$picsavedir/$(date +%y%m%d_%H%M)

echo mkdir -p $picsavefolder
mkdir -p $picsavefolder

for dir in $(ls -d ${h5dir}"/"$h5prefix* )
do

    blah=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 

    tosave="$picsavefolder"/movie_$(printf "%03d" $count)_

    #This should only submit the first time the loop runs
    #This submits the xml_go job
    #The other jobs won't run until this one finishes
    if [[ $count -eq 1 ]]
    then
	echo qsub -N $jobName"_xml_go" -v VISITSCRIPT=$setxmlscript,H5=$dir,OVERLAP=$PWD"/overlap.txt",BH=$bhfulldata,PARTICLESEED=$particledir $setxmlpbsfile

        xmlsub=`qsub -N $jobName"_xml_go" -v VISITSCRIPT=$setxmlscript,H5=$dir,OVERLAP=$PWD"/overlap.txt",BH=$bhfulldata,PARTICLESEED=$particledir $setxmlpbsfile`
        echo "submited " $xmlsub
    
        for rank in `seq 0 $(( $totranks - 1 ))`;
        do
            echo submitting job $count with rank = $rank

            echo qsub -W depend=afterany:$xmlsub -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",BH=$blah,RANK=$rank,TOTRANKS=$totranks $manypbsfila

            firstrun=`qsub -W depend=afterany:$xmlsub -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",BH=$blah,RANK=$rank,TOTRANKS=$totranks $manypbsfile`

        done

    else
        for rank in `seq 0 $(( $totranks - 1 ))`;
        do
            echo submitting job $count with rank = $rank

            echo qsub -W depend=after:$firstrun -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",BH=$blah,RANK=$rank,TOTRANKS=$totranks $manypbsfila

            qsub -W depend=after:$firstrun -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",BH=$blah,RANK=$rank,TOTRANKS=$totranks $manypbsfile

        done

    fi
    count=$((count+1))

done
