# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Jones_matrix module"""

import sys

import numpy as np
from numpy import matrix

from py_pol import degrees, eps
from py_pol.jones_matrix import Jones_matrix
"""
PendingDeprecationWarning: the matrix subclass is not the recommended way to
represent matrices or deal with linear algebra
(see https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html).
Please adjust your code to use regular ndarray.
"""


class TestJonesMatrix(object):
    def test_custom(self):

        solution = matrix([[1, 0], [0, 0]])
        M1 = Jones_matrix()
        M1.from_elements(1, 0, 0, 0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: (1, 0, 0 ,0)"

        solution = matrix([[1, 0], [0, 1j]])
        M1 = Jones_matrix()
        M1.from_elements(1, 0, 0, 1j)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: (1, 0, 0, 1j)"

    def test_linear_polarizer(self):

        solution = matrix([[1, 0], [0, 0]])
        M1 = Jones_matrix('M_linear')
        M1.polarizer_linear(angle=0 * degrees)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 0*degrees"

        solution = matrix([[0.5, 0.5], [0.5, 0.5]])
        M1 = Jones_matrix('M_linear')
        M1.polarizer_linear(angle=45 * degrees)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 45*degrees"

        solution = matrix([[0, 0], [0, 1]])
        M1 = Jones_matrix('M_linear')
        M1.polarizer_linear(angle=90 * degrees)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 90*degrees"

    def test_neutral_element(self):

        solution = matrix([[0.25, 0], [0, 0.25]])
        M1 = Jones_matrix('M_neutral')
        M1.neutral(D=.25)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 0.25"

    def test_diatenuator_retarder(self):

        solution = matrix([[1, 0], [0, 1j]])
        M1 = Jones_matrix('M_diat')
        M1.diattenuator_retarder_linear(delta=np.pi / 2, A=1, B=1, angle=0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: pi/2"

        solution = matrix([[1, 0], [0, -1]])
        M1 = Jones_matrix('M_diat')
        M1.diattenuator_retarder_linear(delta=np.pi, A=1, B=1, angle=0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: pi"

        solution = matrix([[0.5 + 0.25j, 0.5 - 0.25j],
                           [0.5 - 0.25j, 0.5 + 0.25j]])
        M1 = Jones_matrix('M_diat')
        M1.diattenuator_retarder_linear(
            delta=np.pi / 2, A=1, B=.5, angle=45 * degrees)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: delta=np.pi/2, A=1, B=.5, angle=45*degrees"

    def test_real_polarizer(self):

        solution = matrix([[1, 0], [0, 0]])
        M1 = Jones_matrix('M_linear')
        M1.diattenuator_lineal(p1=1, p2=0, angle=0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: p1=1, p2=0, angle=0"

        solution = matrix([[0.95, 0], [0, 0.25]])
        M1 = Jones_matrix('M_linear')
        M1.diattenuator_lineal(p1=.95, p2=0.25, angle=0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: p1=.95, p2=0.25, angle=0"

        solution = matrix([[0.5, 0.25], [0.25, 0.5]])
        M1 = Jones_matrix('M_linear')
        M1.diattenuator_lineal(p1=.75, p2=.25, angle=45 * degrees)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: p1=.75, p2=.25, angle=45*degrees"

    def test_general_diatenuator(self):

        solution = matrix([[0.75, 0], [0, 0.25]])
        M1 = Jones_matrix('M_gen_diat')
        M1.diattenuator_azimuth_ellipticity(
            p1=.75, p2=0.25, az=0 * degrees, el=0 * degrees, angle=0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: without angles"

        solution = matrix([[0.5, -0.5j], [0.5j, 0.5]])
        M1 = Jones_matrix('M_gen_diat')
        M1.diattenuator_azimuth_ellipticity(
            p1=1, p2=0, az=45 * degrees, el=90 * degrees, angle=0)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: without angles"

    def test_rotate(self):

        solution = matrix([[0.5, 0.5], [0.5, 0.5]])
        M1 = Jones_matrix('M_rot')
        M1.polarizer_linear(angle=0 * degrees)
        M1.rotate(45 * degrees)
        proposal = M1.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 45*degrees"

    def test_multiplication(self):

        solution = matrix([[2, 0], [0, 0]])
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        M2 = Jones_matrix('M2')
        M2.from_elements(1, 0, 1, 0)
        M3 = M1 * M2
        proposal = M3.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: M1*M2"

        solution = matrix([[1, 1], [1, 1]])
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        M2 = Jones_matrix('M2')
        M2.from_elements(1, 0, 1, 0)
        M3 = M2 * M1
        proposal = M3.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: M2*M1"

        solution = matrix([[3, 3], [0, 0]])
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        M4 = 3 * M1
        proposal = M4.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 3 * M1"

        solution = matrix([[3, 3], [0, 0]])
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        M5 = M1 * 3
        proposal = M5.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: M1*3"

        solution = matrix([[5, 2], [3, 0]])
        M1 = Jones_matrix('M1')
        M1.from_elements(1, 1, 0, 0)
        M2 = Jones_matrix('M2')
        M2.from_elements(1, 0, 1, 0)
        M6 = 2 * M1 + 3 * M2
        proposal = M6.get()
        assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
        ).f_code.co_name + ".py --> example: 2*M1+3*M2"

    # TODO: Faltan parameters
    #
    # def test_get_intensity(self):
    #
    #     solution = 1.
    #     M1 = Jones_vector('M1')
    #     M1.from_elements(1, 0)
    #     proposal = M1.parameters.intensity()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> example: (1,0)"
    #
    #     solution = 2.
    #     M1 = Jones_vector('M1')
    #     M1.from_elements(1, 1)
    #     proposal = M1.parameters.intensity()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> example: (1,1)"
    #
    #     solution = 2.
    #     M1 = Jones_vector('M1')
    #     M1.from_elements(1, 1j)
    #     proposal = M1.parameters.intensity()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> example: (1,1j)"
    #
    # def test_to_stokes(self):
    #
    #     solution = matrix([[1., 1., 0., 0.]])
    #     M1 = Jones_vector('M1')
    #     M1.linear_light(angle=0 * degrees)
    #     S1 = M1.to_Stokes()
    #     proposal = S1.get()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> linear_light(angle=0*degrees)"
    #
    #     solution = matrix([[1., 0., 1., 0.]])
    #     M1 = Jones_vector('M1')
    #     M1.linear_light(angle=45 * degrees)
    #     S1 = M1.to_Stokes()
    #     proposal = S1.get()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> linear_light(angle=45*degrees)"
    #
    #     solution = matrix([[1., -1., 0., 0.]])
    #     M1 = Jones_vector('M1')
    #     M1.linear_light(angle=90 * degrees)
    #     S1 = M1.to_Stokes()
    #     proposal = S1.get()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> linear_light(angle=90*degrees)"
    #
    #     solution = matrix([[1., 0., -1., 0.]])
    #     M1 = Jones_vector('M1')
    #     M1.linear_light(angle=135 * degrees)
    #     S1 = M1.to_Stokes()
    #     proposal = S1.get()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> linear_light(angle=135*degrees)"
    #
    #     solution = matrix([[+1, +0, +0., +1.]])
    #     M1 = Jones_vector('M1')
    #     M1.circular_light(kind='r')
    #     S1 = M1.to_Stokes()
    #     proposal = S1.get()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> circular_light(kind='r')"
    #
    #     solution = matrix([[+1, +0, +0., -1]])
    #     M1 = Jones_vector('M1')
    #     M1.circular_light(kind='l')
    #     S1 = M1.to_Stokes()
    #     proposal = S1.get()
    #     assert np.linalg.norm(proposal - solution) < eps, sys._getframe(
    #     ).f_code.co_name + ".py --> circular_light(kind='l')"
