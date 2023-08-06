# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for stokes module"""
import sys

from numpy import matrix

from py_pol import degrees, np
from py_pol.mueller import Mueller

eps = 1e-6
"""
PendingDeprecationWarning: the matrix subclass is not the recommended way to
represent matrices or deal with linear algebra
(see https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html).
Please adjust your code to use regular ndarray.
"""


class TestMueller(object):
    def test_quarter_wave(self):
        """test for quarter plate using Mueller formalism.
        We have checked 0, 45 and 90 degrees"""

        solution = matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1],
                           [0, 0, -1, 0]])

        M1 = Mueller()
        proposal = M1.quarter_wave(theta=0 * degrees)
        proposal = M1.M
        print(solution)
        print(proposal)
        print(type(solution), type(proposal))
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + "@ 0 grados"

        solution = matrix([[1., 0., 0., 0.], [0., 0., 0., -1.],
                           [0., 0., 1., 0.], [0., 1., -0., 0.]])

        M1 = Mueller()
        proposal = M1.quarter_wave(theta=45 * degrees)
        proposal = M1.M
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + "@ 45 grados"

        solution = matrix([[1., 0., 0., 0.], [0., 1., -0., -0.],
                           [0., -0., 0., -1.], [0., 0., 1., 0.]])

        M1 = Mueller()
        proposal = M1.quarter_wave(theta=90 * degrees)
        proposal = M1.M
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + "@ 90 grados"
