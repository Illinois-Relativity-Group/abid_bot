. params

attsdir=$root/bin/bw_many_folder_scripts/atts

dir='3d_data_20190528045603'
savename='BHNS_q31_mag_medspin_t0'
seedfile=$root/seeds/BHNS_q31_mag_medspin_seeds_t554.txt

viewXML=$attsdir/bhns_view_reg.xml
volXML=$attsdir/bhns_vol_dim.xml
streamXML=$attsdir/Stream.xml
idx=21

visitScript=$root/bin/bw_many_folder_scripts/runFrame.py
xmldir=$root/xml/$dir
dir=$root/h5data/$dir
tosave=$root/movies/$savename
rank=0
totranks=1

echo "visitScript    = $visitScript"
echo "dir            = $dir"
echo "xmldir         = $xmldir"
echo "tosave         = $tosave"
echo "rank           = $rank"
echo "totranks       = $totranks"
echo "numBfieldPlots = $numBfieldPlots"
echo "vecXML         = $vecXML"
echo "bsqXML         = $bsqXML"
echo "maxdensity     = $maxdensity"
echo "rho_pseudoXML  = $rho_pseudoXML"
echo "rho_isoXML     = $rho_isoXML"
echo "g00_pseudoXML  = $g00_pseudoXML"
echo "g00_isoXML     = $g00_isoXML"
echo "viewXML        = $viewXML"
echo "volXML         = $volXML"
echo "idx            = $idx"
echo "seedfile       = $seedfile"
echo "streamXML      = $streamXML"

visit -cli -nowin -s $visitScript $dir $xmldir $tosave $rank $totranks $numBfieldPlots $vecXML $bsqXML $maxdensity $rho_pseudoXML $rho_isoXML $g00_pseudoXML $g00_isoXML $viewXML $volXML $idx $seedfile $streamXML
