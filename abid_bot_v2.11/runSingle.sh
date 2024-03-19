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

jobName=cut_plot_vel
h5dir=$root/h5data
extrasDir=$root/xml$1
h5prefix=3d_data_

########run movies variables

pbsfile=$root/bin/bw_many_folder_scripts/singleRun_anvil_frames.pbs
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
PlotDensAsVol=0 # Plot density in a volume plot
PlotDensAsIso=1 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=0 # Plot spin vector
PlotBsq2rAsVol=0 # Plot B squared over 2 rho in a volume plot
PlotBsq2rAsIso=0 # Plot B squared over 2 rho in a pseudocolor plot as isosurfaces
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=1 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="blue" #background color

PlotVelCustom=1  #plot velocity arrows with custom generated .vtk file using Vel.xml settings
VelCustomFile=$root/h5data/test.vtk
# VelCustomFile=$root/h5data/half_c_field.vtk

PlotEvolve=1
PlotZoom=0
PlotFlyOver=0
PlotFlyAround=0

##########This section submits the rest of the files.
# default is first frame
#foldernum=(0 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280 290 300)	#starts from 1, list all folders you want to run
#foldernum=($(seq 1 204))
#ranknum=($(seq 0 30))

# foldernum=(1)
# ranknum=(1)

foldernum=(3)
ranknum=(71)

#initial frame
#foldernum=(1)
#ranknum=(1)		#starts from 0, list all ranks in each folder you want to run
#ranknum=(1 2)

#stars touch
#foldernum=(4)
#ranknum=(34 35 36)

#after merger
#foldernum=(5)
#ranknum=(45)

#test last
#foldernum=(12)
#ranknum=(76)


count=1
DATE=$(date +%y%m%d_%H%M)
picsavefolder=$picsavedir/"$jobName"; mkdir -p $picsavefolder
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
					# echo visit -cli -nowin -forceversion 3.1.4 -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $blah $tosave$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $g00_pseudoXML $g00_isoXML $maxdensity $rho_pseudoXML $rho_isoXML $PlotSpinVec $spinvecXML $vec2XML $bsq_pseudoXML $bsq_isoXML $PlotBsq2rAsIso $PlotVelCustom $VelCustomFile
					# echo $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $Plotg00 $refPlot $cutPlot $bgcolor
					# echo $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $blah $tosave$(printf "%03d" $rank)"_" $rank $totranks 
					# echo $numBfieldPlots $vecXML $bsqXML $g00_pseudoXML $g00_isoXML $maxdensity $rho_pseudoXML $rho_isoXML $PlotSpinVec 
					# echo $spinvecXML $vec2XML $bsq_pseudoXML $bsq_isoXML $PlotBsq2rAsIso $pbsfile
					#qsub -N $jobName"_"$count"_"$rank -v VISITSCRIPT=$visitScript,PDAS=$PlotDensAsVol,PDAI=$PlotDensAsIso,PDL=$PlotDensLinear,PV=$PlotVel,PBSQ2R=$PlotBsq2r,PG00=$Plotg00,REFPLOT=$refPlot,CUTPLOT=$cutPlot,BGCOLOR=$bgcolor,PE=$PlotEvolve,PZ=$PlotZoom,PFO=$PlotFlyOver,PFA=$PlotFlyAround,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",RANK=$rank,TOTRANKS=$totranks,NUMBFIELDPLOTS=$numBfieldPlots,VECXML=$vecXML,BSQXML=$bsqXML,G00_PSEUDOXML=$g00_pseudoXML,G00_ISOXML=$g00_isoXML,MAXDENS=$maxdensity,RHO_PSEUDOXML=$rho_pseudoXML,RHO_ISOXML=$rho_isoXML $pbsfile
					sbatch --job-name=$jobName"_"$count"_"$rank --export=ALL,VISITSCRIPT=$visitScript,PDAS=$PlotDensAsVol,PDAI=$PlotDensAsIso,PDL=$PlotDensLinear,PV=$PlotVel,PBSQ2RAV=$PlotBsq2rAsVol,PG00=$Plotg00,REFPLOT=$refPlot,CUTPLOT=$cutPlot,BGCOLOR=$bgcolor,PE=$PlotEvolve,PZ=$PlotZoom,PFO=$PlotFlyOver,PFA=$PlotFlyAround,H5=$dir,EXTRAS=$blah,SAVEFOLDER=$tosave$(printf "%03d" $rank)"_",RANK=$rank,TOTRANKS=$totranks,NUMBFIELDPLOTS=$numBfieldPlots,VECXML=$vecXML,BSQXML=$bsqXML,G00_PSEUDOXML=$g00_pseudoXML,G00_ISOXML=$g00_isoXML,MAXDENS=$maxdensity,RHO_PSEUDOXML=$rho_pseudoXML,RHO_ISOXML=$rho_isoXML,PSV=$PlotSpinVec,SPINVECXML=$spinvecXML,VEC2XML=$vec2XML,BSQ_PSEUDOXML=$bsq_pseudoXML,BSQ_ISOXML=$bsq_isoXML,PBSQ2RAI=$PlotBsq2rAsIso,CUSTOMVEL=$PlotVelCustom,VELVTK=$VelCustomFile $pbsfile
				fi
		done
	fi
    count=$((count+1))
done

cd $root
