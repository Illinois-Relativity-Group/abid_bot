#!/bin/bash

dirs="24_01_28_025450
24_01_29_015828
24_01_29_135851
24_01_30_020649
24_01_30_140749
24_01_31_020902
24_01_31_141001
24_02_06_100738
24_02_07_215921
24_02_08_095942
24_02_08_220044
24_02_09_100149
24_02_09_220218
24_02_10_100242
24_02_10_220305
24_02_11_100327"


for dir in $dirs
do
        echo $dir
        cmd="scp -r $dir/rho_b.file_* anvil:/anvil/scratch/x-ericyu3/abid_bot_gw/h5data_ir2.70/$dir"
        $cmd
done

echo "DONE IM DONE THE THING IS OVER"