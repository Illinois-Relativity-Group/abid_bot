// Taken from Francis
// Modified by Lingyi/Brian
//
// After compiling, run as ./gpto3d ./h.5*.gp
//
//Converts bhdata from gp files to 3d files that visit can read
#include <cstdio>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <stdio.h>
#include <string.h>
#include <string>
using namespace std;
#define TOLERANCE .0005

int main(int argc, const char* argv[])
{
	for(int f=2; f<argc; f++)
	{
        	int n_patches, time, counter1=0, counter2=0;
        	double centerz, centerx, centery;
        	char ofilename[256];
		char timestr[50];
		int bhtype;
		
        	sscanf(argv[f],"h.t%d.ah%i.gp",&time, &bhtype);
		sprintf(ofilename, argv[1]);
		sprintf(timestr, "ht%d_%07i.3d", bhtype, time);
		strcat(ofilename, timestr);
        	ifstream ifile(argv[f]);
        	ofstream ofile(ofilename);
        	ofile.precision(11);
       		ifile.ignore(256,'=');
        	ifile >> n_patches;
        	ifile.ignore(256,'=');
        	ifile >> centerx;
        	ifile >> centery;
        	ifile >> centerz;	
        	ofile << "x\ty\tz\tbh";
		ofile << bhtype;
		ofile <<"p\n";
        		
        for(int i=0; i<n_patches; i++)
        {
            int n_rho, n_sigma;
            ifile.ignore(256,'=');
            ifile >> n_rho;
            ifile.ignore(256,'=');
            ifile >> n_sigma;
            for(int l=0; l<6; l++)
                ifile.ignore(256,'\n');
            for(int j = 0; j < n_rho; j++)
            {
                for(int k = 0; k < n_sigma; k++)
                {
                    char line[256];
                    double dpx, dpy, gridfn, x, y, z;
                    ifile.getline(line, 256);
                    stringstream sline(line,stringstream::in);
                    sline >> dpx >> dpy >> gridfn >> x >> y >> z;
                    ofile <<  x  << '\t' << y  << '\t' << z << '\t' << '0' <<endl;
                    counter1++;
                }
                ifile.ignore(256,'\n');
             }
        }
        ifile.close();
        ofile.close();
    }
    return 0;
}	
