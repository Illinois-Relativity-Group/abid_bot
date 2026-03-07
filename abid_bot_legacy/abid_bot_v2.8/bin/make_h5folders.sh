cur=$PWD
echo "making h5 and xml folders"
mkdir $root"/xml/"
cd $root"/h5data/"
for i in $(ls -d 3d_data*)
do
	mkdir $root"/xml/"$i
done
cd $cur

