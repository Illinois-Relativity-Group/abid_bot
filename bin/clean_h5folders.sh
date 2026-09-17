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
	# A folder is unusable if it has no *.h5, not merely if it is empty:
	# restart folders often contain only CCTK_Proc1.out, which slips past a
	# file-count test, renders no frames, and still consumes a folder index.
	if ! ls $i/*.h5 >/dev/null 2>&1
	then
		# -T so an existing bad_data/$i symlink is replaced, not descended
		# into (that produced self-referential links inside the data dirs).
		rm -rf $bad_data/$i
		mv -T $i $bad_data/$i
	fi
done
cd $cur
