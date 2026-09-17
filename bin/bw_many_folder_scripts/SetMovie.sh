xmldir=$root/xml$1/
h5prefix=3d_data_
echo deleting xml files...
rm -rf ${xmldir}/$h5prefix*/*
echo creating xml files...
# riemann: no module system; system python3 is used
python3 setmovie.py $root/ $it $dt $M $offset $fields $numBfieldPlots $g00 $time_offset $vol1XML $vol2XML $view1XML $view2XML $twoColorsSeeds $particleTracer $twoColorsTracer $xmldir $streamXML > xml_log.txt

chmod 770 -R $xmldir
