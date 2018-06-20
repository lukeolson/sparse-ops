from scipy.sparse import csr_matrix, _sparsetools
from scipy.sparse.sputils import upcast_char
import sparse
import numpy as np
from timeit import default_timer as timer 
import pyamg


class mycsr(csr_matrix):
    """
    *OpenMP Enabled*
    """
    def _mul_vector(self, other):
        M, N = self.shape

        # output array
        result = np.zeros(M, dtype=upcast_char(self.dtype.char,
                                               other.dtype.char))

        # csr_matvec or csc_matvec
        sparse.csr_matvec(M, N, self.indptr, self.indices, self.data, other, result)

        return result


mycsr.__doc__ += csr_matrix.__doc__

if __name__ == '__main__':
    nx = int(1e2)
    A = pyamg.gallery.poisson((nx, nx), format='csr').tocoo().tocsr()
    b = np.random.rand(A.shape[0])

    print(id(A.indices))
    w = A * b
    print(id(A.indices))
    # A2 = mycsr(A)
    # w2 = A2 * b
    M, N = A.shape
    result = np.zeros(M,)  # dtype=upcast_char(A.dtype.char, b.dtype.char))
    sparse.csr_matvec(M, N, A.indptr, A.indices, A.data, b, result)
    print(id(A.indices))

    ml = pyamg.smoothed_aggregation_solver(A, max_coarse=10)
    print(ml)
