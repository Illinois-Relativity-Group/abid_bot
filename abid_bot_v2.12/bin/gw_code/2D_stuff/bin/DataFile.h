#ifndef DATAFILE_H_
#define DATAFILE_H_
#include <string>
#include <utility>
#include <vector>

template <typename T>
class DataFile
{
public:
   size_t nx, // number of columns
          ny, // number of rows
          nz;
   std::vector<T> data;
   
   // allocates and fills array with c
   DataFile(size_t nx=0, size_t ny=1, size_t nz=1, T c=0.0);
   
   // loads data
   DataFile(std::string const & filename, size_t stride=1);
   std::vector<std::pair<size_t,std::string> > loadCSV(std::string const & filename);
   
   // manipulates data
   T* operator[](size_t j);
   T& operator()(size_t i, size_t j=0, size_t k=0);
   std::vector<T> resampleCSV(size_t stride=1);
   void resize(size_t nx=0, size_t ny=1, size_t nz=1, T c=0.0);
   void clear();
   
   // saves data
   void saveCSV(std::string const & filename, std::vector<std::pair<size_t,std::string> > const & headers=std::vector<std::pair<size_t,std::string> >()) const;
   void saveCluster(std::string const & filename, double time=0.0) const;
   void saveScalarField(std::string const & filename,
                           double xmin, double xmax,
                           double ymin, double ymax,
                           double zmin, double zmax,
                           double time=0.0 ) const;
   void saveVectorField(std::string const & filename,
                           double xmin, double xmax,
                           double ymin, double ymax,
                           double zmin, double zmax,
                           double time=0.0 ) const;
   
   // helper function
   static bool is_little_endian();
};
#endif
