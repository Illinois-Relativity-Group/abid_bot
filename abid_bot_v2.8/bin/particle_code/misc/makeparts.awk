#Taken from Brian
#Modified by Lingyi Kong
#Last edited on Nov 2, 2013
# This code separates the particle.mon file into smaller .dat files based on time
#	These files are used for parts_new.cpp code to generate particle seeding points
# Use "grep -n \# particle.mon" to find the line numbers that can be deleted
date;

wdir=$(pwd);

folder="dat/";

dir=$1;

file_original="particles.mon";

mkdir $dir$folder;

cd $dir$folder;

echo $(pwd);

awk -F " " '{if (/#/) {} else {print > $1".dat"}}' $dir$file_original

ls > $dir"part.txt"; for i in `cat $dir"part.txt"`;do mv $i $(echo $i | sed s/".dat"// | awk '{printf "%017.11f\n", $1}')".dat";done;    
#"%017.11f" has 11 digits for decimal parts, 5 digits for interger part with 0 padding (used for sorting files in the correct order", 1 digit for "."

ls > $dir"files.txt"; 	#create a list of the files for seed points select

cd $wdir;

date;
