#!/bin/bash
. params
#gw_dt=0.1 #gw_test
#gw_dt=0.432  #bbh
gw_dt=0.056325
#M=1.0
r_areal=70.013132761
#M=0.058298549469  #90 hydro??
#M=0.063640592586 #00 hydro
M=0.058298549469  #45 hydro
#wave_zone_r=10.0
wave_zone_r=5.0
###### the type of wave to make
##(hcross or hplus)
#kind="hcross"
kind="hplus"
all=true       #Runs all folders if true, if false will run from
firstVTKFolder=40       #   firstFolder to lastFolder.  Can be changed in
lastVTKFolder=40   #   the if-statement below
framesPerRun=300
totranks=25
templatefile=$root/multirun_template_anvil
# begin 
jobName=bhdisk_45_allmodes
GWdir=$root/gwdata/2D
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
                        echo visit -cli -nowin -s $visitScript $kind $dir $tosave$(printf "%03d" $rank)"_" $rank $totranks $gw_dt $M $wave_zone_r $r_areal >> $jobfile
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


