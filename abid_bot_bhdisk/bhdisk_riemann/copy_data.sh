#root=/anvil/scratch/x-colson1/abid_bot_sol_01
root=/data/codyolson/abid_bot_sol_v2/abid_bot_disk_template
#datadir=/anvil/scratch/x-jbamber/BH_massiveDisk/bhtD2.0_fAJS0.80_000_000_q2.00_l4.00_r0.40_gamma4o3_sol_01
datadir=/data/codyolson/bhtD2.0_fAJS0.80_000_000_q2.00_l4.00_r0.40_gamma4o3_sol_01_v2

#datadir=/anvil/scratch/x-jbamber/BH_massiveDisk/bhtD2.0_fAJS0.80_000_000_q1.85_l3.65_r0.40_gamma4o3_sol_07

cd $root/h5data
for d in $datadir/beta100/25_*; do    ln -s "$d" "3d_data_$(basename "$d")";done
cp $datadir/data/*on .
cp $datadir/data/*.gp ./horizon/all_horizon/

cd horizon/all_horizon/
cp -u $datadir/AH_data/*.gp .

cd $root
echo "Setup complete."