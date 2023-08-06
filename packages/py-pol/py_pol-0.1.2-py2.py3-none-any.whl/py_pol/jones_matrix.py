# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------
# Authors:    Luis Miguel Sanchez Brea and Jesus del Hoyo
# Fecha       2019/01/09 (version 1.0)
# License:    GPL
# -------------------------------------
"""
We present a number of functions for polarization using Jones framework:

## Polarizers
* linear polarizer
* retarder
* quarter wave
* half wave
"""
import cmath
from functools import wraps

from scipy import array, cos, exp, matrix, pi, sin, sqrt

from . import degrees, eps, np, um
# Imports at the end of the script allows cycling import
from .jones_vector import Jones_vector
from .utils import (azimuth_elipt_2_carac_angles, put_in_limits,
                    rotation_matrix_Jones)


class Parameters_Jones_Matrix(object):
    """Class for Jones Matrix Parameters

    Args:
        jones_matrix (Jones_matrix): Jones Matrix

    Attributes:
        self.M (Jones_matrix)
        self.dict (dict): dictionary with parameters
    """

    def __init__(self, Jones_matrix):
        self.M = Jones_matrix
        self.dict = {}

    def diattenuation(self):
        """Calculation of the diattenuation  of a Jones element.

        From: "Homogeneous and inhomogeneous Jones matrices", Shih-Yau Lu and
        Russell A. Chipman, J. Opt. Soc. Am. A/Vol. 11, No. 2 pp. 766 (1994)

        Args:
            J (matrix): 2x2 Jones matrix

        Returns:
            D (float): Diattenuation."""
        J = self.M

        # Check that the matrix is homogeneous
        val, vect = np.linalg.eig(J)
        (v1, v2) = (vect[0, :], vect[1, :])
        prod = (v1 * v2.H)[0, 0]
        if abs(prod) < eps:
            # Homogeneous case
            a1, a2 = (abs(val[0]), abs(val[1]))
            D = abs(a1**2 - a2**2) / (a1**2 + a2**2)
        else:
            # Inhomogeneous case (unknown source)
            # tr2 = np.trace(J.H * J)
            # det1 = np.linalg.det(J)
            # Tmin = (tr2 - sqrt(tr2**2 - 4 * abs(det1)**2)) / 2
            # Tmax = (tr2 + sqrt(tr2**2 - 4 * abs(det1)**2)) / 2
            # D = (Tmax - Tmin) / (Tmax + Tmin)
            # Inhomogeneous case (refered source)
            num = (2 * (1 - prod**2) * abs(val[0]) * abs(val[1]))**2
            den = (abs(val[0])**2 + abs(val[1])**2 - prod**2 *
                   (val[0] * np.conj(val[1]) + val[1] * np.conj(val[0])))**2
            D = sqrt(1 - num / den)
        return D

    def is_homogeneous(self, inhom=True):
        """determines if matrix is homogeneous or not

        From: "Homogeneous and inhomogeneous Jones matrices", Shih-Yau Lu and
        Russell A. Chipman, J. Opt. Soc. Am. A/Vol. 11, No. 2 pp. 766 (1994)

        Args:
            J (matrix): 2x2 Jones matrix

        Returns:
            (bool): True if matrix is homongeneus."""

        J = self.M

        # Check that the matrix is homogeneous
        val, vect = np.linalg.eig(J)
        (v1, v2) = (vect[0, :], vect[1, :])
        prod = (v1 * v2.H)[0, 0]
        if abs(prod) < eps:
            return True
        else:
            return False

    def delay(self, inhom=True):
        """Calculation of the delay (or retardance) of a Jones element.

        From: "Homogeneous and inhomogeneous Jones matrices", Shih-Yau Lu and
        Russell A. Chipman, J. Opt. Soc. Am. A/Vol. 11, No. 2 pp. 766 (1994)

        Args:
            J (matrix): 2x2 Jones matrix

        Returns:
            R (float): Retardance."""

        J = self.M

        # Check that the matrix is homogeneous
        val, vect = np.linalg.eig(J)
        (v1, v2) = (vect[0, :], vect[1, :])
        prod = (v1 * v2.H)[0, 0]
        (tr1, tr2) = (np.trace(J), np.trace(J.H * J))
        det_J = np.linalg.det(J)
        if abs(prod) < eps:
            # Homogeneous case (unknown source)
            # d1, d2 = (np.angle(val[0]), np.angle(val[1]))
            # R = abs(d1 - d2)
            # Homogeneous (refered source)
            if abs(det_J) < eps:
                delay = 2 * np.arccos(np.abs(tr1) / np.sqrt(tr2))
            else:
                num = np.abs(tr1 + det_J * np.trace(J.H) / np.abs(det_J))
                den = 2 * np.sqrt(tr2 + 2 * np.abs(det_J))
                delay = np.real(2 * np.arccos(num / den))

        else:
            # Inhomogenous (unknown source)
            # val, vect = np.linalg.eig(J.H * J)
            # (v1, v2) = (vect[0, :], vect[1, :])
            # R = 2 * np.arccos(abs(v1.H * J * v1 + v2.H * J * v2) / 2)
            # Inhomogenous (refered source)
            num = (1 - prod**2) * (abs(val[0]) + abs(val[1]))**2
            den = (abs(val[0]) + abs(val[1]))**2 - prod**2 * (
                2 * val[0] * abs(val[0]) * abs(val[1]) + np.conj(val[1]) +
                val[1] * np.conj(val[0]))
            co = cos((np.angle(val[0]) - np.angle(val[1])) / 2)
            delay = float(2 * np.arccos(sqrt(num / den) * co))
        return delay


class Jones_matrix(object):
    """Class for Jones matrices

    Args:
        name (str): name of matrix for string representation

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

    def __init__(self, name='M'):
        self.name = name
        self.M = np.matrix(np.zeros((2, 2), dtype=complex))
        self.parameters = Parameters_Jones_Matrix(self.M)

    def _actualize_(self):
        # print("inside _actualize_")
        self.parameters.M = self.M
        # print(self.parameters.M)

    def get(self):
        return self.M

    def __add__(self, other):
        """Adds two Jones matrices.

        Args:
            other (Jones): 2nd Jones matrix to add

        Returns:
            Jones Matrix: `s3 = s1 + s2`
        """

        j3 = Jones_matrix()
        j3.M = self.M + other.M
        j3.name = self.name + " + " + other.name

        return j3

    def __sub__(self, other):
        """Substracts two Jones matrices.

        Args:
            other (Jones): 2nd Jones matrix to add

        Returns:
            Jones: `s3 = s1 - s2`
        """

        j3 = Jones_matrix()
        j3.M = self.M - other.M
        j3.name = self.name + " - " + other.name

        return j3

    def __mul__(self, other):
        """
        TODO: check that other is a matrix (or a Jones_matrix) or a constant
        multiplies two Jones matrices.

        Args:
            other (Jones): 2nd Jones multiply

        Returns:
            Jones: `s3 = s1*s2`
        """

        if isinstance(other, (int, float, complex)):
            M3 = Jones_matrix()
            M3.M = self.M * other
        elif isinstance(other, (self.__class__)):
            M3 = Jones_matrix()
            M3.M = self.M * other.M
            M3.name = self.name + " * " + other.name
        elif isinstance(other, Jones_vector):
            M3 = Jones_vector()
            M3.M = self.M * other.M
            M3.name = self.name + " * " + other.name
        else:
            raise ValueError(
                'other is Not number, Jones_vector or Jones_matrix')
        return M3

    def __rmul__(self, other):
        """
        TODO: check that other is a matrix (or a Jones_matrix) or a constant
        multiplies two Jones matrices.

        Args:
            other (Jones): 2nd Jones multiply

        Returns:
            Jones: `s3 = s2*s1`
        """

        M3 = Jones_matrix()

        if isinstance(other, (int, float, complex)):
            M3.M = self.M * other
        elif isinstance(other, self.__class__):
            M3.M = other.M * self.M
            M3.name = other.name + " * " + self.name
        else:
            raise ValueError('other is Not number or Jones_matrix')
        return M3

    def __repr__(self):

        M = np.array(self.M).squeeze()
        l_name = "{} = \n".format(self.name)

        if abs(M.real - M).sum() < eps:
            M = M.real
            M.dtype = float

        difference = abs(M.round() - M).sum()
        if difference > eps:
            l0 = "      [{:+1.3f}, {:+1.3f}]\n".format(M[0, 0], M[0, 1])
            l1 = "      [{:+1.3f}, {:+1.3f}]".format(M[1, 0], M[1, 1])
        else:
            l0 = "      [{:+1.0f}, {:+1.0f}]\n".format(M[0, 0], M[0, 1])
            l1 = "      [{:+1.0f}, {:+1.0f}]".format(M[1, 0], M[1, 1])

        return l_name + l0 + l1

    def check(self):
        """
        verifies that is a Jones matrix is properly defined
        verifies that is a 2x2 matrix
        norm <=1 ?
        """

        # TODO: do check function
        print("TODO")
        pass

    @_actualize
    def rotate(self, angle):
        """rotates a jones_matrix a certain angle

        Args:
            angle (float): angle of polarizer axis, in radians.

        Returns:
            np.matrix: 2x2 matrix
        """
        if angle != 0.:
            self.M = rotation_matrix_Jones(
                -angle) * self.M * rotation_matrix_Jones(angle)
            self.name = self.name + " @ rotated {:1.2f}º".format(
                angle / degrees)
        return self.M

    @_actualize
    def from_elements(self, m00, m01, m10, m11):
        """2x2 Jones matrix [m00, m01, m10, m11]

        Args:
            m00 (float): first element m00
            m01 (float): first element m01
            m10 (float): first element m10
            m11 (float): first element m11

        Returns:
            np.matrix: 2x2 matrix
        """

        self.M = matrix(array([[m00, m01], [m10, m11]]), dtype=complex)
        return self.M

    @_actualize
    def from_matrix(self, M):
        """Create a Jones matrix from an external matrix.

        Args:
            M (2x2 numpy matrix): New matrix

        Returns:
            np.matrix: 2x1 matrix
        """

        self.M = M
        return self.M

    # @_actualize
    # def from_Mueller(self):
    #   pass

    # @_actualize
    # def to_Mueller(self):
    #     """Takes a Jones Matrix and converts into Mueller Matrix
    #
    #     After: Handbook of Optics vol 2. 22.36 (50)
    #
    #     M = U * (J oX J*) * U^(-1)
    #
    #     T(M*Mt)=4*m00
    #
    #
    #     Args:
    #         J (2x2 mumpy.matrix): Mueller matrix
    #
    #     Returns:
    #         M (mumpy.matrix): Mueller matrix
    #     """
    #
    #     J = self.M
    #     U = matrix([[1, 0, 0, 1], [1, 0, 0, -1], [0, 1, 1, 0], [0, 1j, -1j,
    #                                                             0]])
    #     M = U * np.kron(J, J.conjugate()) * inv(U)
    #     M = np.real(M)
    #     self.M = M
    #     return self.M

    @_actualize
    def neutral(self, D=1):
        """Creates the matrix for a neutral filter or amplifier element.

        Args:
            D (float): Attenuation (gain if > 1).

        Returns:
            np.matrix: 2x2 matrix
        """
        self.M = matrix(array([[D, 0], [0, D]]), dtype=complex)
        return self.M

    @_actualize
    def polarizer_linear(self, angle=0):
        """2x2 perfect linear polarizer

        Args:
            angle (float): angle of polarizer axis, in radians.

        Returns:
            np.matrix: 2x2 matrix
        """

        # Metodo directo
        # return matrix(array([[cos(angle) ** 2, sin(angle) * cos(angle)],
        #         [sin(angle) * cos(angle), sin(angle) ** 2]]), dtype = float)

        self.M = matrix(array([[1, 0], [0, 0]]), dtype=float)
        self.rotate(angle)
        return self.M

    @_actualize
    def diattenuator_lineal(self, p1=1, p2=0, angle=0):
        """Creates a real polarizer with perpendicular axes:
        J = [p1, 0; 0, p2]

        Args:
            P1 (float):
            angle (float): rotation angle.

        Returns:
            np.matrix: 2x2 matrix
        """
        self.M = matrix(array([[p1, 0], [0, p2]]), dtype=complex)

        self.rotate(angle)
        return self.M

    @_actualize
    def retarder_linear(self, delay=0 * degrees, angle=0 * degrees):
        """Creates a 2x2 linear.


        Args:
            delay (float): delay produced by retarder.
            angle (float): angle of polarizer axis, in radians.

        Returns:
            np.matrix: 2x2 matrix
        """

        self.M = matrix(array([[1, 0], [0, exp(1j * delay)]]), dtype=complex)
        self.rotate(angle)
        return self.M

    @_actualize
    def retarder_material(self,
                          ne=1,
                          no=1,
                          d=1 * um,
                          wavelength=0.6328 * um,
                          angle=0 * degrees):
        """Creates a 2x2 retarder using delay or physical properties of an anisotropic material.
            phase=2*pi*(ne-no)*d/lambda

        Args:
            ne (float): extraordinary index
            n0 (float): ordinary index
            d (float): thickness of the sheet
            wavelength (float): wavelength of the illumination
            angle (float): angle of polarizer axis, in radians.

        Returns:
            np.matrix: 2x2 matrix
        """

        phase = 2 * pi * (ne - no) * d / wavelength

        self.M = matrix(array([[1, 0], [0, exp(1j * phase)]]), dtype=complex)
        self.rotate(angle)
        return self.M

    @_actualize
    def diattenuator_retarder_linear(self, delay, p1=1, p2=1, angle=0):
        """Creates a linear diattenuator retarder with the same
        axes for diattenuation and retardance. At 0 degrees, the matrix is of
        the form:

        J = [p1, 0; 0, p2*exp(i*delay)]

        Args:
            delay (float): Retarding angle.
            p1 (float): Field transmission of the fast axis (default 1).
            p2 (float): Field transmission of the slow angle (default 1).
            angle (float): Element rotation angle (default 0).

        Returns:
            np.matrix: 2x2 matrix
        """
        self.M = matrix(
            array([[p1, 0], [0, p2 * exp(1j * delay)]], dtype=complex))
        name = self.name
        self.rotate(angle)
        self.name = name
        return self.M

    @_actualize
    def diattenuator_carac_angles(self, p1, p2, alpha, delta, angle=0):
        """Creates the most general diattenuator with orthogonal
        eigenstates from the caracteristic angles of the main eigenstate.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 137.

        Args:
            p1 (float): [0, 1] Square root of the higher transmission for one
                eigenstate.
            p2 (float): [0, 1] Square root of the lower transmission for the other
                eigenstate.
            alpha (float): [0, pi/2]: tan(alpha) is the ratio between field
                amplitudes of X and Y components.
            delta (float): [0, 2*pi]: phase difference between X and Y field
                components.
            carac (bool): [Default: True] If false, assumes alpha is azimuth and
            delta is elipticity.
            angle (float): rotation angle.

        Output:
            J (2x2 matrix): Mueller matrix of the diattenuator.
        """
        # TODO: (Jesus) Check this step
        # Restrict measured values to the correct interval
        alpha = put_in_limits(alpha, "alpha")
        delta = put_in_limits(delta, "delta")
        # Compute the common operations
        sa, ca = (sin(alpha), cos(alpha))
        ed, edm = (cmath.exp(1j * delta), cmath.exp(-1j * delta))
        # Calculate the Jones matrix
        self.M = matrix(
            array([[p1 * ca**2 + p2 * sa**2, sa * ca * (p1 - p2) * edm],
                   [sa * ca * (p1 - p2) * ed, p2 * ca**2 + p1 * sa**2]]))

        self.rotate(angle)
        return self.M

    @_actualize
    def diattenuator_azimuth_ellipticity(self, p1, p2, az, el, angle=0):
        """Creates the general diattenuator with orthogonal eigenstates from the caracteristic angles of the main eigenstate.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 137.

        Args:
            p1 (float): [0, 1] Square root of the higher transmission for one
                eigenstate.
            p2 (float): [0, 1] Square root of the lower transmission for the other
                eigenstate.
            az (float): [0, pi]: Azimuth.
            el (float): [-pi/4, pi/]: Ellipticity.
            carac (bool): [Default: True] If false, assumes alpha is azimuth and
            delta is elipticity.
            angle (float): rotation angle.

        Output:
            J (2x2 matrix): Mueller matrix of the diattenuator.
        """
        # If we are not working tith the caracteristic angles, but with azimuth and
        # elipticity, convert them
        alpha, delta = azimuth_elipt_2_carac_angles(az=az, el=el)
        self.diattenuator_carac_angles(p1, p2, alpha, delta, angle)
        return self.M

    # TODO: (Jesus) Retardadores. Que en Jones no tenemos ninguno.
