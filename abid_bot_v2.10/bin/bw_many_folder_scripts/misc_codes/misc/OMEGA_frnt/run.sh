#Params
vxfile=/u/sciteam/liu14/scratch/OMEGAhydro/data/vx.xy.asc
vyfile=/u/sciteam/liu14/scratch/OMEGAhydro/data/vy.xy.asc
delta_r=0.16 #will collect omega data for multiples of this r value, should be around size of grid refinement
M=2.9991824827 #ADM Mass of system
dt=0.083333 #time per iteration
comp_omega_mode=2 #mode in computing omega
ini_omega=1.24e-4 #self-define initial omega if comp_omega_mode=2
ini_time=0.0 #initial time of the data, needed to be set when regridding
start_time=803  #start time that you split the data(unit is M). 

plotting_mode=3
#Different plotting modes (see below):                                                                                                                                  
#1. Plot with all solid curves with gradient color labeled as "T/M".   
#2. Calculate period P, plot with all solid curves with gradient color labeled as "T/P".                                                                                  
#3. Plot with three distinct group of colors with different dashed curves.                                                                                                

#Split Ascii files

if [ -e vel_data_iter ]
then
	echo "Ascii file already split"
else
	mkdir vel_data_iter
	echo "Splitting vx..."
	python bin/split.py $vxfile x $M $start_time
	echo "...done"
	echo "Splitting vy..."
	python bin/split.py $vyfile y $M $start_time
	echo "...done"
fi

if [ -e vel_data ]
then 
        echo "Iteration already converted to time"
else
        #echo "Copying velocity data..."
        #cp -r vel_data_iter vel_data
        mkdir vel_data
        echo "Converting from iteration to time"
	python bin/iter_to_time.py $dt $M $ini_time
	echo "moving data..."
	mv v*txt vel_data
	echo "...done"
fi

#Convert to Omega
echo
if [ -e w_data ]
then
	echo "Omega files already made"
else
	mkdir w_data
	echo "Creating w data..."
	python bin/vel_to_omega.py $delta_r $M $ini_time $start_time
	echo "...done"
fi

#Time average over nearby files
echo
if [ -e t_ave ]
	then
	rm -rf t_ave
fi
mkdir t_ave

echo "Time averaging..."
python bin/new_time_ave.py $dt $comp_omega_mode $M $ini_time $start_time
echo "...done"

#Make Images
echo
if [ -e png_ave ]
	then
	rm -rf png_ave
fi
mkdir png_ave

echo "Making images..."
python bin/save.py $M 
if [ -e w_data/w_000000.txt ]
         then
         cp w_data/w_000000.txt .
fi

if test "$plotting_mode" = 1
then
    echo "Plotting mode 1"
    python bin/plot.py $M $dt
elif test "$plotting_mode" = 2
then
    echo "Plotting mode 2"
    python bin/plot_2.py $M $dt
else
    echo "Plotting mode 3"
    python bin/plot_3.py $M $dt
fi

echo "...done"
