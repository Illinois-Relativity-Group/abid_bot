. params
n_frac=1
#module load bwpy
#Make Images

echo "Making images..."
#python bin/save.py $M 

plotting_mode=3
if test "$plotting_mode" = 1
then
    echo "Plotting mode 1"
    python bin/plot.py $M $dt
elif test "$plotting_mode" = 2
then
    echo "Plotting mode 2"
    python bin/plot_2.py $M $dt
elif test "$plotting_mode" = 3
then
    echo "Plotting mode 3"
    python3 bin/plot_3.py $M $dt $n_frac
else
    echo "Plotting mode 4"
    python bin/plot_4.py $M $dt $n_frac
fi

echo "...done"
