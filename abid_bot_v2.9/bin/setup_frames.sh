echo "setting up frames"

cur=$PWD
cd $root/bin/bw_many_folder_scripts/
./cray.sh $it $root/h5data
python rmdupes.py $root/
. SetMovie.sh 
cd $cur
echo "done"
