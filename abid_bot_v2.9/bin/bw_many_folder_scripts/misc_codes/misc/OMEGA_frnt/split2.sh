. params
#Split Ascii files
rm -r vel_data_iter2
mkdir vel_data_iter2
echo "Splitting vx..."
python bin/split2.py $vxfile x $M $start_time $dt
echo "...done"
echo "Splitting vy..."
python bin/split2.py $vyfile y $M $start_time $dt
echo "...done"
rm -r vel_data_iter_clean2
mkdir vel_data_iter_clean2

python bin/cleanvel2.py
