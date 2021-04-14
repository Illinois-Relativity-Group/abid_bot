. params
rm -r w_data
mkdir w_data
rm err.log
touch err.log
echo "Creating w data..."
python bin/vel_to_omega.py $delta_r $M $ini_time $start_time
echo "...done"

