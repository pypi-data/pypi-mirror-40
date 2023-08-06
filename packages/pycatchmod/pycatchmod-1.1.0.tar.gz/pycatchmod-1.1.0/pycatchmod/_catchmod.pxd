from libc.math cimport exp, atan, tan, sin, acos, cos, fabs, sqrt, M_PI

cdef class Catchment:
    cdef public basestring name
    cdef public list subcatchments

    cpdef reset(self)
    cpdef int step(self, double[:] rainfall, double[:] pet, double[:, :] percolation, double[:, :] outflow) except -1


cdef class OudinCatchment:
    """
    """
    cdef public basestring name
    cdef public list subcatchments
    cdef public double latitude

    cpdef reset(self)
    cpdef int step(self, int day_of_year, double[:] rainfall, double[:] temperature, double[:] pet,
               double[:, :] percolation, double[:, :] outflow) except -1
