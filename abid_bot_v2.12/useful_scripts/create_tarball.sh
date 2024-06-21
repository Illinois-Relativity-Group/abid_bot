#!/bin/bash

start_time=$(date +%s)

cd $root
chmod +x $root/useful_scripts/create_tarball.sh

script_dir=$root

echo $script_dir

dir_name=$(basename "$script_dir")

echo "Making a tarball of directory: $dir_name"

tarball_name="${dir_name}.tar.gz"

tar -cvzf "$tarball_name" \
    --exclude="h5data/*" \
    --exclude="log/*" \
    --exclude="movies/*" \
    --exclude="xml/*" \
    --exclude="seeds/*" \
    --exclude="bhdata/*" \
    --exclude="bin/particle_code/dat/*" \
    --exclude="bin/grid_code/bhseeds/*" \
    --exclude="bin/gw_code/VTKdata/*" \
    -C "$script_dir" .

echo "Created tarball: $tarball_name"

end_time=$(date +%s)
execution_time=$((end_time - start_time))

echo "Time to make tarball: $execution_time seconds"
