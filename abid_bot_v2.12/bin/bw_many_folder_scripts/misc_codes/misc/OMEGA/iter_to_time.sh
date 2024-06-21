. params
#cp -r vel_data_iter vel_data
rm -r vel_data
mkdir vel_data
echo "Converting from iteration to time"
python bin/iter_to_time.py $dt $M $ini_time
echo "moving data..."
mv v*txt vel_data
echo "...done"

