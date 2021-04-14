#Will remove all directories
#Move images if you want to keep them

for i in {png_ave, t_ave, w_data, vel_data}
	do
	if [ -e $i ]
	then
		rm -rf $i
	fi
done
