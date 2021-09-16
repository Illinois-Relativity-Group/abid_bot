#!/bin/bash

for f in *
do
#change the prefix syntax as you need
if [[ $f == 2?_* ]]
then 
mv -- "$f" "3d_data_$f"
#Script to remove _
#suf=`echo $f | sed -e 's/_//g' -e 's/^3ddata//'`
#echo $suf
#mv "$f" "3d_data_$suf"
fi
done

