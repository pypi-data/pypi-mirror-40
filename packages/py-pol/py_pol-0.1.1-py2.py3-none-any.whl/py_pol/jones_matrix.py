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

    def diattenuation_retardance_hom(self, inhom=True):
        """Calculation of the diattenuation and retardance of an homogeneous Jones
        element.

        From: "Homogeneous and inhomogeneous Jones matrices", Shih-Yau Lu and
        Russell A. Chipman, J. Opt. Soc. Am. A/Vol. 11, No. 2 pp. 766 (1994)

        Args:
            J (matrix): 2x2 Jones matrix
            inhom (bool): If element is inhomogenous, calculate the inhomogenous
                case instead or not.

        Returns:
            D (float): Diattenuation.
            R (float): Retardance."""
        J = self.M

        val, vect = np.linalg.eig(J)
        # Check that the matrix is really homogeneous
        (v1, v2) = (vect[0, :], vect[1, :])
        prod = v1.H * v2
        if prod == 0 and inhom:
            D, R = self.diattenuation_retardance(J)
        elif prod == 0:
            raise ValueError('Element is inhomogenous.')
        else:
            # Really is homogeneous, so calculate
            a1, a2 = (abs(val[0]), abs(val[1]))
            d1, d2 = (np.angle(val[0]), np.angle(val[1]))
            D = abs(a1**2 - a2**2) / (a1**2 + a2**2)
            R = abs(d1 - d2)
        return D, R

    def diattenuation_retardance(self):
        """Calculation of the diattenuation and retardance of a Jones element.

        From: "Homogeneous and inhomogeneous Jones matrices", Shih-Yau Lu and
        Russell A. Chipman, J. Opt. Soc. Am. A/Vol. 11, No. 2 pp. 766 (1994)

        Args:
            J (matrix): 2x2 Jones matrix

        Returns:
            D (float): Diattenuation.
            R (float): Retardance."""

        # Diattenuation
        J = self.M

        _, tr2 = (np.trace(J), np.trace(J.H * J))
        det1, _ = (np.linalg.det(J), np.linalg.det(J.H * J))
        Tmin = (tr2 - sqrt(tr2**2 - 4 * abs(det1)**2)) / 2
        Tmax = (tr2 + sqrt(tr2**2 - 4 * abs(det1)**2)) / 2
        D = (Tmax - Tmin) / (Tmax + Tmin)

        # Retardance
        val, vect = np.linalg.eig(J.H * J)
        (v1, v2) = (vect[0, :], vect[1, :])
        R = 2 * np.arccos(abs(v1.H * J * v1 + v2.H * J * v2) / 2)
        return D, R


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

        M3 = Jones_matrix()

        if isinstance(other, (int, float, complex)):
            M3.M = self.M * other
        elif isinstance(other, (self.__class__, Jones_vector)):
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
            ndarray: 2x2 matrix
        """
        if angle != 0.:
            self.M = rotation_matrix_Jones(
                -angle) * self.M * rotation_matrix_Jones(angle)
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
            ndarray: 2x2 matrix
        """

        self.M = matrix(array([[m00, m01], [m10, m11]]), dtype=complex)
        return self.M

    @_actualize
    def from_matrix(self, M):
        """Create a Jones matrix from an external matrix.

        Args:
            M (2x2 numpy matrix): New matrix

        Returns:
            ndarray: 2x1 matrix
        """

        self.M = M
        return self.M

    @_actualize
    def to_Mueller(self):
        """Takes a Jones Matrix and converts into Mueller Matrix

        After: Handbook of Optics vol 2. 22.36 (50)

        M = U * (J oX J*) * U^(-1)

        T(M*Mt)=4*m00


        Args:
            J (2x2 mumpy.matrix): Mueller matrix

        Returns:
            M (mumpy.matrix): Mueller matrix
        """

        J = self.M
        U = matrix([[1, 0, 0, 1], [1, 0, 0, -1], [0, 1, 1, 0], [0, 1j, -1j,
                                                                0]])
        M = U * np.kron(J, J.conjugate()) * inv(U)
        M = np.real(M)
        self.M = M
        return self.M

    @_actualize
    def polarizer_linear(self, angle=0):
        """2x2 perfect linear polarizer

        Args:
            angle (float): angle of polarizer axis, in radians.

        Returns:
            ndarray: 2x2 matrix
        """

        # Metodo directo
        # return matrix(array([[cos(angle) ** 2, sin(angle) * cos(angle)],
        #         [sin(angle) * cos(angle), sin(angle) ** 2]]), dtype = float)

        self.M = matrix(array([[1, 0], [0, 0]]), dtype=float)
        self.rotate(angle)
        return self.M

    @_actualize
    def retarder_material(self,
                          phase=0,
                          ne=1,
                          no=1,
                          d=1 * um,
                          wavelength=0.6328 * um,
                          angle=0 * degrees):
        """2x2 retarder
            It can be computed in two ways:
                if phase is not None: the phase is that of phase variable
                if phase is None: phase=2*pi*(ne-no)*d/lambda

        Args:
            phase (float): phase shift produced by retarder- 2*pi*(ne-no)*d/lambda
            ne (float): extraordinary index
            n0 (float): ordinary index
            d (float): thickness of the sheet
            wavelength (float): wavelength of the illumination
            angle (float): angle of polarizer axis, in radians.

        Returns:
            ndarray: 2x2 matrix
        """

        if phase is None:
            phase = 2 * pi * (ne - no) * d / wavelength

        self.M = matrix(array([[1, 0], [0, exp(1j * phase)]]), dtype=complex)
        self.rotate(angle)
        return self.M

    @_actualize
    def neutral(self, D=1):
        """Creates the matrix for a neutral filter or amplifierelement.
        TODO: verify

        Args:
            D (float): Attenuation (gain if > 1).

        Returns:
            ndarray: 2x2 matrix
        """
        self.M = matrix(array([[D, 0], [0, D]]), dtype=complex)
        return self.M

    @_actualize
    def diattenuator_retarder_linear(self, delta, p1=1, p2=1, angle=0):
        """Creates the matrix for a linear diattenuator retarder with the same
        axes for diattenuation and retardance. At 0 degrees, the matrix is of
        the form:

        J = [p1, 0; 0, p2*exp(i*delta)]

        Args:
            delta (float): Retarding angle.
            p1 (float): Field transmission of the fast axis (default 1).
            p2 (float): Field transmission of the slow angle (default 1).
            angle (float): Element rotation angle (default 0).

        Returns:
            ndarray: 2x2 matrix
        """
        self.M = matrix(
            array([[p1, 0], [0, p2 * exp(1j * delta)]], dtype=complex))

        self.rotate(angle)
        return self.M

    @_actualize
    def diattenuator_lineal(self, p1=1, p2=0, angle=0):
        """Creates the matrix for a real polarizer with perpendicular axes:
        J = [P1, 0; 0, P2]

        Args:
            P1 (float):
            angle (float): rotation angle.

        Returns:
            ndarray: 2x2 matrix
        """
        self.M = matrix(array([[p1, 0], [0, p2]]), dtype=complex)

        self.rotate(angle)
        return self.M

    @_actualize
    def diattenuator_carac_angles(self, p1, p2, alpha, delta, angle=0):
        """Function that calculates the most general diattenuator with orthogonal
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
        """Function that calculates the most general diattenuator with orthogonal
        eigenstates from the caracteristic angles of the main eigenstate.

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
        self.diattenuator_carac_angles(self, p1, p2, alpha, delta, angle)
        return self.M

    # TODO: (Jesus) Retardadores. Que en Jones no tenemos ninguno.


# Imports at the end of the script allows cycling import
from .jones_vector import Jones_vector
