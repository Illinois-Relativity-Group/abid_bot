

echo "Removing old 3D folder"
rm -r gwdata
mkdir gwdata
echo "Done"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/usr/lib


echo "Starting hplushcross code"
g++  -I $HOME/usr/include -O2 -fopenmp DataFile.cpp hplus_hcross.cpp -o hplus_hcross -L/usr/lib64 -L$HOME/usr/lib -lfftw3 && ./hplus_hcross
echo "hplushcross finished"

