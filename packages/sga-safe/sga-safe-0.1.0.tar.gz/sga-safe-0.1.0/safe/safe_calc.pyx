# cython: language_level=3
import numpy as np
cimport numpy as np


cdef extern from "safe.cpp":
    cdef extern void safe(long* data, double* enrichment, unsigned int* Fj, long* neighbours, int m, int n)


cpdef calculate(const long[:, :] data, unsigned int[:] Fj, long[:] neighbours):
    cdef int m, n
    cdef np.ndarray[np.double_t, ndim=2, mode="c"] enriched

    m = data.shape[0]
    n = data.shape[1]

    enriched = np.zeros((m, n), dtype=np.double)
    safe(&data[0, 0], &enriched[0, 0], &Fj[0], &neighbours[0], m, n)

    return enriched
