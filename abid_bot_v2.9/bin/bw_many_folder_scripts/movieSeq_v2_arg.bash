#!/bin/bash

# This bash script trasverse thte h5 data and output the starting time and ending time of each folder and the folders name
# Simply run as "./movieSeq_initial.bash [-f]"
# Use "-f" option to skip keyboard response
# V2 will try to use as many frames from later data as possible. Thus it will skip the last few frames for earlier data


# Define a sort function that finds the min and max of an h5 file
sort_h5 (){
    sort_file=$1
    sort_tmp="sort_tmp.txt"
    h5ls $sort_file |sed '$d'| awk '{print $2}'|sed s/"it="//|sed -e 's/\\//g' > $sort_tmp
    sort_min=$(sort -n $sort_tmp | head -n1)
    sort_max=$(sort -n $sort_tmp | tail -n1)
    rm $sort_tmp
} # End of sort_h5()


####################### Usages and Options ######################

usage()
{
echo -e "\e[1;38;5;172m\e[48;5;241m"
cat << EOF
usage: $0 -i it_inc -r folder_root -p folder_pattern -n file_name [-f]

This script run the test1 or test2 over a machine.

OPTIONS:
   -h      Show this message
   -i      iteration increment number, (eg. 256, 128 ..)
   -r      root folders that contains multiple folders of hdf5 files (eg. /home/projects/BHBH_inspiral)
   -p      folder pattern that contains hdf5 files (eg.3d_data_)
   -n      hdf5 file name (eg. rho_b.h5, rho_b.file_0.h5 ...)
   -f      force to run the script without any interaction
EOF
echo -e "\e[0m"
}

it_inc=
folderroot=
folderpattern=
filename=
forceQ=0
while getopts “hi:r:p:n:f” OPTION
do
     case $OPTION in
         h)
             usage
             exit 0
             ;;
         i)
             it_inc=$OPTARG
             ;;
         r)
             folderroot=$OPTARG
             folderroot=${folderroot%/}/    # No longer need to worry about the trailing "/"!
	     ;;
         p)
             folderpattern=$OPTARG
             ;;
         n)
	     filename=$OPTARG
	     ;;
         f)
             forceQ=1;
             ;;
         ?)
             usage
             exit 2
             ;;
     esac
done

if [[ -z $it_inc ]] || [[ -z $folderroot ]] || [[ -z $folderpattern ]] || [[ -z $filename ]];
then
     usage
     exit 1
fi
####################### Parameter Setting ########################
#it_inc=256; 							#Iteration increment
#folderroot="/home/projects/bhbh_mag_inspiral"			#Root path for the h5 data (Dont' forget the "/" at the end)
#folderpattern="3d_data_";					#folder path pattern for h5 data (eg. "3d_data_*")
#folderroot=${folderroot%/}/					# No longer need to worry about the trailing "/"!
#filename=rho_b.file_0.h5;					#name patter for h5 data
#filename=rho_b.h5;

foldername=$folderroot$folderpattern

####################### Introduction #############################
if [ "$forceQ" -eq "0" ]
    then
	echo;
	echo "================Running==============="
	echo;
	echo;
	echo -e "it_inc=\e[1;31m$it_inc\e[0m";
	echo -e "folderroot=\e[1;31m$folderroot\e[0m";
	echo -e "folderpattern=\e[1;31m$folderpattern\e[0m";
	echo -e "filename=\e[1;31m$filename\e[0m";
	echo; echo "Below are the folders that will be traversed"
	echo;
	echo -en "Press ENTER";
	read key_var
	ls -dr $foldername*/
	if [[  $? != 0 ]];
		then
			echo;
			echo "Wrong folderpath!";
			echo;
			echo "ERROR...EXIT";
			echo;
			exit;
	fi
	echo;
	echo -n "Total number of folders = "
	ls -dr $foldername*/ | wc -l
	echo "===================================================="
	echo "Press ENTER to continue the script or enter q to quit"
	read key_var
	while [ -n "$key_var" ]
	do
	    if [ "$key_var" == "q" ]
		then
		    echo "quit..."
		    exit 0
	    fi
	    echo "Press ENTER to continue the script or enter q to quit"
	    read key_var
	done
	echo "Continuing the script....."
	echo;
fi

########################### Main Body ##############################
list_tmp="list_tmp.txt" # temporary list file


rm -f $list_tmp # removes previous output file

#Old way uses specific file.  Will fail if missing that file

#for dir in $( ls -dr $foldername*/ ); do
#	for file in $dir$filename; do
#		sort_h5 $file
#		tmp_start=$sort_min;
#		tmp_end=$sort_max;
#		tmp_frame=$(( ( tmp_end - tmp_start ) / it_inc + 1 ));
#		echo "$tmp_start $tmp_end $tmp_frame $dir" >> $list_tmp
#	done
#done
#End old way

#New way uses first file in folder, works if data is still transferring
for dir in $( ls -dr $foldername*/ ); do
	fil=$(ls $dir | head -n 1);
	sort_h5 $dir$fil;
	tmp_start=$sort_min;
	tmp_end=$sort_max;
	tmp_frame=$(( ( tmp_end - tmp_start ) / it_inc + 1 ));
	echo "$tmp_start $tmp_end $tmp_frame $dir" >> $list_tmp;
done
chmod 770 $list_tmp
#End new way


gap_txt="gap.txt";
rm -f $gap_txt;
echo "# List of folderpaths where gap occurs" > $gap_txt;
echo "# two lines of folder_paths where gap occurs" >> $gap_txt;
echo "# iteration_end folder_path_1" >> $gap_txt;
echo "# iteration_begin folder_path_2" >> $gap_txt;
chmod 770 $gap_txt

duplicate_txt="duplicate.txt";
rm -f $duplicate_txt;
echo "# List of folderpaths which are duplicated by other data" > $duplicate_txt;
echo "# These folders won't be used for filming" >> $duplicate_txt;
chmod 770 $duplicate_txt

overlap_txt="overlap.txt";
rm -f $overlap_txt;
echo "# Version 2" > $overlap_txt;
echo "# List the overlaps with next data (skipping last few frames)" >> $overlap_txt;
echo "# negative number means there's gap between current and next folder" >> $overlap_txt;
echo "# will only use latest dataset for duplicated data" >> $overlap_txt;
echo "# frames_overlaps total_frames_w/_overlaps folder_path" >> $overlap_txt;
chmod 770 $overlap_txt


list_sorted="list_sorted.txt";
sort -n -k1 -k2 $list_tmp > $list_sorted
chmod 770 $list_sorted
first_path=$(head -n1 $list_sorted | awk '{print $4}');
last_path=$(tail -n1 $list_sorted | awk '{print $4}');

max=$(($( head -n1 $list_sorted | awk '{print $1}')-$it_inc));

sort -n -k1 -k2 $list_tmp | while read line
do
	t_start=$(echo $line | awk '{print $1}');
	t_end=$(echo $line | awk '{print $2}');
	t_frame=$(echo $line | awk '{print $3}');
	folder_path=$(echo $line | awk '{print $4}');

	if [[ "$folder_path" == "$first_path" ]] # ignore the first line
	then
		min=$t_start;
		max=$t_end;
		folder_last=$folder_path;
		frame_last=$t_frame;
		if [[ "$last_path" == "$first_path" ]]
		then
			echo "0 $t_frame $folder_path" >> $overlap_txt;
		fi
		continue;
	fi


	if [[ "$min" == "$t_start" ]] # Duplicate
	then
		echo "Duplicate found! See $duplicate_txt for details";
       		echo "$folder_last" >> $duplicate_txt;
		min=$t_start;
		max=$t_end;
		folder_last=$folder_path;
		frame_last=$t_frame;
		continue;
	fi

	it_diff=$(( ($max - $t_start)/$it_inc + 1 ));
	if [[ "$it_diff" -lt "0" ]]; # Gap
	then
		echo "Gap found! See $gap_txt for details";
		echo "$max $folder_last" >> $gap_txt;
		echo "$t_start $folder_path" >> $gap_txt;
		echo >> $gap_txt;
	fi
	echo "$it_diff $frame_last $folder_last" >> $overlap_txt;
	if [[ "$folder_path" == "$last_path" ]] # reaching the end
	then
		echo "0 $t_frame $folder_path" >> $overlap_txt;
	fi
	min=$t_start;
	max=$t_end;
	folder_last=$folder_path;
	frame_last=$t_frame;
done
echo "Success! Please check $overlap_txt for output"
