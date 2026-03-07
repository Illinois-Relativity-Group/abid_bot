cd xml
for f in 3d_data*
do
	cd $f
        for f2 in grid_seeds_0*
	do
	cp ../3d_data_202301280112/grid_seeds_0_0000.txt  $f2
	done

	for f3 in grid_seeds_1*
	do
	cp ../3d_data_202301280112/grid_seeds_1_0000.txt  $f3
	done
	
	cd ..	
done
cd ..
