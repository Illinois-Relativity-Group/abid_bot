. params
#Time average over nearby files
echo
if [ -e t_ave ]
	then
	rm -rf t_ave
fi
mkdir t_ave

echo "Time averaging..."
python bin/new_time_ave.py $dt $comp_omega_mode $M $ini_time $ini_omega
echo "...done"

