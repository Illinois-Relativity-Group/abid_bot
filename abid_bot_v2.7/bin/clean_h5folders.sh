echo "cleaning h5 and xml folders"
cur=$PWD
rm -rf $root/xml/
cd $root/h5data/
for i in $(ls -d 3d_data*)
do
	if [ $(ls $i | wc -l) -eq 0 ]
	then
		rm -rf $i
	fi
done
cd $cur
