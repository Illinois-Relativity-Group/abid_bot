. params
#cp -r w_data_iter vel_data
#rm -r w_data
mkdir w_data
echo "Converting from iteration to time"
python bin/iter_to_time.py $dt $M $ini_time
echo "moving data..."
mv w*txt w_data
echo "...done"

