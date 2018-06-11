// DO NOT EDIT: this file is generated

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/complex.h>

#include "sparse.h"

namespace py = pybind11;

template <class I, class T>
void _csr_matvec_omp(
            const I n_row,
            const I n_col,
      py::array_t<I> & Ap,
      py::array_t<I> & Aj,
      py::array_t<T> & Ax,
      py::array_t<T> & Xx,
      py::array_t<T> & Yx
                     )
{
    auto py_Ap = Ap.unchecked();
    auto py_Aj = Aj.unchecked();
    auto py_Ax = Ax.unchecked();
    auto py_Xx = Xx.unchecked();
    auto py_Yx = Yx.mutable_unchecked();
    const I *_Ap = py_Ap.data();
    const I *_Aj = py_Aj.data();
    const T *_Ax = py_Ax.data();
    const T *_Xx = py_Xx.data();
    T *_Yx = py_Yx.mutable_data();

    return csr_matvec_omp <I, T>(
                    n_row,
                    n_col,
                      _Ap, Ap.size(),
                      _Aj, Aj.size(),
                      _Ax, Ax.size(),
                      _Xx, Xx.size(),
                      _Yx, Yx.size()
                                 );
}

template <class I, class T>
void _csr_matvec(
            const I n_row,
            const I n_col,
      py::array_t<I> & Ap,
      py::array_t<I> & Aj,
      py::array_t<T> & Ax,
      py::array_t<T> & Xx,
      py::array_t<T> & Yx
                 )
{
    auto py_Ap = Ap.unchecked();
    auto py_Aj = Aj.unchecked();
    auto py_Ax = Ax.unchecked();
    auto py_Xx = Xx.unchecked();
    auto py_Yx = Yx.mutable_unchecked();
    const I *_Ap = py_Ap.data();
    const I *_Aj = py_Aj.data();
    const T *_Ax = py_Ax.data();
    const T *_Xx = py_Xx.data();
    T *_Yx = py_Yx.mutable_data();

    return csr_matvec <I, T>(
                    n_row,
                    n_col,
                      _Ap, Ap.size(),
                      _Aj, Aj.size(),
                      _Ax, Ax.size(),
                      _Xx, Xx.size(),
                      _Yx, Yx.size()
                             );
}

PYBIND11_MODULE(sparse, m) {
    m.doc() = R"pbdoc(
    Pybind11 bindings for sparse.h

    Methods
    -------
    csr_matvec_omp
    csr_matvec
    )pbdoc";

    py::options options;
    options.disable_function_signatures();

    m.def("csr_matvec_omp", &_csr_matvec_omp<int, float>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert());
    m.def("csr_matvec_omp", &_csr_matvec_omp<int, double>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert());
    m.def("csr_matvec_omp", &_csr_matvec_omp<int, std::complex<float>>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert());
    m.def("csr_matvec_omp", &_csr_matvec_omp<int, std::complex<double>>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert(),
R"pbdoc(
Threaded SpMV

y <- A * x

Parameters
----------
n_row, n_col : int
   dimensions of the n_row x n_col matrix A
Ap, Aj, Ax : array
   CSR pointer, index, and data vectors for matrix A
Xx : array
   input vector
Yy : array
   output vector (modified in-place)

See Also
--------
csr_matvec

Notes
-----
Requires GCC 4.9 for ivdep
Requires a compiler with OMP)pbdoc");

    m.def("csr_matvec", &_csr_matvec<int, float>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert());
    m.def("csr_matvec", &_csr_matvec<int, double>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert());
    m.def("csr_matvec", &_csr_matvec<int, std::complex<float>>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert());
    m.def("csr_matvec", &_csr_matvec<int, std::complex<double>>,
        py::arg("n_row"), py::arg("n_col"), py::arg("Ap").noconvert(), py::arg("Aj").noconvert(), py::arg("Ax").noconvert(), py::arg("Xx").noconvert(), py::arg("Yx").noconvert(),
R"pbdoc(
Reference SpMV from scipy

y <- A * x

Parameters
----------
n_row, n_col : int
   dimensions of the n_row x n_col matrix A
Ap, Aj, Ax : array
   CSR pointer, index, and data vectors for matrix A
Xx : array
   input vector
Yy : array
   output vector (modified in-place)

See Also
--------
csr_matvec_omp

Notes
-----
Requires GCC 4.9 for ivdep
Requires a compiler with OMP)pbdoc");

}

