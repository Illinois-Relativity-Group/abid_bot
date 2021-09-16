

echo "Removing old 3D folder"
rm -r gwdata
mkdir gwdata
echo "Done"

echo "Starting hplushcross code"
g++ -O2 -fopenmp DataFile.cpp hplus_hcross.cpp -o hplus_hcross -lfftw3 && ./hplus_hcross
echo "hplushcross finished"

