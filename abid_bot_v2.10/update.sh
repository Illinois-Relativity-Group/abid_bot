# This script updates the data folders when new data arrives. Do this only if a black hole has formed. 
# Otherwise, just re-run "setup.sh".
# Run this code only after you run setup. Copy the parameters from "setup.sh" to here. 

. params

. $bin/clean_h5folders.sh
. $bin/make_h5folders.sh 

[ -d $root"/h5data/horizon/" ] && bhForms=true || bhForms=false 
[ $(ls $root/h5data/horizon/all_horizon/h.t*.ah2.gp 2>/dev/null | wc -l) -eq 0 ] && binary=false || binary=true
[ $(ls $root/h5data/horizon/all_horizon/h.t*.ah3.gp 2>/dev/null | wc -l) -eq 0 ] && merged=false || merged=true
echo "binary = "$binary
echo "merged = "$merged

if $bhForms
then
	. $bin/setup_bh.sh
fi



if $bhForms && $fields
then
	tmp=$particleSeeds
	particleSeeds=false
	. $bin/setup_seeds.sh
	particleSeeds=$tmp
fi

rm $root/cm.txt
. $bin/setup_cm.sh

. $bin/setup_frames.sh
echo "update complete!"
