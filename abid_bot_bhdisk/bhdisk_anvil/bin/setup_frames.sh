echo "setting up frames"

cur=$PWD
cd $root/bin/bw_many_folder_scripts/
./cray.sh $it $root/h5data
python3 rmdupes.py $root/
. SetMovie.sh $1
cd $cur
echo "done"
