module load python

cd $gwdir
python3 params_gw.py $root
python3 setup_gw.py $root >&setup_progress.txt&
cd $root
echo "Creating the VTK files needed for gravitational waves takes a long time, so I'm running it in the background"
echo "You will need to rerun setup.sh"
echo "Run this command after some time: tail -n 1 $gwdir/setup_progress.txt"
echo "If the output is YIPPPPEEEEEEEEEE DONE XD, set updateGWdata=false in params and rerun setup.sh"