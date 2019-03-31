cur=$PWD
bin=$root"/bin"

echo "setting up black hole data..."
rm -rf $root/bhdata/
mkdir $root/bhdata/

echo "		sifting *.gp files'"
python $bin/sift_gp.py $root/h5data/horizon/ $it 1
python $bin/center_lister.py $root/ $it $dt 1

if $binary
then
	python $bin/sift_gp.py $root/h5data/horizon/ $it 2
	python $bin/center_lister.py $root/ $it $dt 2
fi

if $merged
then
	python $bin/sift_gp.py $root/h5data/horizon/ $it 3
	python $bin/center_lister.py $root/ $it $dt 3
fi

echo "		creating bhdata"
cd $bin
g++ gpto3d.cpp -o gpto3d
mv gpto3d $root/h5data/horizon/
cd $root/h5data/horizon/
./gpto3d $root"/bhdata/" h.t*
rm gpto3d

cd $cur
echo "done"
