cur=$PWD
echo "making h5 and xml folders"
mkdir $root"/xml$1/"
chmod 770 $root"/xml$1/"
cd $root"/h5data/"
for i in $(ls -d 3d_data*)
do
	mkdir $root"/xml$1/"$i
	chmod 770 $root"/xml$1/"$i
done
cd $cur

