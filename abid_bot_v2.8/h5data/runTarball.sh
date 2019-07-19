
jobName=tarball
folders_per_job=5
pbsfile=tarball.pbs
tot=$(ls -d 3d* | wc -l)
DATE=$(date +%y%m%d_%H%M)
[ -d tar ] && rm -r tar
mkdir tar
for ((i=1; i<=tot; i+=folders_per_job))
do
    qsub -N $jobName"_"$i -v end=$((i+folders_per_job-1)),num=$folders_per_job $pbsfile 
done

