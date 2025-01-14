#include <iomanip>
#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>

#include "shtools.h"

/*
 * This is a very simple example, explaining how to use the c/cpp interface
 *
 * By default arguments in Fortran are passed by reference and in c/cpp by
 * value. To pass a reference to Fortran get the pointer with the address-of
 * operator: &
 *
 * A lot of the fortran subroutines have optional arguments. In c/c++ optional
 * arguments in arbitrary order are not possible. You can use nullptr, which is
 * equivalent to not specifying the argument in fortran.
 * 
 *
 */

int
main(int argc, char** argv)
{

  std::string infile;

  int lmax = 15;
  int cilm_dim = lmax + 1;

  // In Fortran Cilm has the dimension 2 x cilm_dim x cilm_dim
  // In the C interface we always use 1-D arrays
  std::vector<double> cilm(2 * cilm_dim * cilm_dim);
  
  int exitstatus;

  if( argc > 1 ){
    infile = argv[1];
  } else {
    infile = "../ExampleDataFiles";
  }
  infile += "/MarsTopo719.shape";
  shtools::SHRead(infile.c_str(),
                   infile.size(),
                   &cilm[0],
                   cilm_dim,
                   &lmax,
                   nullptr,
                   nullptr,
                   0,
                   nullptr,
                   &exitstatus);
  
  std::cerr << "SHRead exit status: " << exitstatus << std::endl;
  
  // convert to 'vector' format and print
  std::vector<double> index(cilm_dim*cilm_dim);
  shtools::SHCilmToVector(&cilm[0],cilm_dim,&index[0],lmax, &exitstatus);
  std::cerr << "SHCilmToVector exit status: " << exitstatus << std::endl;
  for(double d : index )
      std::cerr << d << " ";
  std::cerr << std::endl;
  
  double lat = 10.0;
  double lon = 30.0;

  // Here the optional arguments norm, csphase, dealloc are null pointers.
  // Thus, they are not used. 
  double val = shtools::MakeGridPoint(
    &cilm[0], cilm_dim, lmax, lat, lon, nullptr, nullptr, nullptr);

  double diff = val - 3395259.548270001;
  std::cout << "diff to python " << diff << std::endl;

  if( std::abs(diff) > 1e-9 ){
    return 1;
  }
  return 0;
}
