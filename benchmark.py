import sys
import numpy as np
import sparse
import argparse
from timeit import default_timer as timer
import os
import subprocess
import scipy.io as sio
import scipy.sparse

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
    p.add_argument("--scipy", action="store_true",
                   help="Test the scipy implementation")
    p.add_argument("--ref", action="store_true",
                   help="Test the reference implementation (no OpenMP)")
    p.add_argument("--omp", action="store_true",
                   help="Test the OpenMP implementation")
    p.add_argument("--save",
                   nargs='?', const='data.out', default=False,
                   help="Save the results in a .npz file")
    p.add_argument("--plot", action="store_true",
                   help="A simple plot")
    p.add_argument("--matrix", nargs=1,
                   help="cant, mc2depi, rbs480a, or yourown.mat")
    args = p.parse_args()

    test_scipy = args.scipy
    test_ref = args.ref
    test_omp = args.omp
    save = args.save
    plotit = args.plot
    matrix = args.matrix

    ntests = 100

    if matrix == 'cant':
        f = os.path.join('data-input', 'cant.mat')
        if not os.path.isfile(f):
            subprocess.call(['wget', '--directory-prefix=data-input', 'https://www.cise.ufl.edu/research/sparse/mat/Williams/cant.mat'])
        mat = sio.loadmat(f)
        A = mat['Problem'][0][0][2].tocsr()
    elif matrix == 'mc2depi':
        f = os.path.join('data-input', 'mc2depi.mat')
        if not os.path.isfile(f):
            subprocess.call(['wget', '--directory-prefix=data-input', 'https://www.cise.ufl.edu/research/sparse/mat/Williams/mc2depi.mat'])
        mat = sio.loadmat(f)
        A = mat['Problem'][0][0][2].tocsr()
    elif matrix == 'rbs480a':
        f = os.path.join('data-input', 'rbs480a.mtx.gz')
        if not os.path.isfile(f):
            subprocess.call(['wget', '--directory-prefix=data-input', 'ftp://math.nist.gov/pub/MatrixMarket2/NEP/robotics/rbs480a.mtx.gz'])
        A = sio.mmread(f).tocsr()
    elif matrix is None:
        size = int(4e6)
        data = np.ones((5, size))
        diags = np.arange(-2, 3)
        A = scipy.sparse.spdiags(data, diags, size, size).tocsr()
        matrix = 'pyamg'
    else:
        f = os.path.join('data-input', matrix)
        A = sio.loadmat(f)['A']

    n = A.shape[0]
    np.random.seed(23957)
    v = np.random.rand(n)
    V = np.random.rand(n, 2)
    w = A * v

    try:
        w2 = np.zeros((A.shape[0],))
        sparse.csr_matvec(n, n, A.indptr, A.indices, A.data, v, w2)
        np.testing.assert_array_max_ulp(w, w2)
        print('...testing reference passed')
    except AssertionError:
        sys.exit(1)
        print('... reference did NOT pass')

    try:
        w3 = np.zeros((A.shape[0],))
        sparse.csr_matvec(n, n, A.indptr, A.indices, A.data, v, w3)
        np.testing.assert_array_max_ulp(w, w3)
        print('...testing OMP passed with {} threads'.format(nt))
    except AssertionError:
        print('... OMP did NOT pass')

    if save:
        datadir = os.path.join(os.getcwd(), save)
        os.makedirs(datadir, exist_ok=True)

    flops = A.nnz * np.ones((ntests,))
    times_scipy = np.zeros((ntests,))
    times_ref = np.zeros((ntests,))
    times_omp = np.zeros((ntests,))

    if test_scipy:
        print("...testing scipy with {} runs".format(ntests))
        for i in tqdm(range(ntests)):
            t0 = timer()
            w = A * v
            t1 = timer()
            times_scipy[i] = t1 - t0

        if save:
            np.savez(os.path.join(datadir, "data-scipy.npz"),
                     times=times_scipy, flops=flops)

    if test_ref:
        print("...testing reference with {} runs".format(ntests))
        for i in tqdm(range(ntests)):
            t0 = timer()
            sparse.csr_matvec(n, n, A.indptr, A.indices, A.data, v, w2)
            t1 = timer()
            times_ref[i] = t1 - t0

        if save:
            np.savez(os.path.join(datadir, "data-ref.npz"),
                     times=times_ref, flops=flops)

    if test_omp:
        print("...testing OpenMP with {} runs".format(ntests))
        for i in tqdm(range(ntests)):
            t0 = timer()
            sparse.csr_matvec_omp(n, n, A.indptr, A.indices, A.data, v, w3)
            t1 = timer()
            times_omp[i] = t1 - t0

        if save:
            np.savez(os.path.join(datadir, "data-omp-{}.npz".format(nt)),
                     times=times_omp, flops=flops)

    if plotit:
        import matplotlib.pyplot as plt
        if test_scipy:
            plt.plot(times_scipy, label='scipy.sparse')
        if test_ref:
            plt.plot(times_ref, label='reference')
        if test_omp:
            plt.plot(times_omp, label='reference with OpenMP')
        plt.legend()
        plt.show()
