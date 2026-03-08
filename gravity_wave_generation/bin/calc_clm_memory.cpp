#include <cassert>
#include <cmath>
#include <complex>
#include <iostream>
#include <vector>
#include <algorithm>

#ifdef _OPENMP
#include <omp.h>
#endif
#include <sys/stat.h>
#include <fftw3.h>

#include "DataFile.h"
using namespace std;

// Polynomial interpolation (Numerical Recipes polint port)
// Given xa[0..n-1], ya[0..n-1], compute y at x, with error estimate dy
void polint(const vector<double>& xa, const vector<double>& ya, double x, double &y) {
    int n = xa.size();
    vector<double> c(ya), d(ya);
    int ns = 0;
    double dif = fabs(x - xa[0]);
    for (int i = 1; i < n; ++i) {
        double dift = fabs(x - xa[i]);
        if (dift < dif) { ns = i; dif = dift; }
        c[i] = ya[i]; d[i] = ya[i];
    }
    y = ya[ns];
    ns--;
    for (int m = 1; m < n; ++m) {
        for (int i = 0; i < n - m; ++i) {
            double ho = xa[i] - x;
            double hp = xa[i+m] - x;
            double w = c[i+1] - d[i];
            double den = ho - hp;
            assert(den != 0.0);
            den = w / den;
            d[i] = hp * den;
            c[i] = ho * den;
        }
        if (2*ns < (n - m)) {
            y += c[ns+1];
        } else {
            y += d[ns];
            ns--;
        }
    }
}

void get_lm(size_t mode_idx, int &l, int &m) {
    l = 2;
    size_t idx = mode_idx;
    while (idx >= (size_t)(2*l+1)) {
        idx -= (2*l + 1);
        l++;
    }
    m = (int)idx - l;
}

size_t num_modes, num_times;
vector<complex<double>> Clm;
double dt;
double r_phys;

void calc_Clm(string const & filename, double m_adm, double cutoff_w=0.05, size_t padding=100000) {
    // Load CSV and remove duplicates
    DataFile<double> file;
    file.loadCSV(filename);
    file.resampleCSV();

    // basic parameters
    num_times = file.ny;
    dt = file[1][0] - file[0][0];
    num_modes = (file.nx - 1)/2 - 2;  // last 4 columns: r, gtt, gtr, grr

    // read extraction radius and metric components per time step
    vector<double> R_arr(num_times), gtt(num_times), gtr(num_times), grr(num_times);
    vector<double> tret_arr(num_times), tsch_arr(num_times);

    // allocate storage for r*psi4
    vector<vector<complex<double>>> psi4_modes(num_modes, vector<complex<double>>(num_times));

    for (size_t i = 0; i < num_times; ++i) {
        R_arr[i]   = file[i][file.nx-4];
        gtt[i]     = file[i][file.nx-3];
        gtr[i]     = file[i][file.nx-2];
        grr[i]     = file[i][file.nx-1];
        // r*Psi4 for each mode
        for (size_t mode = 0; mode < num_modes; ++mode) {
            double re = file[i][1+2*mode];
            double im = file[i][2+2*mode];
            psi4_modes[mode][i] = complex<double>(re*R_arr[i], -im*R_arr[i]);
        }
    }

    // compute Schwarzschild time and retarded time arrays
    double tsch = file[0][0];
    double dtc0 = 0.0;
    // initial dtc0
    dtc0 = (gtr[0] - sqrt(gtr[0]*gtr[0] - gtt[0]*grr[0]))
           / gtt[0] / (1.0 - 2.0*m_adm/R_arr[0]) * dt;
    for (size_t i = 0; i < num_times; ++i) {
        if (i > 0) {
            double dtc1 = (gtr[i] - sqrt(gtr[i]*gtr[i] - gtt[i]*grr[i]))
                          / gtt[i] / (1.0 - 2.0*m_adm/R_arr[i]) * dt;
            tsch += 0.5*(dtc0 + dtc1);
            dtc0 = dtc1;
        }
        double rstar = R_arr[i] + 2.0*m_adm * log(R_arr[i]/(2.0*m_adm) - 1.0);
        tret_arr[i] = tsch - rstar;
    }

    // define interpolation window based on tret_arr
    double tret_start = tret_arr.front(), tret_end = tret_arr.back();

    // FFT parameters
    size_t n = num_times;
    size_t nn = 1; while (nn < n) nn <<= 1;  // next power of 2
    size_t padded = nn + 2*padding;

    Clm.assign(num_modes * n, complex<double>(0,0));

    // temporary buffers
    fftw_complex *td = (fftw_complex*)fftw_malloc(sizeof(fftw_complex)*padded);
    fftw_complex *fd = (fftw_complex*)fftw_malloc(sizeof(fftw_complex)*padded);

    for (size_t mode = 0; mode < num_modes; ++mode) {
        // zero padding
        for (size_t i = 0; i < padded; ++i)
            td[i][0] = td[i][1] = 0.0;

        // interpolate psi4_modes[mode] onto uniform retarded-time grid
        vector<double> xa(4), ya(4);
        for (size_t i = 0; i < n; ++i) {
            double t_unif = tret_start + dt * i;
            // find interval
            size_t k = 0;
            for (size_t j = 0; j+1 < n; ++j) {
                if (tret_arr[j] <= t_unif && t_unif < tret_arr[j+1]) { k = j; break; }
            }
            // pick 4 points around k
            size_t istart = (k >= 1 ? k-1 : 0);
            istart = min(istart, n-4);
            for (int p = 0; p < 4; ++p) {
                xa[p] = tret_arr[istart + p];
                ya[p] = psi4_modes[mode][istart + p].real();
            }
            double real_interp; polint(xa, ya, t_unif, real_interp);
            for (int p = 0; p < 4; ++p) {
                ya[p] = psi4_modes[mode][istart + p].imag();
            }
            double imag_interp; polint(xa, ya, t_unif, imag_interp);
            td[padding + i][0] = real_interp;
            td[padding + i][1] = imag_interp;
        }

        // FFT forward
        fftw_plan p_fwd = fftw_plan_dft_1d(padded, td, fd, FFTW_FORWARD, FFTW_ESTIMATE);
        fftw_execute(p_fwd);

        // frequency-domain integration
        double c = r_phys/(m_adm * padded);
        double dw = 2.0*M_PI/(dt*padded);
        for (size_t i = 0; i < padded; ++i) {
            int i2 = (i <= padded/2) ? (int)i : (int)i - (int)padded;
            double w = i2 * dw;

            int l,m;
            get_lm(mode, l, m);
            double wcut = max(fabs(m)*cutoff_w, cutoff_w);
            double fact = (fabs(w) < wcut ? -c/(wcut*wcut) : -c/(w*w));
            fd[i][0] *= fact;
            fd[i][1] *= fact;
        }

        // FFT backward
        fftw_plan p_bwd = fftw_plan_dft_1d(padded, fd, td, FFTW_BACKWARD, FFTW_ESTIMATE);
        fftw_execute(p_bwd);

        // normalize and store
        for (size_t i = 0; i < n; ++i) {
            complex<double> val(td[padding + i][0], td[padding + i][1]);
            Clm[i*num_modes + mode] = val / (double)padded;
        }

        fftw_destroy_plan(p_bwd);
        fftw_destroy_plan(p_fwd);
    }

    fftw_free(td);
    fftw_free(fd);
}

void write_simple_Clm(string const & filename) {
    DataFile<double> out;
    out.resize(1+2*(int)num_modes, (int)num_times);
    for (size_t i = 0; i < num_times; ++i) {
        out[i][0] = dt * i;
        for (size_t mode = 0; mode < num_modes; ++mode) {
            auto c = Clm[i*num_modes + mode];
            out[i][1+2*mode] = c.real();
            out[i][1+2*mode+1] = c.imag();
        }
    }
    out.saveCSV(filename);
}

int main(int argc, const char* argv[]) {
    assert(argc==5);
    string filename = argv[1];
    double ADM_M = stod(argv[2]);
    double cutoff_w = stod(argv[3]);
    string outdir = argv[4];
    calc_Clm(filename, ADM_M, cutoff_w);
    write_simple_Clm(outdir + "/Clm_with_time.dat");
    return 0;
}
