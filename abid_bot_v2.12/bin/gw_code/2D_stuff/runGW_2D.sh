#!/bin/bash
#gw_dt=0.1 #gw_test
root=/anvil/scratch/x-rnarasimhan/gw_bot/2D_stuff
gw_dt=0.432  #bbh
M=1.0
wave_zone_r=5.0
###### the type of wave to make
##(hcross or hplus)
#kind="hcross"
kind="hplus"
all=true       #Runs all folders if true, if false will run from
firstVTKFolder=100       #   firstFolder to lastFolder.  Can be changed in
lastVTKFolder=110   #   the if-statement below
framesPerRun=100
totranks=25
templatefile=$root/multirun_template_anvil
# begin 
jobName=hp_ring_pulsate_2D
GWdir=$root/gwdata_ring_pulsate/2D
DATE=$(date +%y%m%d_%H%M); echo $DATE
########run movies variables
#pbsfile=$root/bin/gw_code/makeGW_movie_frontera.pbs    #unused
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/GW_2D_run.py  #2D use GW_up.py 3D use GW_3D.py
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
        mkdir -p $logfolder/run
        mkdir -p $logfolder/job
        mkdir -p $logfolder/out

count=1
job_num=0
frame_count=0



for dir in $(ls -d ${GWdir}"/"* ); do
        if [ $all = true ] || [ $count -ge $firstVTKFolder -a $count -le $lastVTKFolder ]; then
                tosave="$picsavefolder"/"$jobName"_$(printf "%03d" $count)_
                for rank in `seq 0 $(( $totranks - 1 ))`; do
                        jobfile=$logfolder/job/job$job_num.sh
                        echo visit -cli -nowin -s $visitScript $kind $dir $tosave$(printf "%03d
" $rank)"_" $rank $totranks $gw_dt $M $wave_zone_r >> $jobfile
                        frame_count=$((frame_count+1))
                        if [[ "$frame_count" -ge "$framesPerRun" ]]; then
                                frame_count=0
                                job_num=$((job_num+1))
                        fi
                done
        fi
    count=$((count+1))
done

totjobs=$(ls $logfolder/job/* | wc -l)
for ((c=0; c<$totjobs; c++)); do
        runfile=$logfolder/run/run$c.sh
        cat $templatefile $logfolder/job/job$c.sh >> $logfolder/run/run$c.sh
        echo "submitting job $c"
        sbatch $logfolder/run/run$c.sh
done
echo "    ...Done!"
cd $root


