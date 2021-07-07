echo "cleaning h5 and xml folders"
cur=$PWD
rm -rf $root/xml$1/
cd $root/h5data/
bad_data=$root/h5data/bad_data

if [ ! -d $bad_data ]; then
	mkdir $bad_data
	chmod 770 $bad_data
fi

for i in $(ls -d 3d_data*)
do
	if [ $(ls $i | wc -l) -eq 0 ]
	then
		mv $i $bad_data/$i
	fi
done
cd $cur
