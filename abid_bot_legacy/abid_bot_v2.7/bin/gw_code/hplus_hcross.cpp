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
float ReverseFloat( const float inFloat )
{
       float retVal;
          char *floatToConvert = ( char* ) & inFloat;
             char *returnFloat = ( char* ) & retVal;

                // swap the bytes into a temporary buffer
                   returnFloat[0] = floatToConvert[3];
                      returnFloat[1] = floatToConvert[2];
                         returnFloat[2] = floatToConvert[1];
                            returnFloat[3] = floatToConvert[0];
                
                                return retVal;
                                }

double factorial(int number) {
   int retvalue=number;
   for(int i=1;i<number;i++) {
      retvalue *= i;
   }
   if(number==0)
      retvalue = 1;
   return (double)retvalue;
}

double plgndr(int l, int m, double x)
{
   double fact,pll,pmm,pmmp1,somx2;
   int i,ll;
   // bad args
   assert(!(m < 0 || m > l || fabs(x) > 1.0));
   pmm=1.0;
   if (m > 0) {
      somx2=sqrt((1.0-x)*(1.0+x));
      fact=1.0;
      for (i=1;i<=m;i++) {
         pmm *= -fact*somx2;
         fact += 2.0;
      }
   }
   if (l == m)
      return pmm;
   else {
      pmmp1=x*(2*m+1)*pmm;
      if (l == (m+1))
      return pmmp1;
      else {
         for (ll=m+2;ll<=l;ll++) {
            pll=(x*(2*ll-1)*pmmp1-(ll+m-1)*pmm)/(ll-m);
            pmm=pmmp1;
            pmmp1=pll;
         }
         return pll;
      }
   }
}

//Stolen from PsiKadelia thorn:
void compute_Wlm_Xlm(int l,int m,double th,double ph,double &Wlmr,double &Wlmi,double &Xlmr,double &Xlmi) {
   double cost,sint,cott,cosmp,sinmp,Plm,fac1,fac1_0,fac2,Pl1;
   double Plm1,Ylmr,Ylmi,Ylmtr,Ylmti;

   cost = cos(th);
   sint = sin(th);

   cott = cost/sint;
   fac2 = sqrt( (2.0*l+1.0)*factorial(l-(int)fabs(m)) / ( 4.0*M_PI*factorial(l+(int)fabs(m)) ) );
   fac1 = fac2 * (l+fabs(m))*(l-fabs(m)+1.0);
   fac1_0 = sqrt( (2.0*l+1.0)/(4.0*M_PI) );

   cosmp = cos( m * ph );
   sinmp = sin( m * ph );

   Plm = plgndr(l,(int)fabs(m),cost);

   if(m==0) {
      Pl1 = plgndr(l,1,cost);
      Ylmr = fac2*Plm;
      Ylmtr = fac1_0 * Pl1;
      Wlmr = -l*(l+1.0)*Ylmr - 2.0*cott*Ylmtr;
      Xlmr = 0.0;
      Wlmi = 0.0;
      Xlmi = 0.0;
   } else {
      Plm1 = plgndr(l,(int)fabs(m)-1,cost);
      Ylmr = fac2*Plm;
      Ylmtr = -fac1*Plm1 - fabs(m)*cott*fac2*Plm;
      if(m < 0) {
         Ylmr = Ylmr*pow(-1.0,-m);
         Ylmtr = Ylmtr*pow(-1.0,-m);
      }

      Wlmr = ( -l*(l+1.0)*Ylmr -2.0*cott*Ylmtr + 2.0*Ylmr*pow(m/sint,2) );
      Xlmr = 2.0*(Ylmtr - cott*Ylmr)*m;
      Wlmi = Wlmr * sinmp;
      Xlmi = Xlmr*cosmp;
      Wlmr = Wlmr*cosmp;
      Xlmr = -Xlmr*sinmp;
   }
}

complex<double> calc_Ylm(int l, int m, double theta, double phi)
{
   double sintheta = sin(theta);
   double Wlmr,Wlmi,Xlmr,Xlmi;
   compute_Wlm_Xlm(l,m,theta,phi,Wlmr,Wlmi,Xlmr,Xlmi);
   
   double C=sqrt(factorial(l-2)/factorial(l+2));
   
   return complex<double>(C*( Wlmr + Xlmi/sintheta ),C*( Wlmi - Xlmr/sintheta ));
}

size_t num_modes, num_times;
vector<complex<double> > Clm;
double dt;

// TODO: automatic cutoff, wisdom, threads, proper padding
void calc_Clm(string const & filename, double r_phys, double m_adm, double cutoff_w=0.05, size_t padding=100000)
{
   // load Psi4
   DataFile<double> file;
   file.loadCSV(filename);
  cout<<"bite"; 
   // sort and remove duplicate time steps
   file.resampleCSV();
  cout << "my"; 
   // check rows and columns
   assert(file.nx>1 || file.ny>1 || file.nx%2);
  cout << "shiny";  
   dt=file[1][0]-file[0][0];
   num_times=file.ny;
   num_modes=(file.nx-1)/2 -2; //FIXME: last 4 columns are not psi4 modes
   Clm.resize(num_times*num_modes);
  cout << "metal"; 
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
            frequency_domain[i][0]=0.0;
            frequency_domain[i][1]=0.0;
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

void write_3D( string const & dirname,
               size_t nx, size_t ny, size_t nz,
               double xmin, double xmax,
               double ymin, double ymax,
               double zmin, double zmax,
               size_t dtime=1 )
{
   mkdir(dirname.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
   
   // more lookup tables
   vector<double> r(nz*ny*nx);
   vector<complex<double> > Ylm(nz*ny*nx*num_modes);
   for(size_t k=0; k<nz; k++)
   {
      double z=(zmin*(nz-1-k)+zmax*k)/(nz-1+(nz==1));
      for(size_t j=0; j<ny; j++)
      {
         double y=(ymin*(ny-1-j)+ymax*j)/(ny-1+(ny==1));
         for(size_t i=0; i<nx; i++)
         {
            double x=(xmin*(nx-1-i)+xmax*i)/(nx-1+(nx==1));
            // singularity at theta=0
            assert(x!=0.0 || y!=0.0);
            size_t kji=(k*ny+j)*nx+i;
            r[kji]=sqrt(x*x+y*y+z*z);
            double theta=acos(z/r[kji]),
                   phi=atan2(y,x);
            int l=2, m=2;
            for(size_t mode=0; mode<num_modes; mode++)
            {
               Ylm[kji*num_modes+mode]=calc_Ylm(l,m,theta,phi);
               if(m>-l)
                  --m;
               else
                  m=++l;
            }
         }
      }
   }
   
   // sample h+, hx and write to files
   #pragma omp parallel for num_threads(2*omp_get_max_threads())
   for(size_t time=0; time<num_times; time+=dtime)
   {
      DataFile<float> hp(nx,ny,nz),
                      hc(nx,ny,nz);
      for(size_t k=0; k<nz; k++)
         for(size_t j=0; j<ny; j++)
            for(size_t i=0; i<nx; i++)
            {
               size_t kji=(k*ny+j)*nx+i;
               double rtime=time-r[kji]/dt;
               if(rtime<0)
                  continue;
               size_t rt=rtime;
               double drt=rtime-rt;
               complex<double> hphc;
               //TODO uncomment for loop and comment size_t mode = 0;
               for(size_t mode=0; mode<num_modes; mode++)
                  //size_t mode = 0;
                  hphc+=(Clm[rt*num_modes+mode]*(1.0-drt)+Clm[(rt+1)*num_modes+mode]*drt)*Ylm[kji*num_modes+mode];
               hp(i,j,k)=  ReverseFloat(hphc.real()/r[kji]);
               hc(i,j,k)=  ReverseFloat(-hphc.imag()/r[kji]);
                       //int64_t __builtin_bswap64 (int64_t x)
            }
      stringstream hpname, hcname;
      hpname << dirname << "/hplus_" << time << ".vtk";
      hcname << dirname << "/hcross_" << time << ".vtk";
      #pragma omp critical(saveScalarField)
      {
         hp.saveScalarField(hpname.str(), xmin, xmax, ymin, ymax, zmin, zmax, time*dt);
         hc.saveScalarField(hcname.str(), xmin, xmax, ymin, ymax, zmin, zmax, time*dt);
      }
   }
}

void write_1D(string const & filename, double theta, double phi)
{
   DataFile<double> output;
   output.resize(3,num_times);
   // sample h+, hx and write to file
   for(size_t time=0; time<num_times; time++)
   {
      output[time][0]=time*dt;
      int l=2, m=2;
      complex<double> hphc;
      for(size_t mode=0; mode<num_modes; mode++)
      {
         hphc+=Clm[time*num_modes+mode]*calc_Ylm(l,m,theta,phi);
         if(m>-l)
            --m;
         else
            m=++l;
      }
      output[time][1]=hphc.real();
      output[time][2]=-hphc.imag();
   }
   output.saveCSV(filename);
}
/*template <typename T> 
void swap_endian(T& pX)
{
        // should static assert that T is a POD
             char& raw = reinterpret_cast<char&>(pX);
                 std::reverse(&raw, &raw + sizeof(T));
                 }
                 */
int main (int argc, const char *argv[])
{
   //NOTE: choose these carefully to avoid singularity at theta=0
   size_t n=150;//number of points
   double min=0.001,
          max=75;//Maximum dimension
   
   //cout << "Calculating Clms...\n";
   //calc_Clm("Psi4_rad.mon.sort.3", 60.1277102551413, 1.0); //TODO (filename, radius, ADM mass)
   
   
   //cout << "3D test...\n";
   //write_3D("3D",n,n,n/2,-max,max,-max,max,-max,0,1);

	//cout << "1D test...\n";
	//write_1D("1D",3.14159265368979/4.0,0.0);

	cout << "Calculating Clms...\n";
	//calc_Clm("Psi4_rad.mon.thin.sort.5", 77.9258507826028, 1.0);
	//calc_Clm("Psi4_rad.mon.sort.1", 48.948052762078, 1.0);
	//calc_Clm("Psi4_rad.mon.sort.9", 191.0, 1.0);
	//calc_Clm("Psi4_rad.mon.sort.7", 110.69101357243, 1.0);
	calc_Clm("Psi4_rad.mon.sort.5", 77.9258507826028, 1.0); //TODO (filename, radius, ADM mass)

	cout << "1D test...\n";
	write_1D("1D",3.14159265368979/4.0,0.0);

	//cout << "3D test...\n";
	//write_3D("3D",n,n,n/2,-max,max,-max,max,-max,0,1);
   
   return 0;
}
