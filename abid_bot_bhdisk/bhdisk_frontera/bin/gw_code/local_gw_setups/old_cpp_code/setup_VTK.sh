
files_per_folder=25
M=7.895769590229179
gw_dt=$(sed -n '2p' gwdata/1D | sed -e 's,e.*,,')
extraction_r=300.
echo "Making gravity wave time list"
python3 gw_time_lister.py $M $gw_dt $extraction_r
echo "Time list finished"
cur=$PWD
cd gwdata/3D

numfiles=$(ls *hcross* | wc -l)
folderidx=0

echo "Moving files into new folders"

for i in `seq 0 $(($numfiles - 1))`; do
	curdir=VTK$(printf "%03d" $folderidx)
	if [ ! -d $curdir ]; then
		mkdir $curdir
	fi
	
	mv *_$(printf "%d" $i).vtk $curdir

	if [ $(( ($i+1) % $files_per_folder)) == 0 -a $i != 0 ]; then
		folderidx=$((folderidx+1))
	fi
done

echo "All files moved"

cd $cur
