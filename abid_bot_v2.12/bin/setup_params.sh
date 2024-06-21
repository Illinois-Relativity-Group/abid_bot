module load hdf5

cur=$PWD
bin=$root"/bin"

echo "setting up params"

cd $root"/h5data"

rm temp.txt
touch temp.txt

for dir in 3d*; do
	h5dump -N timestep  $dir"/Bx.file_0.h5" > temp.txt
	break
done

lines=$(sed -n -e 's/^.*(0): //p' temp.txt)
min=0
for line in $lines; do
	if (($min==0)); then
	       min=$line
	       continue
        fi
	if (($min>$line)) && (($line!=0)); then
		min=$line
		continue
	fi
done

newit="it=\"$min\" "
newdt="dt=\"$(awk 'NR==4{print $1}' bhns.xon)\" "
newft="firstTime=\"$(awk 'NR==2{print $1}' bhns.xon)\" "
echo "hey"
if [ $(awk 'NR==2{print $1}' bhns.xon)=="0.0000000000E+000" ]; then
	echo "hi"
	newft="firstTime=\"00000.00000000000\" "
fi	
newmax="maxdensity=\"$(awk 'NR==2{print $9}' bhns.mon)\" "
newM="M=\"$(awk 'NR==2{printf $12}' bhns.mon)+$(awk 'NR==2{printf $13}' bhns.mon)\" "

echo "$newit"
echo "$newdt"
if [ $(awk 'NR==2{print $1}' bhns.xon)!="0.0000000000E+000" ]; then
       echo "recheck first time"	
fi       
echo "$newft"
echo "$newmax"
echo "$newm"

cd ..

previt=$(sed -n -e '/it=/p' params |sed 's/#.*//')
prevdt=$(sed -n -e '/dt=\"/p' params |sed 's/#.*//')
prevft=$(sed -n -e '/firstTime=\"/p' params |sed 's/#.*//')
prevmax=$(sed -n -e '/maxdensity=\"/p' params |sed 's/#.*//')
prevM=$(sed -n -e '/M=\"/p' params |sed 's/#.*//')

sed -i -e "s/$previt/$newit/g" params
sed -i -e "s/$prevdt/$newdt/g" params
sed -i -e "s/$prevft/$newft/g" params
sed -i -e "s/$prevmax/$newmax/g" params
sed -i -e "s/$prevM/$newM/g" params

cd bin

rm $root"/h5data/temp.txt"
#sed -i 's/prev/it=\"$min\" #45_low_m/m/' params
