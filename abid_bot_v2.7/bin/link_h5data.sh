if [[ $(pwd) != $root* || -z "$root" ]]; then
    echo Set params!
    return 1
fi

#full path to actual data
origin="/u/sciteam/ruiz1/scratch/Antonios/Spin_NSNS/med/Magnetized/spHd2.5_K123.6_131_mcor/beta100/"
#full path to h5dir
dest=$root/h5data/ 

for i in $(ls -d $origin/3d* | xargs -n 1 basename); do #just file name no path
	if [ ! -d $dest/$i ]; then 
		echo Linking $i
		ln -s $origin/$i $dest
	fi
done
