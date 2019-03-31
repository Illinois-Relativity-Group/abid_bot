
if [[ $(pwd) != $root* || -z "$root" ]]; then
    echo Set params!
    return 1
fi

xmldir=$root/xml/
h5prefix=3d_data_
echo deleting xml files...
rm -rf ${xmldir}/$h5prefix*/*
echo creating xml files...
module load bwpy
python setmovie.py $root/ $it $dt $M $offset $fields $g00 $time_offset $vol1XML $vol2XML $view1XML $view2XML $twoColorsSeeds $particleTracer $twoColorsTracer > xml_log.txt
module unload bwpy

