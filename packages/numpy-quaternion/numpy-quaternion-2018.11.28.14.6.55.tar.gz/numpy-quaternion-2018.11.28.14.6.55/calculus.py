# Copyright (c) 2017, Michael Boyle
# See LICENSE file for details: <https://github.com/moble/quaternion/blob/master/LICENSE>

from __future__ import division, print_function, absolute_import
import numpy as np
from quaternion.numba_wrapper import njit, jit, xrange


try:

    from scipy.interpolate import InterpolatedUnivariateSpline as spline

    def interpolate(f, t, t_new, axis=None, spline_order=3, derivative_order=0):
        import numpy as np
        from numpy.core.multiarray import normalize_axis_index
        from scipy.interpolate import InterpolatedUnivariateSpline as spline
        dtype = f.dtype
        if axis is None:
            axis = list(f.shape).index(t.size)
        axis = normalize_axis_index(axis, f.ndim)
        if dtype == np.dtype(complex):
            f = f.view((float, 2))
        f = np.swapaxes(f, axis, -1)
        shape = f.shape
        f = f.reshape(np.prod(shape[:-1]), shape[-1])
        f_new = np.empty((f.shape[0], t_new.size))
        for i in range(f.shape[0]):
            f_spline = spline(t, f[i], k=spline_order)
            if derivative_order > 0:
                f_spline = f_spline.derivative(n=derivative_order)
            elif derivative_order < 0:
                f_spline = f_spline.antiderivative(n=-derivative_order)
            f_new[i, :] = f_spline(t_new)
        f_new = f_new.reshape(shape[:-1] + (t_new.size,))
        f_new = np.swapaxes(f_new, axis, -1)
        if dtype == np.dtype(complex):
            f_new = np.ascontiguousarray(f_new).view(complex)
            f_new = np.reshape(f_new, f_new.shape[:-1])
        return f_new


    def derivative(f, t):
        return interpolate(f, t, t, axis=0, derivative_order=1)

    
    def indefinite_integral(f, t):
        return interpolate(f, t, t, axis=0, derivative_order=-1)


    def definite_integral(f, t):
        return interpolate(f, t, t[-1:], axis=0, derivative_order=-1)[0]


except:

    def derivative(f, t):
        """Fourth-order finite-differencing with non-uniform time steps

        The formula for this finite difference comes from Eq. (A 5b) of "Derivative formulas and errors for non-uniformly
        spaced points" by M. K. Bowen and Ronald Smith.  As explained in their Eqs. (B 9b) and (B 10b), this is a
        fourth-order formula -- though that's a squishy concept with non-uniform time steps.

        TODO: If there are fewer than five points, the function should revert to simpler (lower-order) formulas.

        """
        dfdt = np.empty_like(f)
        if (f.ndim == 1):
            _derivative(f, t, dfdt)
        elif (f.ndim == 2):
            _derivative_2d(f, t, dfdt)
        elif (f.ndim == 3):
            _derivative_3d(f, t, dfdt)
        else:
            raise NotImplementedError("Taking derivatives of {0}-dimensional arrays is not yet implemented".format(f.ndim))
        return dfdt


    @njit
    def _derivative(f, t, dfdt):
        for i in xrange(2):
            t_i = t[i]
            t1 = t[0]
            t2 = t[1]
            t3 = t[2]
            t4 = t[3]
            t5 = t[4]
            h1 = t1 - t_i
            h2 = t2 - t_i
            h3 = t3 - t_i
            h4 = t4 - t_i
            h5 = t5 - t_i
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            dfdt[i] = (-((h2 * h3 * h4 + h2 * h3 * h5 + h2 * h4 * h5 + h3 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[0]
                       + ((h1 * h3 * h4 + h1 * h3 * h5 + h1 * h4 * h5 + h3 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[1]
                       - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[2]
                       + ((h1 * h2 * h3 + h1 * h2 * h5 + h1 * h3 * h5 + h2 * h3 * h5) / (h14 * h24 * h34 * h45)) * f[3]
                       - ((h1 * h2 * h3 + h1 * h2 * h4 + h1 * h3 * h4 + h2 * h3 * h4) / (h15 * h25 * h35 * h45)) * f[4])

        for i in xrange(2, len(t) - 2):
            t1 = t[i - 2]
            t2 = t[i - 1]
            t3 = t[i]
            t4 = t[i + 1]
            t5 = t[i + 2]
            h1 = t1 - t3
            h2 = t2 - t3
            h4 = t4 - t3
            h5 = t5 - t3
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            dfdt[i] = (-((h2 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[i - 2]
                       + ((h1 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[i - 1]
                       - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[i]
                       + ((h1 * h2 * h5) / (h14 * h24 * h34 * h45)) * f[i + 1]
                       - ((h1 * h2 * h4) / (h15 * h25 * h35 * h45)) * f[i + 2])

        for i in xrange(len(t) - 2, len(t)):
            t_i = t[i]
            t1 = t[-5]
            t2 = t[-4]
            t3 = t[-3]
            t4 = t[-2]
            t5 = t[-1]
            h1 = t1 - t_i
            h2 = t2 - t_i
            h3 = t3 - t_i
            h4 = t4 - t_i
            h5 = t5 - t_i
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            dfdt[i] = (-((h2 * h3 * h4 + h2 * h3 * h5 + h2 * h4 * h5 + h3 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[-5]
                       + ((h1 * h3 * h4 + h1 * h3 * h5 + h1 * h4 * h5 + h3 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[-4]
                       - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[-3]
                       + ((h1 * h2 * h3 + h1 * h2 * h5 + h1 * h3 * h5 + h2 * h3 * h5) / (h14 * h24 * h34 * h45)) * f[-2]
                       - ((h1 * h2 * h3 + h1 * h2 * h4 + h1 * h3 * h4 + h2 * h3 * h4) / (h15 * h25 * h35 * h45)) * f[-1])

        return


    @njit
    def _derivative_2d(f, t, dfdt):
        for i in xrange(2):
            t_i = t[i]
            t1 = t[0]
            t2 = t[1]
            t3 = t[2]
            t4 = t[3]
            t5 = t[4]
            h1 = t1 - t_i
            h2 = t2 - t_i
            h3 = t3 - t_i
            h4 = t4 - t_i
            h5 = t5 - t_i
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            for k in xrange(f.shape[1]):
                dfdt[i, k] = (
                -((h2 * h3 * h4 + h2 * h3 * h5 + h2 * h4 * h5 + h3 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[0, k]
                + ((h1 * h3 * h4 + h1 * h3 * h5 + h1 * h4 * h5 + h3 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[1, k]
                - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[2, k]
                + ((h1 * h2 * h3 + h1 * h2 * h5 + h1 * h3 * h5 + h2 * h3 * h5) / (h14 * h24 * h34 * h45)) * f[3, k]
                - ((h1 * h2 * h3 + h1 * h2 * h4 + h1 * h3 * h4 + h2 * h3 * h4) / (h15 * h25 * h35 * h45)) * f[4, k])

        for i in xrange(2, len(t) - 2):
            t1 = t[i - 2]
            t2 = t[i - 1]
            t3 = t[i]
            t4 = t[i + 1]
            t5 = t[i + 2]
            h1 = t1 - t3
            h2 = t2 - t3
            h4 = t4 - t3
            h5 = t5 - t3
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            for k in xrange(f.shape[1]):
                dfdt[i, k] = (-((h2 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[i - 2, k]
                              + ((h1 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[i - 1, k]
                              - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35))
                                * f[i, k]
                              + ((h1 * h2 * h5) / (h14 * h24 * h34 * h45)) * f[i + 1, k]
                              - ((h1 * h2 * h4) / (h15 * h25 * h35 * h45)) * f[i + 2, k])

        for i in xrange(len(t) - 2, len(t)):
            t_i = t[i]
            t1 = t[-5]
            t2 = t[-4]
            t3 = t[-3]
            t4 = t[-2]
            t5 = t[-1]
            h1 = t1 - t_i
            h2 = t2 - t_i
            h3 = t3 - t_i
            h4 = t4 - t_i
            h5 = t5 - t_i
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            for k in xrange(f.shape[1]):
                dfdt[i, k] = (
                -((h2 * h3 * h4 + h2 * h3 * h5 + h2 * h4 * h5 + h3 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[-5, k]
                + ((h1 * h3 * h4 + h1 * h3 * h5 + h1 * h4 * h5 + h3 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[-4, k]
                - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[-3, k]
                + ((h1 * h2 * h3 + h1 * h2 * h5 + h1 * h3 * h5 + h2 * h3 * h5) / (h14 * h24 * h34 * h45)) * f[-2, k]
                - ((h1 * h2 * h3 + h1 * h2 * h4 + h1 * h3 * h4 + h2 * h3 * h4) / (h15 * h25 * h35 * h45)) * f[-1, k])

        return


    @njit
    def _derivative_3d(f, t, dfdt):
        for i in xrange(2):
            t_i = t[i]
            t1 = t[0]
            t2 = t[1]
            t3 = t[2]
            t4 = t[3]
            t5 = t[4]
            h1 = t1 - t_i
            h2 = t2 - t_i
            h3 = t3 - t_i
            h4 = t4 - t_i
            h5 = t5 - t_i
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            for k in xrange(f.shape[1]):
                for m in xrange(f.shape[2]):
                    dfdt[i, k, m] = (
                    -((h2 * h3 * h4 + h2 * h3 * h5 + h2 * h4 * h5 + h3 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[0, k, m]
                    + ((h1 * h3 * h4 + h1 * h3 * h5 + h1 * h4 * h5 + h3 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[1, k, m]
                    - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[2, k, m]
                    + ((h1 * h2 * h3 + h1 * h2 * h5 + h1 * h3 * h5 + h2 * h3 * h5) / (h14 * h24 * h34 * h45)) * f[3, k, m]
                    - ((h1 * h2 * h3 + h1 * h2 * h4 + h1 * h3 * h4 + h2 * h3 * h4) / (h15 * h25 * h35 * h45)) * f[4, k, m])

        for i in xrange(2, len(t) - 2):
            t1 = t[i - 2]
            t2 = t[i - 1]
            t3 = t[i]
            t4 = t[i + 1]
            t5 = t[i + 2]
            h1 = t1 - t3
            h2 = t2 - t3
            h4 = t4 - t3
            h5 = t5 - t3
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            for k in xrange(f.shape[1]):
                for m in xrange(f.shape[2]):
                    dfdt[i, k, m] = (-((h2 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[i - 2, k, m]
                                  + ((h1 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[i - 1, k, m]
                                  - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35))
                                     * f[i, k, m]
                                  + ((h1 * h2 * h5) / (h14 * h24 * h34 * h45)) * f[i + 1, k, m]
                                  - ((h1 * h2 * h4) / (h15 * h25 * h35 * h45)) * f[i + 2, k, m])

        for i in xrange(len(t) - 2, len(t)):
            t_i = t[i]
            t1 = t[-5]
            t2 = t[-4]
            t3 = t[-3]
            t4 = t[-2]
            t5 = t[-1]
            h1 = t1 - t_i
            h2 = t2 - t_i
            h3 = t3 - t_i
            h4 = t4 - t_i
            h5 = t5 - t_i
            h12 = t1 - t2
            h13 = t1 - t3
            h14 = t1 - t4
            h15 = t1 - t5
            h23 = t2 - t3
            h24 = t2 - t4
            h25 = t2 - t5
            h34 = t3 - t4
            h35 = t3 - t5
            h45 = t4 - t5
            for k in xrange(f.shape[1]):
                for m in xrange(f.shape[2]):
                    dfdt[i, k, m] = (
                    -((h2 * h3 * h4 + h2 * h3 * h5 + h2 * h4 * h5 + h3 * h4 * h5) / (h12 * h13 * h14 * h15)) * f[-5, k, m]
                    + ((h1 * h3 * h4 + h1 * h3 * h5 + h1 * h4 * h5 + h3 * h4 * h5) / (h12 * h23 * h24 * h25)) * f[-4, k, m]
                    - ((h1 * h2 * h4 + h1 * h2 * h5 + h1 * h4 * h5 + h2 * h4 * h5) / (h13 * h23 * h34 * h35)) * f[-3, k, m]
                    + ((h1 * h2 * h3 + h1 * h2 * h5 + h1 * h3 * h5 + h2 * h3 * h5) / (h14 * h24 * h34 * h45)) * f[-2, k, m]
                    - ((h1 * h2 * h3 + h1 * h2 * h4 + h1 * h3 * h4 + h2 * h3 * h4) / (h15 * h25 * h35 * h45)) * f[-1, k, m])

        return


    # @njit('void(f8[:,:], f8[:], f8[:,:])')
    @jit
    def indefinite_integral(f, t):
        Sfdt = np.empty_like(f)
        Sfdt[0] = 0.0
        for i in xrange(1, len(t)):
            for j in xrange(f.shape[1]):
                Sfdt[i, j] = Sfdt[i - 1, j] + (f[i, j] + f[i - 1, j]) * ((t[i] - t[i - 1]) / 2.0)
        return Sfdt


    #@njit('void(f8[:,:], f8[:], f8[:])')
    @jit
    def definite_integral(f, t):
        Sfdt = np.zeros_like(f)
        for i in xrange(1, f.shape[0]):
            Sfdt[i, ...] += (f[i, ...] + f[i - 1, ...]) * ((t[i] - t[i - 1]) / 2.0)
        return Sfdt
