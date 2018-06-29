#!/bin/bash

. params

###### the type of wave to make
##(hcross or hplus)
kind="hcross"

# begin 

jobName=bhbh_disk_GW_"$kind"
GWdir=$root/gwdata/less_3D

########run movies variables

pbsfile=$root/bin/gw_code/makeGW_movie.pbs
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/gw_code/GW_up.py  #2D use GW_up.py 3D use GW_3D.py
#totranks=60
frameperrank=5
Stoptime=$( tail -1 $root/gwdata/time_list.txt )  #the t/m you want to stop the movie
totframes=$( awk -v stoptime="$Stoptime" 'BEGIN{FS="\n"}{if ($1>= stoptime){exit}}END{print NR}' $root/gwdata/time_list.txt )
echo "Number of frames: "$totframes
totranks=$(( $totframes/$frameperrank +1 ))

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
echo $logfolder

cd $logfolder

#for rank in `seq 0 $(( 2 ))`;
for rank in `seq 0 $(( $totranks - 1 ))`;
do
	tosave="$picsavefolder"/movie_$(printf "%03d" $rank)   #For 3D use this line
	#tosave="$picsavefolder"/movie                           #For 2D use this line
	echo submitting job with rank = $rank out of $(( $totranks - 1 ))
	qsub -N $jobName"_"$rank -v VISITSCRIPT=$visitScript,KIND=$kind,GWDIR=$GWdir,SAVEFOLDER=$tosave"_",RANK=$rank,TOTRANKS=$totranks,STOPTIME=$Stoptime,GWDT=$gw_dt,MASS=$M $pbsfile
done

cd $root
