/**
MIT License

Copyright (c) 2017 Matej Ušaj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include <algorithm>
#include <gsl/gsl_cdf.h>
#include <iostream>

void safe(const long* data,
          double* enrichment,
          unsigned int* Fj,
          long* neighbours,
          int m, int n) {
    const double eps = -log10(.05 / n) / 16.;

    int i, j, datIdx;
    double cdf, normcdf;

    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            datIdx = i * n + j;
            if (data[datIdx] == 0) continue;

            cdf = 1 - gsl_cdf_hypergeometric_P(data[datIdx] - 1, Fj[j], m - Fj[j], neighbours[i]);

            normcdf = -log10(cdf);
            normcdf = isinf(normcdf) ? 16. : normcdf;

            normcdf = std::min(normcdf, 16.) / 16.;

            if (normcdf < eps || cdf > 0.05) normcdf = 0.;

            enrichment[datIdx] = normcdf;
        }
    }
}
