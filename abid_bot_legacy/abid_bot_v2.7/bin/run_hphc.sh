. params

cur=$PWD

echo "Removing old 3D folder"
rm -r $root/gwdata/3D
echo "Done"

cd $root/bin/gw_code

echo "Starting hplushcross code"
g++ -O2 -fopenmp DataFile.cpp hplus_hcross.cpp -o hplus_hcross -lfftw3 && ./hplus_hcross
echo "hplushcross finished"

cd $root/bin

echo "Making gravity wave time list"
python gw_time_lister.py $root $M $gw_dt
echo "Time list finished"

cd $root/gwdata/3D

numfiles=$(ls *hcross* | wc -l)
folderidx=0

echo "Moving files into new folders"

for i in `seq 0 $(($numfiles - 1))`; do
	curdir=$root/gwdata/3D/VTK$(printf "%03d" $folderidx)
	if [ ! -d $curdir ]; then
		mkdir $curdir
	fi
	
	mv *_$(printf "%04d" $i).vtk $curdir

	if [ $(($i % 25)) == 0 -a $i != 0 ]; then
		folderidx=$((folderidx+1))
	fi
done

echo "All files moved"

cd $cur 
