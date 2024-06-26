cur=$PWD

echo "setting up particles"
rm -rf $root/seeds/
mkdir $root/seeds/
chmod 770 $root/seeds/

tracefolder=trace1/
tracefolder2=trace2/
rm -rf $root/$tracefolder/
rm -rf $root/$tracefolder2/

if $particleSeeds
then
	particledir=$bin/particle_code
	rm -rf $particledir/seeds/
	mkdir $particledir/seeds/
	chmod 770 $particledir/seeds/

	if $updateParticleMon
	then
		ln -s $root/h5data/particles.mon $particledir/misc/

		cd $particledir/misc/
		rm -rf $particledir/filesOrigin.txt
		rm -rf $particledir/misc/dat/
		chmod 770 makeparts.awk  
		./makeparts.awk $particledir/misc/
		rm *.mon

		rm -rf $particledir/misc/dat_shortened/
		mkdir $particledir/misc/dat_shortened/
		chmod 770 $particledir/misc/dat_shortened/
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
	python particlePicker.py $dt $firstTime $particledir/ $arg1 $arg2 $arg3 $arg4 txt $numBfieldPlots false
	
	cp seeds/* $root/seeds/
	python $bin/rename_seeds.py $root/ $dt
fi

if $bhForms
then
	echo "	making grid seeds"
	cd $root/bin/grid_code/
	python seedmaker.py $root/ $dt 1 $numBfieldPlots
	targetdir=$root/seeds/
	if $twoColorsSeeds
	then
		mkdir $root/seeds/gridseeds/
		chmod 770 $root/seeds/gridseeds/
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
		python seedmaker.py $root/ $dt 2 $numBfieldPlots
		cd bhseeds/
		for i in *
		do
			cat $i >> $targetdir/$i
		done
	fi

	if $merged
	then
		cd $root/bin/grid_code/
		python seedmaker.py $root/ $dt 3 $numBfieldPlots
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
	chmod 770 $root/$tracefolder/
	rm -rf $particledir/$tracefolder/
	mkdir $particledir/$tracefolder/
	chmod 770 $particledir/$tracefolder/
	if $twoColorsTracer
	then
		mkdir $root/$tracefolder2/
		chmod 770 $root/$tracefolder2/
		rm -rf $particledir/$tracefolder2/
		mkdir $particledir/$tracefolder2/
		chmod 770 $particledir/$tracefolder2/
	fi	

	if $updateParticleMon
	then
		ln -s $root/h5data/particles.mon $particledir/misc/

		cd $particledir/misc/
		./makeparts.awk $particledir/misc/
		rm *.mon

		rm -rf $particledir/misc/dat_shortened/
		mkdir $particledir/misc/dat_shortened/
		chmod 770 $particledir/misc/dat_shortened/
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
	python particlePicker.py $dt $firstTime $particledir/ $arg1 $arg2 $arg3 $arg4 3d $numBfieldPlots false

	cp $tracefolder/* $root/$tracefolder/
	python $bin/rename_seeds.py $root/ $dt $tracefolder/
	if $twoColorsTracer
	then
		cd $particledir
		python particlePicker.py $dt $firstTime $particledir/ $arg1 $arg2 $arg3 $arg4 3d $numBfieldPlots true

		cp $tracefolder2/* $root/$tracefolder2/
		python $bin/rename_seeds.py $root/ $dt $tracefolder2/
	fi
		
fi


cd $cur
echo "done"
