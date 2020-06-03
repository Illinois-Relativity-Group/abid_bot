. ../params
cur=$PWD

jobName=make_g00
h5dir=$root/h5data
h5prefix=3d_data_

pbsfile=$root/bin/bw_many_folder_scripts/g00Run_nasa.pbs
python_file=$root/bin/make_g00_bw.py
logdir=$root/log

foldersperjob=3
totfolders=$(ls -d ${h5dir}/$h5prefix* | wc -l)

DATE=$(date +%y%m%d_%H%M)
logfolder=$logdir/"$DATE"_"$jobName";         mkdir -p $logfolder

cd $logfolder

counter=1
temp_str=""
for dir in $(ls -d ${h5dir}/$h5prefix*);
do
	if [ $(($counter % $foldersperjob)) != 0 ]; then
		temp_str="$temp_str+$dir"
		counter=$(($counter+1))
	elif [ $(($counter % $foldersperjob)) == 0 ] || [ $counter == $totfolders ]; then
		temp_str="$temp_str+$dir"
		echo making g00 with $foldersperjob folders per job
		qsub -N $jobName"_"$counter -v G00SCRIPT=$python_file,DIR_STR=$temp_str $pbsfile
		temp_str=""
		counter=$(($counter+1))
	fi
done

cd $cur
