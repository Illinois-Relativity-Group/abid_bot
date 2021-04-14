. params
#Split Ascii files
rm -r vel_data_iter
mkdir vel_data_iter
echo "Splitting vx..."
python bin/split.py $vxfile x $M $start_time $dt
echo "...done"
echo "Splitting vy..."
python bin/split.py $vyfile y $M $start_time $dt
echo "...done"
rm -r vel_data_iter_clean
mkdir vel_data_iter_clean

python bin/cleanvel.py
