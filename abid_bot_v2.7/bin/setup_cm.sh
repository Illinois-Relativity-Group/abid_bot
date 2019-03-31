cur=$PWD

echo "making cm.txt"
if [ ! $numStars -eq 0 ]
then 
	python $root/bin/cmmake.py $numStars $root/
fi

if $bhForms
then
	cd $root/bin/grid_code/
	python $root/bin/cm_append.py $root/
	if $merged
	then
		cat $root/bin/grid_code/bhcen3.txt >> $root/cm.txt
	fi
	cd $root
fi
cd $cur
echo "done"
