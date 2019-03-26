// https://www.shoup.net/ntl/doc/tour-ex5.html

#include <iostream>
#include <NTL/GF2XFactoring.h>

using namespace std;
using namespace NTL;

int main()
{
  const long maxBits = 1024;
  std::cout << "gPrimitivePolysCondensed = {" << std::endl;
  std::cout << "    1 : (1,0), # x+1" << std::endl;
  for (long bits = 2; bits <= maxBits; ++bits) {
    GF2X poly;
    BuildSparseIrred(poly,bits);
    long d = deg(poly);

    std::cout << "    " << d << " : (" << d;
    for (long k = d-1; k >= 0; --k) {
      GF2 c = coeff(poly,k);
      if (IsOne(c)) { std::cout << "," << k; }
    }

    std::cout << ")" << (bits < maxBits ? "," : "") << " # ";

    std::cout << "x^" << d;
    for (long k = d-1; k >= 0; --k) {
      GF2 c = coeff(poly,k);
      if (IsOne(c)) {
	if (k > 1) {
	  cout << "+x^" << k;
	} else if (k == 1) {
	  cout << "+x";
	} else if (k == 0) {
	  cout << "+1";
	}
      }
    }
    std::cout << std::endl;
  }
  std::cout << "} # gPrimitivePolysCondensed" << std::endl;
}
