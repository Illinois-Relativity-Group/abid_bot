if [[ -f "params$1" ]];then
        echo "using params$1"
        . params$1
else
        echo "params$1 not found. using params"
        . params
fi

#Use this if you are submitting very few folders (~1-5)
#Otherwise use runBundle.sh
#####begin things you have to change TODO

jobName=runsingle
h5dir=$root/h5data
extrasDir=$root/xml$1
h5prefix=3d_data_

########run movies variables

pbsfile=$root/bin/bw_many_folder_scripts/singleRun_frontera_frames.pbs
picsavedir=$root/movies
logdir=$root/log
visitScript=$root/bin/bw_many_folder_scripts/run.py
#totranks=0 -- auto detect, no longer need to set
#####end things you have to change

#remove trailing '/'
extrasDir=$( echo $extrasDir | sed "s,/$,,")
h5dir=$( echo $h5dir | sed "s,/$,,")
savefolder=$( echo $savefolder | sed "s,/$,,")
picsavefolder=$( echo $picsavefolder | sed "s,/$,,")

#plotting varibles
PlotDensAsVol=1 # Plot density in a volume plot
PlotDensAsIso=0 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=0 # Plot spin vector
PlotBsq2r=0 # Plot B squared over 2 rho
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="blue" #background color

PlotEvolve=1
PlotZoom=0
PlotFlyOver=0
PlotFlyAround=0

##########This section submits the rest of the files.
# default is first frame
foldernum=(1 2)	#starts from 1, list all folders you want to run
ranknum=(0 1)		#starts from 0, list all ranks in each folder you want to run
count=1
DATE=$(date +%y%m%d_%H%M)
picsavefolder=$picsavedir/"$DATE"_"$jobName"; mkdir -p $picsavefolder
#picsavefolder=$picsavedir/"$jobName"; mkdir -p $picsavefolder		#if you don't want date&time in folder name
logfolder=$logdir/"$DATE"_"$jobName"; mkdir -p $logfolder

cd $logfolder

for dir in $(ls -d ${h5dir}"/"$h5prefix* ); do
	if [[ " ${foldernum[@]} " =~ " ${count} " ]]; then
		echo $count
    		blah=$(ls -d -1 $extrasDir/** | sed -n ${count}p) 
   	 	tosave="$picsavefolder"/"$jobName"_$(printf "%03d" $count)_
		totranks=$(ls ${blah}/time_* | wc -l)
		echo $totranks
		for rank in `seq 0 $(( $totranks - 1 ))`; do
				if [[ " ${ranknum[@]} " =~ " ${rank} " ]]; then
		        	echo submitting job $count with rank = $rank
					#qsub -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,PDAS=$PlotDensAsVol,PDAI=$PlotDensAsIso,PDL=$PlotDensLinear,PV=$PlotVel,PBSQ2R=$PlotBsq2r,PG00=$Plotg00,REFPLOT=$refPlot,CUTPLOT=$cutPlot,BGCOLOR=$bgcolor,PE=$PlotEvolve,PZ=$PlotZoom,PFO=$PlotFlyOver,PFA=$PlotFlyAround,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",RANK=$rank,TOTRANKS=$totranks,NUMBFIELDPLOTS=$numBfieldPlots,VECXML=$vecXML,BSQXML=$bsqXML,G00_PSEUDOXML=$g00_pseudoXML,G00_ISOXML=$g00_isoXML,MAXDENS=$maxdensity,RHO_PSEUDOXML=$rho_pseudoXML,RHO_ISOXML=$rho_isoXML $pbsfile
					sbatch --job-name=$jobName"_"$count"_"$rank --export=ALL,VISITSCRIPT=$visitScript,PDAS=$PlotDensAsVol,PDAI=$PlotDensAsIso,PDL=$PlotDensLinear,PV=$PlotVel,PBSQ2R=$PlotBsq2r,PG00=$Plotg00,REFPLOT=$refPlot,CUTPLOT=$cutPlot,BGCOLOR=$bgcolor,PE=$PlotEvolve,PZ=$PlotZoom,PFO=$PlotFlyOver,PFA=$PlotFlyAround,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",RANK=$rank,TOTRANKS=$totranks,NUMBFIELDPLOTS=$numBfieldPlots,VECXML=$vecXML,BSQXML=$bsqXML,G00_PSEUDOXML=$g00_pseudoXML,G00_ISOXML=$g00_isoXML,MAXDENS=$maxdensity,RHO_PSEUDOXML=$rho_pseudoXML,RHO_ISOXML=$rho_isoXML,PSV=$PlotSpinVec,SPINVECXML=$spinvecXML $pbsfile
				fi
		done
	fi
    count=$((count+1))
done

cd $root
