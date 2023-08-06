# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------
# Authors:    Luis Miguel Sanchez Brea and Jesus del Hoyo
# Fecha       2019/01/09 (version 1.0)
# License:    GPL
# -------------------------------------
"""
We present a number of functions for polarization using Jones framework:

## Light beams
* linear light beam
* circular light beam
* elliptical light beam
* convert a jones (2x1) vector to a Stokes (4x1) vector

## parameters
* intensity

TODO: Define a constant ¿maybe cte_I? to change from field to intensity. At the
beggining, it can be 1, but maybe the user will want to change it. __prod__ by
a number. LMSB: No entiendo
"""

import warnings
from functools import wraps

from scipy import cos, exp, matrix, pi, sin, sqrt

from . import degrees, eps, np
from .stokes import Stokes
from .utils import rotation_matrix_2

warnings.filterwarnings('ignore', message='PendingDeprecationWarning')


def rotate_jones(M, angle):
    """Rotation of a Jones matrix

    M_rotated= rotation_matrix_2(-angle) * M * rotation_matrix_2(angle)

    Args:
        M (numpy.matrix): Jones matrix
        angle (float): angle of rotation_matrix_2 in radians.

    """
    if angle == 0:
        return M
    else:
        return rotation_matrix_2(angle) * M


class Parameters_Jones_Vector(object):
    """Class for Jones vector Parameters

    Args:
        jones_vector (Jones_vector): Jones Vector

    Attributes:
        self.M (Jones_vector)
        self.dict (dict): dictionary with parameters
    """

    def __init__(self, Jones_vector=[2, 2]):
        self.M = Jones_vector
        self.dict = {}

    def intensity(self):
        """intensity of Jones vector: v[0]**2 + v[1]**2

        Args:
            j_vector (ndarray): 2x1 polarization vector


        Returns:
            float: intensity
        """
        j_vector = self.M

        i1 = float(abs(j_vector[0])**2 + abs(j_vector[1])**2)
        return i1


class Jones_vector(object):
    """Class for Jones vectors

    Args:
        name (str): name of vector for string representation

    Attributes:
        self.M (numpy.matrix): 4x1 array
        self.parameters (class): parameters of stokes
    """

    def _actualize(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            f(inst, *args, **kwargs)
            inst._actualize_()
            return

        return wrapped

    def __init__(self, name='J'):
        self.name = name
        self.M = np.matrix(np.array([[0], [0]]))
        self.M = np.matrix([[0], [0]])
        self.parameters = Parameters_Jones_Vector(self.M)

    def __add__(self, other):
        """Adds two Jones vectors.

        Args:
            other (Jones): 2nd Jones vector to add

        Returns:
            JOnes: `s3 = s1 + s2`
        """

        j3 = Jones_vector()
        j3.M = self.M + other.M
        j3.name = self.name + " + " + other.name

        return j3

    def __sub__(self, other):
        """Substracts two Jones vectors.

        Args:
            other (Jones): 2nd Jones vector to add

        Returns:
            Jones: `s3 = s1 - s2`
        """

        j3 = Jones_vector()
        j3.M = self.M - other.M
        j3.name = self.name + " - " + other.name

        return j3

    def __mul__(self, other):
        """Multiplies a Jones vectors by a number.

        Args:
            other (Mueller): number to multiply

        Returns:
            Stokes: `s3 = number * s2`
        """
        M3 = Jones_vector()

        if isinstance(other, (int, float, complex)):
            M3.M = self.M * other
        else:
            raise ValueError('other is Not number')
        return M3

    def __rmul__(self, other):
        """Multiplies a Jones vectors by a number.

        Args:
            other (Mueller): number to multiply

        Returns:
            Stokes: `s3 =  s2 * number`
        """
        M3 = Jones_vector()

        if isinstance(other, (int, float, complex)):
            M3.M = other * self.M

        else:
            raise ValueError('other is Not number')
        return M3

    def __repr__(self):
        """
        represents jones vector with print()
        """
        M = np.array(self.M).squeeze()
        l_name = "{} = ".format(self.name)
        difference = abs(M.round() - M).sum()

        if difference > eps:
            l0 = "[{:+1.3f}; {:+1.3f}]'".format(M[0], M[1])
        else:
            l0 = "[{:+1.0f}; {:+1.0f}]'".format(M[0], M[1])

        return l_name + l0

    def _actualize_(self):
        # print("inside _actualize_")
        self.parameters.M = self.M
        # print(self.parameters.M)

    def get(self):
        return self.M

    def check(self):
        """
        verifies that is a Jones vector is properly defined
        verifies that is a 2x1 vector
        """

        # TODO: do check function
        print("TODO")
        pass

    @_actualize
    def rotate(self, angle):
        """Rotation of a Jones matrix

        M_rotated= rotation_matrix_2(angle) * M

        Args:
            M (numpy.matrix): Jones matrix
            angle (float): angle of rotation_matrix_2 in radians.

        """
        # TODO, no me fio del signo menos
        self.M = rotate_jones(self.M, -angle)
        return self.M

    @_actualize
    def custom(self, v0, v1):
        # TODO: 2 funciones: form matrix y custom-> from_elements
        """2x1 Custom Jones vector (v0, v1)

        Args:
            v0 (float): first element v[0]
            v1 (float): first element v[1]

        Returns:
            ndarray: 2x1 matrix
        """

        self.M = matrix([[v0], [v1]])
        return self.M

    @_actualize
    def linear_light(self, amplitude=1, angle=0 * degrees):
        """2x1 Jones vector for polarizer linear light

        Args:
            angle (float): angle of polarization (azimuth).

        Returns:
            ndarray: 2x1 matrix
        """

        self.M = amplitude * matrix([[cos(angle)], [sin(angle)]])
        return self.M

    @_actualize
    def circular_light(self, amplitude=1, kind='d'):
        """2x1 Jones vector for polarizer circular light

        Args:
            kind (str): 'd','r' - right, dextro, derecha.
                        'l', 'i' - left, levo, izquierda.

        Returns:
            ndarray: 2x1 matrix
        """
        # Definicion del vector de Jones a dextrogiro o levogiro
        if kind in 'dr':  # derecha, right
            self.M = amplitude * matrix([[1], [1j]]) / sqrt(2)
        elif kind in 'il':  # izquierda, left
            self.M = amplitude * matrix([[1], [-1j]]) / sqrt(2)
        return self.M

    @_actualize
    def elliptical_light(self, a=1, b=1, phase=0, angle=0):
        """2x1 Jones vector for polarizer elliptical light

        Args:
            a (float): amplitude of x axis
            b (float): amplitude of y axis
            phase (float): phase shift between axis
            angle (float): rotation_matrix_2 angle respect to x axis

        Returns:
            ndarray: 2x1 matrix
        """

        # Definicion del vector de Jones
        M = matrix([[a], [b * exp(1j * phase)]], dtype=complex)
        self.M = rotation_matrix_2(angle) * M
        return self.M

    def to_Stokes(self, p=1):
        """Function that converts Jones light states to Stokes states.
        Args:
            p (float): Degree of polarization
        Returns:
            S (4x1 real array): Stokes state."""
        # Check if we are using linear/circular or global polarization degree
        if np.size(p) == 1:
            (p1, p2) = (p, p)
        else:
            (p1, p2) = (p[0], p[1])

        E = self.M
        # Calculate the vector
        (Ex, Ey) = (E[0], E[1])
        S = np.zeros([1, 4])
        S[0, 0] = abs(Ex)**2 + abs(Ey)**2
        S[0, 1] = (abs(Ex)**2 - abs(Ey)**2) * p1
        S[0, 2] = 2 * np.real(Ex * np.conj(Ey)) * p1
        S[0, 3] = -2 * np.imag(Ex * np.conj(Ey)) * p2

        S1 = Stokes()
        S1.custom(S[0, 0], S[0, 1], S[0, 2], S[0, 3])
        return S1
