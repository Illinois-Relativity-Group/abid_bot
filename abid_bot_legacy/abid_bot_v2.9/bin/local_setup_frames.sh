echo "setting up frames"

cur=$PWD
cd $root/bin/bw_many_folder_scripts/
./local_cray.sh $it $root/h5data
python rmdupes.py $root/
. local_SetMovie.sh 
cd $cur
echo "done"
