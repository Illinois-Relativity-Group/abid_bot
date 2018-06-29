cur=$PWD

if [ -z "$paramsSet" ]; then
	echo Set params!
	return 1
fi

echo "setting up particles"
rm -rf $root/seeds/
mkdir $root/seeds/

tracefolder=trace1/
rm -rf $root/$tracefolder/

if $particleSeeds
then
	particledir=$bin/particle_code
	rm -rf $particledir/seeds/
	mkdir $particledir/seeds/

	if $updateParticleMon
	then
		ln -s $root/h5data/particles.mon $particledir/misc/

		cd $particledir/misc/
		rm -rf $particledir/filesOrigin.txt
		rm -rf $particledir/misc/dat/
		./makeparts.awk $particledir/misc/
		rm *.mon

		rm -rf $particledir/misc/dat_shortened/
		mkdir $particledir/misc/dat_shortened/
		python dat_cut.py $root/ $firstTime $dt
		rm -rf $particledir/misc/dat/
		mv $particledir/misc/dat_shortened/ $particledir/misc/dat/
		cd $particledir/misc/dat/
		ls > $particledir/misc/files.txt
		cd $particledir/misc/

		if $extend
		then
			echo "	reflecting seed points"
			python extend.py $root/
			rm -rf $particledir/misc/dat/
			rm -rf $particledir/dat/
			mv $particledir/misc/extended/ $particledir/dat/
		else
			rm -rf $particledir/dat/
			mv $particledir/misc/dat/ $particledir/
		fi
	fi
	
	echo "	making particle seeds"
	cd $particledir
	python particlePicker.py $dt $firstTime $particledir/ $arg1 $arg2 $arg3 $arg4 txt

	cp seeds/* $root/seeds/
	module unload bwpy
	python $bin/rename_seeds.py $root/ $dt
fi

if false #$bhForms
then
	echo "	making grid seeds"
	cd $root/bin/grid_code/
	python seedmaker.py $root/ $dt 1
	targetdir=$root/seeds/
	if $twoColorsSeeds
	then
		mkdir $root/seeds/gridseeds/
		targetdir=$root/seeds/gridseeds/
	fi

	if $appendSeeds
	then
		cd bhseeds/
		for i in *
		do
			cat $i >> $root/seeds/$i
		done
	else
		cp bhseeds/* $targetdir
	fi

	if $binary
	then
		cd $root/bin/grid_code/
		python seedmaker.py $root/ $dt 2
		cd bhseeds/
		for i in *
		do
			cat $i >> $targetdir/$i
		done
	fi

	if $merged
	then
		cd $root/bin/grid_code/
		python seedmaker.py $root/ $dt 3
		cd bhseeds/
		for i in *
		do
			cat $i >> $targetdir/$i
		done
	fi
fi

if $particleTracer
then
	particledir=$bin/particle_code
	mkdir $root/$tracefolder/
	rm -rf $particledir/$tracefolder/
	mkdir $particledir/$tracefolder/

	if $updateParticleMon
	then
		ln -s $root/h5data/particles.mon $particledir/misc/

		cd $particledir/misc/
		./makeparts.awk $particledir/misc/
		rm *.mon

		rm -rf $particledir/misc/dat_shortened/
		mkdir $particledir/misc/dat_shortened/
		python dat_cut.py $root/ $firstTime $dt
		rm -rf $particledir/misc/dat/
		mv $particledir/misc/dat_shortened/ $particledir/misc/dat/
		cd $particledir/misc/dat/
		ls > $particledir/misc/files.txt
		cd $particledir/misc/

		if $extend
		then
			echo "	reflecting seed points"
			python extend.py $root/
			rm -rf $particledir/misc/dat/
			mv $particledir/misc/extended/ $particledir/dat/
		else
			mv $particledir/misc/dat/ $particledir/dat/
		fi
	fi
	
	echo "	making particle tracer"
	cd $particledir
	python particlePicker.py $dt $firstTime $particledir/ $arg1 $arg2 $arg3 $arg4 3d

	cp $tracefolder/* $root/$tracefolder/
	python $bin/rename_seeds.py $root/ $dt $tracefolder/
fi


cd $cur
echo "done"
