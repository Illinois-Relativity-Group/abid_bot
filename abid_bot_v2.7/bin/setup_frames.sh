echo "setting up frames"

if [[ $(pwd) != $root* || -z "$root" ]]; then
    echo Set params!
    return 1
fi

cur=$PWD
cd $root/bin/bw_many_folder_scripts/
./cray.sh $it $root/h5data
python rmdupes.py $root/
. SetMovie.sh 
cd $cur
echo "done"
