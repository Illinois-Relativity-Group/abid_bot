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

all_frames=true


# jobName=04_no_Bfields
jobName=test_vel
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
PlotDensAsVol=0 # Plot density in a volume plot
PlotDensAsIso=1 # Plot density in a pseudocolor plot as isosurfaces
PlotDensLinear=0 # Plot linear scale density rather than log scale
PlotVel=0 # Plot velocity arrows
PlotSpinVec=0 # Plot spin vector
PlotBsq2rAsVol=0 # Plot B squared over 2 rho in a volume plot
PlotBsq2rAsIso=0 # Plot B squared over 2 rho in a pseudocolor plot as isosurfaces
Plotg00=0 # Plot g00 from metric
refPlot=1 # Reflect plot over xy plane
cutPlot=0 # only show back half (y>0), needs view like: (0,-x,y)
bgcolor="blue" #background color

PlotCustomVel=1


PlotEvolve=1
PlotZoom=0
PlotFlyOver=0
PlotFlyAround=0

#run folder

foldernum=(13)
ranknum=(0)

# foldernum=(15)
# ranknum=(47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76)

# foldernum=(16)
# ranknum=(33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77)

#initial frame
# foldernum=(1)
# ranknum=(1)
#ranknum=(1 2)

#stars touch
#foldernum=(5)
#ranknum=(20)

#after merger
#foldernum=(6)
#ranknum=(55 56 57 58)

#test last
# foldernum=(1)
# ranknum=(122)


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
				# if [[ $all_frames ]] || [[ " ${ranknum[@]} " =~ " ${rank} " ]]; then
		        	echo submitting job $count with rank = $rank
					visit -cli -nowin -forceversion 3.3.3 -s $visitScript $PlotDensAsVol $PlotDensAsIso $PlotDensLinear $PlotVel $PlotBsq2rAsVol $Plotg00 $refPlot $cutPlot $bgcolor $PlotEvolve $PlotZoom $PlotFlyOver $PlotFlyAround $dir $blah $tosave$(printf "%03d" $rank)"_" $rank $totranks $numBfieldPlots $vecXML $bsqXML $g00_pseudoXML $g00_isoXML $maxdensity $rho_pseudoXML $rho_isoXML $PlotSpinVec $spinvecXML $vec2XML $bsq_pseudoXML $bsq_isoXML $PlotBsq2rAsIso	
				fi
		done
	fi
    count=$((count+1))
done

cd $root
