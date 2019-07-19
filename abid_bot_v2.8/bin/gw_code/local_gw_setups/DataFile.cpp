#include <fstream>
#include <iterator>
#include <sstream>
#include <cmath>
#include "DataFile.h"
using namespace std;

template <typename T>
DataFile<T>::DataFile(size_t nx, size_t ny, size_t nz, T c) :
   nx(nx), ny(ny), nz(nz), data(nx*ny*nz,c)
{
}

template <typename T>
DataFile<T>::DataFile(string const & filename, size_t stride)
{
   loadCSV(filename);
   resampleCSV(stride);
}

template <typename T>
vector<pair<size_t,string> > DataFile<T>::loadCSV(string const & filename)
{
   ifstream ifs(filename.c_str());
   vector<pair<size_t,string> > headers;
   string line;
   clear();
   while(getline(ifs,line))
   {
      size_t start=line.find_first_not_of(" \t");
      if(start==string::npos)
         continue;
      if(line[start]=='#')
      {
         headers.push_back(pair<size_t,string>(ny+headers.size(),line));
         continue;
      }
      ny++;
      stringstream ss(line);
      copy(istream_iterator<T>(ss),
           istream_iterator<T>(),
           back_inserter<vector<T> >(data) );
   }
   if(ny==0)
      ny=1;
   nx=data.size()/ny;
   nz=1;
   ifs.close();
   return headers;
}

template <typename T>
T* DataFile<T>::operator[](size_t j)
{
   return &data[j*nx];
}

template <typename T>
T& DataFile<T>::operator()(size_t i, size_t j, size_t k)
{
   return data[i+nx*(j+ny*k)];
}

template <typename T>
vector<T> DataFile<T>::resampleCSV(size_t stride)
{
   // assumes first and second time step are correct
   T dt=(data[nx]-data[0])*stride;
   size_t num_times=(data[(ny-1)*nx]-data[0])/dt+1.5;
   vector<T> new_data(nx*num_times);
   size_t previous_row=0;
   for(size_t row=0; row<ny; row++)
   {
      size_t new_row=(data[row*nx]-data[0])/dt+0.5;
      // remove duplicate time steps
      for(size_t col=0; col<nx; col++)
         new_data[new_row*nx+col]=data[row*nx+col];
      // interpolate missing time steps
      for(size_t i=previous_row+1; i<new_row; i++)
      {
         T A=T(new_row-i)/(new_row-previous_row),
               B=T(i-previous_row)/(new_row-previous_row);
         for(size_t col=0; col<nx; col++)
            new_data[i*nx+col]=A*new_data[previous_row*nx+col]+B*new_data[new_row*nx+col];
      }
      previous_row=new_row;
   }
   data.swap(new_data);
   ny=num_times;
   return new_data;
}

template <typename T>
void DataFile<T>::resize(size_t pnx, size_t pny, size_t pnz, T c)
{
   nx=pnx;
   ny=pny;
   nz=pnz;
   data.resize(pnx*pny*pnz,c);
}

template <typename T>
void DataFile<T>::clear()
{
   nx=0;
   ny=0;
   nz=0;
   vector<T>().swap(data);
}


template <typename T>
void DataFile<T>::saveCSV(string const & filename, vector<pair<size_t,string> > const & headers) const
{
   ofstream ofs(filename.c_str());
   ofs.setf(ios::scientific);
   ofs.precision(15);
   size_t dj=0;
   for(size_t j=0; j<ny+headers.size(); j++)
   {
      if(dj==headers.size() || j-dj!=headers[dj].first)
      {
         for(size_t i=0; i<nx-1; i++)
            ofs << data[i+nx*(j-dj)] << '\t';
         ofs << data[nx*(j-dj+1)-1] << '\n';
      } else
         ofs << headers[dj++].second << '\n';
   }
   ofs << '\n';
}

template <>
void DataFile<float>::saveCluster(string const & filename, double time) const
{
   ofstream ofs(filename.c_str());
   ofs << "# AmiraMesh BINARY" << (is_little_endian()?"-LITTLE-ENDIAN":"") << " 1.0\n"
          "\n"
          "define Points " << data.size()/3 << "\n"
          "\n"
          "Parameters {\n"
          "    ContentType \"HxCluster\",\n"
          "    Time " << time << "\n"
          "}\n"
          "\n"
          "Points { float[3] Coordinates } @1\n"
          "\n"
          "@1\n";
   ofs.write(reinterpret_cast<const char*>(&data[0]), data.size() * sizeof(float));
}

template <>
void DataFile<float>::saveScalarField(string const & filename,
                                  double xmin, double xmax,
                                  double ymin, double ymax,
                                  double zmin, double zmax,
                                  double time ) const
{
   ofstream ofs(filename.c_str());
   ofs << "# vtk DataFile Version 2.0\n"
          "Some kind of wizard  \n"
          "BINARY\n"
          "DATASET STRUCTURED_POINTS\n"
          "DIMENSIONS " << nx << ' ' << ny << ' ' << nz << "\n"
          "ORIGIN " << xmin << ' ' << ymin << ' ' << zmin << "\n"
          "SPACING " << double((abs(xmin) + abs(xmax))/(nx)) << ' '  << double((abs(ymin) + abs(ymax))/(ny)) << ' ' << double( (abs(zmin) + abs(zmax))/(nz) )<< "\n"
          "POINT_DATA " << nx*ny*nz << "\n"
         // "TIME 1 1 float " << time << "\n"
          "SCALARS GW-FIELD float 1\n"
          "LOOKUP_TABLE default\n";
   ofs.write(reinterpret_cast<const char*>(&data[0]), data.size() * sizeof(float));
}

template <>
void DataFile<float>::saveVectorField(string const & filename,
                                  double xmin, double xmax,
                                  double ymin, double ymax,
                                  double zmin, double zmax,
                                  double time ) const
{
   ofstream ofs(filename.c_str());
   ofs << "# AmiraMesh BINARY" << (is_little_endian()?"-LITTLE-ENDIAN":"") << " 1.0\n"
          "\n"
          "define Lattice " << nx/3 << ' ' << ny << ' ' << nz << "\n"
          "\n"
          "Parameters {\n"
          "    CoordType \"uniform\",\n"
          "    BoundingBox " << xmin << ' ' << xmax << ' ' << ymin << ' ' << ymax << ' ' << zmin << ' ' << zmax << ",\n"
          "    Time " << time << "\n"
          "}\n"
          "\n"
          "Lattice { float[3] VectorField } = @1\n"
          "\n"
          "@1\n";
   ofs.write(reinterpret_cast<const char*>(&data[0]), data.size() * sizeof(float));
}

template <typename T>
bool DataFile<T>::is_little_endian()
{
   union {
      T d;
      unsigned char c[sizeof(T)];
   } dc = {0.0};

    return dc.c[0] == 0; 
}

template class DataFile<float>;
template class DataFile<double>;
