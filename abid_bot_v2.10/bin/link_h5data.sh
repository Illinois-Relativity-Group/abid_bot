# This file creates symbolic links to the data
# full path to actual data
rootlink=$PWD/../
origin="/u/sciteam/ruiz1/scratch/Tilted_Bfield/anti_alig/spHd2.5_K123.6_131_1.5cor"
beta="$origin/beta100"
#full path to h5dir and bh data
h5dest=$rootlink/h5data/
bhdest=$rootlink/horizon/all_horizon/

if [ ! -f $h5dest/particles.mon ] && [ -f $beta/bhns-particles.mon ]; then
        ln -s $origin/bhns-particles.mon $h5dest/particles.mon
fi

if [ -f $origin/bhns.mon ]; then
	cp $origin/bhns.mon $h5dest
fi
if [ -f $origin/bhns.xon ]; then
    cp $origin/bhns.xon $h5dest
fi
cp $origin/*.par $h5dest

if [ -f $beta/BH_diagnostics.ah1.gp ] && [ ! -f $h5dest/BH_diagnostics.ah1.gp ]; then
        cp $beta/BH_diagnostics.ah1.gp $h5dest
fi
if [ -f $beta/BH_diagnostics.ah2.gp ] && [ ! -f $h5dest/BH_diagnostics.ah2.gp ]; then
        cp $beta/BH_diagnostics.ah2.gp $h5dest
fi
if [ -f $beta/BH_diagnostics.ah3.gp ] && [ ! -f $h5dest/BH_diagnostics.ah3.gp ]; then
        cp $beta/BH_diagnostics.ah3.gp $h5dest
fi

for i in $(ls -d $beta/3d* | xargs -n 1 basename); do #just file name no path
        if [ ! -d $h5dest/$i ]; then
                echo Linking $i
                ln -s $beta/$i $h5dest
        fi
done

for i in $(ls $beta/h.t*.gp | xargs -n 1 basename); do
        if [ ! -f $bhdest/$i ]; then
                echo Linking $i
                ln -s $beta/$i $bhdest/
        fi
done
