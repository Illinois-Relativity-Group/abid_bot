# This script creates the overlap.txt file needed for the set_xml script

#####################THINGS TO CHANGE###########################
cycle=$1
h5dir=$2
################################################################

h5prefix=3d_data_
examplefilename=Bx.file_0.h5
module load cray-hdf5
echo ./movieSeq_v2_arg.bash -i $cycle -r $h5dir -p $h5prefix -n $examplefilename -f
./movieSeq_v2_arg.bash -i $cycle -r $h5dir -p $h5prefix -n $examplefilename -f
echo ...done
