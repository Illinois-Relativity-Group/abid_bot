#!/bin/bash
module unload impi
module load hdf5

s=$1		#start
e=$2		#end
numjobs=0	#number of jobs, from 0 to numjobs-1
fpj=100		#FramePerJob

#if [$((e-s>fpj))]
#then
numjobs=$(((e-s-1)/fpj))
#fi
echo $numjobs
for i in `seq 0 $numjobs`
do
	echo jobnum $i,from $((s+fpj*i)),to $((s+fpj*(i+1)>e ? e : s+fpj*(i+1)))
	
	sbatch --job-name="b2_rho"$i --export=ALL,start=$((s+fpj*i)),end=$((s+fpj*(i+1)>e ? e : s+fpj*(i+1))) job_submit_frontera.pbs
	#qsub -N b2_rho_$i -v IDX=$i job_submit.pbs 
done
