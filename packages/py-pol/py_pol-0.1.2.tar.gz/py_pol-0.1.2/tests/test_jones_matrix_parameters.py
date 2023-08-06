# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Jones_matrix parameters class"""

import sys

import numpy as np
from numpy import matrix

from py_pol import degrees, eps, um
from py_pol.jones_matrix import Jones_matrix


"""
PendingDeprecationWarning: the matrix subclass is not the recommended way to
represent matrices or deal with linear algebra
(see https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html).
Please adjust your code to use regular ndarray.
"""


class TestJonesMatrixParameters(object):
    def test_diattenuation_retardance(self):

        solution = 1
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        ret = M1.parameters.diattenuation_retardance()

        proposal = ret
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: M1*M2"

    def test_diattenuation_retardance_hom(self):

        solution = 1
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        ret = M1.parameters.diattenuation_retardance_hom()

        proposal = ret
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: M1*M2"
