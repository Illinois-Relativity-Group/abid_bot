#include <cassert>
#include <cmath>
#include <complex>
#include <iostream>
#include <algorithm>

#ifdef _OPENMP
#include <omp.h>
#endif
#include <sys/stat.h>
#include <fftw3.h>

#include "DataFile.h"
using namespace std;

// to compile and run:
// g++ -O2 -fopenmp DataFile.cpp hplus_hcross.cpp -o hplus_hcross -lfftw3 && ./hplus_hcross

size_t num_modes, num_times;
vector<complex<double> > Clm;
double dt;
double r_phys;

// TODO: automatic cutoff, wisdom, threads, proper padding
void calc_Clm(string const & filename, double m_adm, double cutoff_w=0.05, size_t padding=100000)
{
   cout << cutoff_w;   // load Psi4
   DataFile<double> file;
   file.loadCSV(filename);
   // sort and remove duplicate time steps
   file.resampleCSV();
   // check rows and columns
   assert(file.nx>1 || file.ny>1 || file.nx%2);
   dt=file[1][0]-file[0][0];
   r_phys=file[0][file.nx-4];   //extraction_r is fourth from last column 
   num_times=file.ny;
   num_modes=(file.nx-1)/2 -2; // last 4 columns are not psi4 modes
   Clm.resize(num_times*num_modes);
   size_t padded_num_times=2*padding+num_times;
   
   // power spectrum file
   //DataFile<double> output;
   //output.resize(file.nx, padded_num_times);
   
   for(size_t mode=0; mode<num_modes; mode++)
   {
      // padded data gives higher frequency resolution
      fftw_complex *time_domain=(fftw_complex *)fftw_malloc(sizeof(fftw_complex) * padded_num_times),
                   *frequency_domain=(fftw_complex *)fftw_malloc(sizeof(fftw_complex) * padded_num_times);
      for(size_t i=0; i<padding; i++)
      {
         time_domain[i][0]=0.0;
         time_domain[i][1]=0.0;
         time_domain[padding+num_times+i][0]=0.0;
         time_domain[padding+num_times+i][1]=0.0;
      }
      for(size_t time=0; time<num_times; time++)
      {
         // force zero endpoints (not really necessary)
         double dtime=time/(num_times-1.0);
         time_domain[padding+time][0]=file[time][1+2*mode]
            -file[0][1+2*mode]*(1.0-dtime)-file[num_times-1][1+2*mode]*dtime;
         time_domain[padding+time][1]=file[time][2+2*mode]
            -file[0][2+2*mode]*(1.0-dtime)-file[num_times-1][2+2*mode]*dtime;
      }
      
      // forward transform
      fftw_plan plan_forward = fftw_plan_dft_1d(padded_num_times, time_domain, frequency_domain, FFTW_FORWARD, FFTW_ESTIMATE);
      fftw_execute(plan_forward);
      
      // scale in frequency_domain (-I/w -> one time integration)
      double c=r_phys/(m_adm*padded_num_times),
             dw=2.0*M_PI/(dt*(padded_num_times-1));
      for(size_t i=0; i<padded_num_times; i++)
      {
         int i2=i<=padded_num_times/2?i:i-padded_num_times;
         double w=i2*dw;
         
         /*output[i][0]=w;
         output[i][1+2*mode]=frequency_domain[i][0];
         output[i][2+2*mode]=frequency_domain[i][1];*/
         
         if(abs(w)<cutoff_w)
         {
            frequency_domain[i][0]*=-c/(cutoff_w*cutoff_w);
            frequency_domain[i][1]*=-c/(cutoff_w*cutoff_w);
         } else {
            frequency_domain[i][0]*=-c/(w*w);
            frequency_domain[i][1]*=-c/(w*w);
         }
      }
      
      // backward transform
      fftw_plan plan_backward = fftw_plan_dft_1d(padded_num_times, frequency_domain, time_domain, FFTW_BACKWARD, FFTW_ESTIMATE);
      fftw_execute(plan_backward);
      
      // transpose buffer for cache locality
      for(size_t time=0; time<num_times; time++)
         Clm[time*num_modes+mode]=complex<double>(time_domain[padding+time][0],time_domain[padding+time][1]);
      
      // fftw deallocate
      fftw_destroy_plan(plan_backward);
      fftw_destroy_plan(plan_forward);
      fftw_free(frequency_domain);
      fftw_free(time_domain);
   }
   //output.saveCSV("power_spectrum.dat");
}


void write_Clm(string const & filename)
{
   DataFile<double> output;
   output.resize(2,num_times*num_modes);
   // sample h+, hx and write to file
   for(size_t time=0; time<num_times; time++)
   {
      for(size_t mode=0; mode<num_modes; mode++)
      {
	     output[time*num_modes+mode][0] = Clm[time*num_modes+mode].real();
		 output[time*num_modes+mode][1] = Clm[time*num_modes+mode].imag();
      }
   }
   cout << "dt=" << dt << endl;
   cout << "num_times=" << num_times << endl;
   cout << "num_modes=" << num_modes << endl;
   cout << "r_phys=" << r_phys << endl;
   output.saveCSV(filename);
}




int main (int argc, const char *argv[])
{
   string filename = argv[1];
   double ADM_M = stod(argv[2]);
   double cutoff_w = stod(argv[3]);
   string fol_name = argv[4];
   cout << "dead among the leaves and stones" << endl;
   cout << filename << endl;
   cout << ADM_M << endl;
   cout << cutoff_w << endl;
   calc_Clm(filename, ADM_M, cutoff_w);
   cout << "write_CLM" << endl;
   write_Clm(fol_name + "/Clm"); 
   return 0;
}
