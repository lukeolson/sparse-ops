import sys
import pyamg
import numpy as np
import sparse
import argparse
from timeit import default_timer as timer

try:
    import omp_thread_count
    nt = omp_thread_count.get_thread_count()
except ImportError:
    raise ImportError('Need omp_thread_count installed...')

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x, *args, **kwargs):
        return x


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Timing tests for w = A * v")
    p.add_argument("--scipy", action="store_true")
    p.add_argument("--pybind", action="store_true")
    p.add_argument("--pybind-omp", action="store_true")
    p.add_argument("--save", action="store_true")
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    test_scipy = args.scipy
    test_pybind = args.pybind
    test_pybind_omp = args.pybind_omp
    save = args.save
    plotit = args.plot

    ntests = 100
    size = int(4e6)
    A = pyamg.gallery.poisson((size,), format='csr')
    n = A.shape[0]

    np.random.seed(23957)
    v = np.random.rand(n)
    V = np.random.rand(n, 2)
    w = A * v

    try:
        w2 = np.zeros((A.shape[0],))
        sparse.csr_matvec(n, n, A.indptr, A.indices, A.data, v, w2)
        np.testing.assert_array_max_ulp(w, w2)
        print('...testing pybind passed')
    except AssertionError:
        sys.exit(1)
        print('... pybind did NOT pass')

    try:
        w3 = np.zeros((A.shape[0],))
        sparse.csr_matvec(n, n, A.indptr, A.indices, A.data, v, w3)
        np.testing.assert_array_max_ulp(w, w3)
        print('...testing pybind-omp passed with {} threads'.format(nt))
    except AssertionError:
        print('... pybind-omp did NOT pass')

    flops = A.nnz * np.ones((ntests,))
    times_scipy = np.zeros((ntests,))
    times_pybind = np.zeros((ntests,))
    times_pybind_omp = np.zeros((ntests,))

    if test_scipy:
        print("...testing scipy with {} runs".format(ntests))
        for i in tqdm(range(ntests)):
            t0 = timer()
            w = A * v
            t1 = timer()
            times_scipy[i] = t1 - t0

        if save:
            np.save("data-scipy.npy", times_scipy)

    if test_pybind:
        print("...testing pybind with {} runs".format(ntests))
        for i in tqdm(range(ntests)):
            t0 = timer()
            sparse.csr_matvec(n, n, A.indptr, A.indices, A.data, v, w2)
            t1 = timer()
            times_pybind[i] = t1 - t0

        if save:
            np.save("data-pybind.npy", times_pybind)

    if test_pybind_omp:
        print("...testing pybind-omp with {} runs".format(ntests))
        for i in tqdm(range(ntests)):
            t0 = timer()
            sparse.csr_matvec_omp(n, n, A.indptr, A.indices, A.data, v, w3)
            t1 = timer()
            times_pybind_omp[i] = t1 - t0

        if save:
            np.save("data-pybind-omp-{}.npy".format(nt), times_pybind_omp)

    if plotit:
        import matplotlib.pyplot as plt
        if test_scipy:
            plt.plot(times_scipy, label='scipy.sparse')
        if test_pybind:
            plt.plot(times_pybind, label='pybind11')
        if test_pybind_omp:
            plt.plot(times_pybind_omp, label='pybind11 + OMP')
        plt.legend()
        plt.show()
