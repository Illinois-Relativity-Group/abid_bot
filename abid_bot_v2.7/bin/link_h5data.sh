if [[ $(pwd) != $root* || -z "$root" ]]; then
    echo Set params!
    return 1
fi

#full path to actual data
origin="/u/sciteam/ruiz1/scratch/Antonios/Spin_NSNS/med/Magnetized/spHd2.5_K123.6_131_mcor/beta100/"
#full path to h5dir and bh data
h5dest=$root/h5data/
bhdest=$root/horizon/all_horizon/

for i in $(ls -d $origin/3d* | xargs -n 1 basename); do #just file name no path
	if [ ! -d $h5dest/$i ]; then 
		echo Linking $i
		ln -s $origin/$i $h5dest
	fi
done

for i in $(ls $origin/h.t*.gp | xargs -n 1 basename); do
    if [ ! -f $bhdest/$i ]; then
        echo Linking $i
        ln -s $origin/$i $bhdest/
    fi
done
