# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------
# Authors:    Luis Miguel Sanchez Brea and Jesus del Hoyo
# Fecha       2019/01/09 (version 1.0)
# License:    GPL
# -------------------------------------
"""
We present a number of functions for Mueller matrices:


## Polarizers
* linear polarizer
* retarder
* quarter wave
* half wave
* partial diffuser

## Polarization properties of Polarizers


* diattenuation

TODO

"""

from functools import wraps

import numpy as np
from numpy import arctan, array, cos, exp, matrix, pi, sin, sqrt
from numpy.linalg import inv

from .jones_vector import Jones_vector, eps
from .utils import (azimuth_elipt_2_carac_angles, carac_angles_2_azimuth_elipt,
                    create_from_blocks, divide_in_blocks, isrow, limAlpha,
                    limDelta, order_eig, put_in_limits)

degrees = pi / 180

tol_default = 0.01
counter_max = 20
# Create a list with the base of matrices
S = [
    np.matrix(np.eye(2)),
    np.matrix(array([[1, 0], [0, -1]])),
    np.matrix(array([[0, 1], [1, 0]])),
    np.matrix(array([[0, -1j], [1j, 0]]))
]


def diattenuation(M, normalize=True):
    """Calculates the diattenuation of a Mueller matrix or a diattenuation
    vector.

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

    Args:
        M (4x4 numpy.matrix or 1x3 array): Mueller matrix or diattenuation
            vector.
        normalize (bool): If True, for matrices it will always normalize by m00

    Returns:
        D (float): Diattenuation
    """
    # In case it is a matrix, take the depolarization vector
    m00 = M[0, 0]
    if M.size == 16:
        M = M[0, 1:4]
        if normalize:
            M = M / m00
    D = sqrt(np.sum(np.power(M, 2)))
    return D


def rotation_matrix(theta=0):
    """Muller 4x4 matrix for rotation
    After: Gil, Ossikovski (4.30) - p. 131
    Handbook of Optics vol 2. 22.16 (eq.8) is with changed sign in sin

    Args:
        theta (float): angle of rotation with respect to 0º.

    Returns:
        ndarray: 4x4 rotation matrix

    Todo: check sign. I think that
    """

    # Definicion de la matrix
    c2b = cos(2 * theta)
    s2b = sin(2 * theta)
    return matrix(
        array([[1, 0, 0, 0], [0, c2b, s2b, 0], [0, -s2b, c2b, 0], [0, 0, 0,
                                                                   1]]),
        dtype=float)


def rotate_mueller(M, theta):
    """Muller 4x4 matrix for pure linear polarizer

    After Gil, Ossikovski (3.3) - p. 116

    M_rotated= rotation_matrix(-theta) * M * rotation_matrix(theta)

    Args:
        M (numpy.matrix): Mueller matrix
        theta (float): angle of rotation_matrix in radians.

    """
    if theta == 0:
        return M
    else:
        return rotation_matrix(-theta) * M * rotation_matrix(theta)


def inverse_covariance(H):
    """Calculates the Mueller matrix from the covariance matrix.
    Warning 1: the base of matrices S is used in an uncommon order.
    Warning 2: In order to obtain the same result as in the book, the formula
        must be:
        H = 0.25 sum(m[i,j] kron(S[i], np.conj(S[J]) ))

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

    Args:
        H (numpy.matrix 4x4): Covariance matrix.

    Returns:
        M (numpy.matrix 4x4): Mueller matrix or diattenuation vector.
    """
    M = np.zeros((4, 4), dtype=complex)
    for i in range(4):
        for j in range(4):
            elem = np.trace(np.kron(S[i], np.conj(S[j])) * H)
            # print(elem)
            # print(np.kron(S[i], np.conj(S[j])) * H)
            M[i, j] = elem
            # print([i, j, np.kron(S[i], S[j])])
    return np.real(M)


class Parameters_Mueller(object):
    """Class for Mueller Matrix Parameters

    Args:
        mueller_matrix (Mueller_matrix): Mueller Matrix

    Attributes:
        self.M (Mueller_matrix)
        self.dict (dict): dictionary with parameters
    """

    def __init__(self, mueller_matrix=np.matrix(np.zeros((4, 4),
                                                         dtype=float))):
        self.M = mueller_matrix
        self.dict = {}

    def __repr__(self):
        """print all parameters
        TODO"""
        self.get_all()
        header = "parameters:\n"
        # text = json.dumps(self.dict, indent=4)
        text = self.dict.__repr__()
        text = text.replace(",", "\n    ", 7)
        text = text.replace("{", "")
        text = text.replace("}", "")
        text = text.replace("'polarized'", "\n     'polarized'")
        text = text.replace("'unpolarized'", "+ 'unpolarized'")
        text = "    " + text
        return header + text

    def help(self):
        """prints help about dictionary
        TODO"""

        text = "Here we explain the meaning of parameters.\n"
        text = text + "    intensity: intensity of the light beam.\n"
        text = text + "    TODO"
        print(text)

    def get_all(self):
        """returns a dictionary with all the parameters of Mueller Matrix"""
        # self.dict['intensity'] = self.intensity()
        # self.dict['degree_pol'] = self.degree_polarization()
        # self.dict['degree_linear_pol'] = self.degree_linear_polarization()
        # self.dict['degree_circular_pol'] = self.degree_circular_polarization()
        # self.dict['ellipticity'] = self.ellipticity()
        # self.dict['azimuth'] = self.azimuth()
        # self.dict['eccentricity'] = self.eccentricity()
        # self.dict['ellipse_parameters'] = self.ellipse_parameters()
        # polarized, unpolarized = self.polarized_unpolarized()
        # self.dict['polarized'] = np.squeeze(np.asarray(polarized)).tolist()
        # self.dict['unpolarized'] = np.squeeze(np.asarray(unpolarized)).tolist()
        pass

    def mic(self):
        """Calculates the mean intensity coefficient.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (4x4 numpy.matrix): Mueller matrix

        Returns:
            (float): Diattenuation
        """
        M = self.M
        return M[0, 0]

    def inhomogeneity(self):
        """Calculates the inhomogeneity parameter.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 119.

        Args:
            M (4x4 numpy.matrix): Mueller matrix.

        Returns:
            eta (float): Inhomogeneity parameter.
        """
        M = self.M
        tr = np.trace(M)
        det = np.linalg.det(M)
        m00 = M[0, 0]
        T = 1 / sqrt(2) * (tr + M[0, 1] + M[1, 0] + 1j * (M[3, 2] + M[2, 3])
                           ) / sqrt(m00 + M[1, 1] + M[1, 0] + M[0, 1])
        eta2 = (4 * m00 - abs(T)**2 - abs(T**2 - 4 * det**0.25)) / (
            4 * m00 - abs(T)**2 + abs(T**2 - 4 * det**0.25))
        return sqrt(eta2)

    # Purity components

    def diattenuation(self, normalize=True):
        """Calculates the diattenuation of a Mueller matrix or a diattenuation
        vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (4x4 numpy.matrix or 1x3 array): Mueller matrix or diattenuation
                vector.
            normalize (bool): If True, for matrices it will always normalize by m00.

        Returns:
            D (float): Diattenuation
        """
        # In case it is a matrix, take the depolarization vector
        M = self.M
        m00 = M[0, 0]
        if M.size == 16:
            M = M[0, 1:4]
            if normalize:
                M = M / m00
        D = sqrt(np.sum(np.power(M, 2)))
        return D

    def diattenuation_linear(self):
        """Calculates the linear diattenuation of a Mueller matrix or a
        diattenuation vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (4x4 numpy.matrix or 1x3 array): Mueller matrix or diattenuation
                vector.

        Returns:
            Dl (float): Linear diattenuation
        """
        # Take the interesting part
        M = self.M

        if M.size == 16:
            M = M[0, 1:3] / M[0, 0]
        else:
            M = M[0:2]
        Dl = sqrt(np.sum(np.power(M, 2)))
        return Dl

    def diattenuation_circular(self):
        """Calculates the circular diattenuation of a Mueller matrix or a
        diattenuation vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (4x4 numpy.matrix or 1x3 array): Mueller matrix or diattenuation
                vector.

        Returns:
            Dc (float): Circular diattenuation
        """
        M = self.M

        if M.size == 16:
            Dc = M[0, 3] / M[0, 0]
        else:
            Dc = M[2]
        return Dc

    def polarizance(self, normalize=True):
        """Calculates the polarizance of a Mueller matrix or a polarizance
        vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix or 1x3 array): Mueller matrix or polarizance vector.
            normalize (bool): If True, for matrices it will always normalize by m00.

        Returns:
            P (float): Polarizance
        """
        # In case it is a matrix, take the depolarization vector
        M = self.M
        m00 = M[0, 0]
        if M.size == 16:
            M = M[1:4, 0]
            if normalize:
                M = M / m00
        P = sqrt(np.sum(np.power(M, 2)))
        return P

    def polarizance_linear(self):
        """Calculates the linear polarizance of a Mueller matrix or a polarizance
        vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix or 1x3 array): Mueller matrix or diattenuation vector.

        Returns:
            Pl (float): Linear polarizance
        """
        # Take the interesting part only
        M = self.M
        if M.size == 16:
            M = M[1:3, 0] / M[0, 0]
        else:
            M = M[0:2]
        Pl = sqrt(np.sum(np.power(M, 2)))
        return Pl

    def polarizance_circular(self):
        """Calculates the linear polarizance of a Mueller matrix or a polarizance
        vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix or 1x3 array): Mueller matrix or diattenuation vector.

        Returns:
            Pc (float): Cilcular polarizance
        """
        M = self.M
        if M.size == 16:
            Pc = M[3, 0] / M[0, 0]
        else:
            Pc = M[2]
        return Pc

    def polarizance_degree(self):
        """Calculates the degree of polarizance.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.

        Returns:
            Pd (1x3 array): Degree of polarizance
        """
        P = self.polarizance()
        D = self.diattenuation()
        Pp = sqrt((P**2 + D**2) / 2)
        return Pp

    def spheric_purity(self):
        """Calculates the spheric purity grade.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.

        Returns:
            Ps (1x3 array): spheric purity grade.
        """
        M = self.M
        Ps = 0
        for i in range(1, 4):
            for j in range(1, 4):
                Ps += M[i, j]**2
        return sqrt(Ps / 3) / M[0, 0]

    # Similar to purity grades
    def delay(self):
        """Calculates the delay of the Mueller matrix of a pure retarder.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 128.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.

        Returns:
            (1x3 array): Retardance vector.
        """
        # In case we have absorption/reflection, substract it
        M = self.M
        M = M / M[0, 0]
        # Calculate delay
        cD = np.trace(M) / 2 - 1
        D = np.arccos(cD)
        return D

    def diattenuation_vect(self):
        """Calculates the diattenuation vector of the Mueller matrix.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 129.

        Args:
            M (numpy.matrix): Mueller matrix.

        Returns:
            D (1x3 array): Retardance vector.
        """
        # In case we have absorption/reflection, substract it
        M = self.M
        M = M / M[0, 0]
        # Calculate it
        D = np.array([M[0, 1], M[0, 2], M[0, 3]])
        return D

    def polarizance_vect(self):
        """Calculates the polarizance vector of the Mueller matrix.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 129.

        Args:
            M (numpy.matrix): Mueller matrix.

        Returns:
            P (1x3 array): Retardance vector.
        """
        # In case we have absorption/reflection, substract it
        M = self.M
        M = M / M[0, 0]
        # Calculate it
        P = np.array([M[1, 0], M[2, 0], M[3, 0]])
        return P

    def retardance(self):
        """Calculates the retardance vector of the Mueller matrix of a retarder.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 129.

        Args:
            M (numpy.matrix): Mueller matrix.

        Returns:
            R (1x3 array): Retardance vector.
        """
        # In case we have absorption/reflection, substract it
        M = self.M
        M = M / M[0, 0]
        # Calculate the delay
        D = self.delay()
        # Calculate retardance
        ur = np.zeros(3)
        ur[0] = M[2, 3] - M[3, 2]
        ur[1] = M[3, 1] - M[1, 3]
        ur[2] = M[1, 2] - M[2, 1]
        # If D == 0, take the limit
        if D == 0:
            cte = 0.5
        else:
            cte = D / (2 * sin(D))
        return cte * ur

    # Polarization or despolarization
    def polarimetric_purity(self):
        """Calculates the degree of polarimetric purity of a Mueller matrix.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.

        Returns:
            PD (float): Degree of polarimetric purity.
        """
        Pp = self.polarizance_degree()
        Ps = self.spheric_purity()
        PD = sqrt(2. / 3. * Pp**2 + Ps**2)
        return PD

    def depolarization_degree(self):
        """Calculates the depolarization degree of a Mueller matrix.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.

        Returns:
            DD (float): Depolarization degree.
        """
        PD = self.polarimetric_purity()
        DD = sqrt(1. - PD**2)
        return DD

    def depolarization_factors(self):
        """Euclidean distance between

        After: Handbook of Optics vol 2. 22.49 (46 and 47)

        Args:
            M (4x4 numpy.matrix): Mueller matrix

        Returns:
            (float): Euclidean distance of the normalized Mueller matrix from ideal depolarizer
            (float): Dep(M) depolarization of the matrix
        """

        M = self.M
        quadratic_sum = (array(M)**2).sum()
        euclidean_distance = sqrt(quadratic_sum - M[0, 0]**2) / M[0, 0]
        depolarization = 1 - euclidean_distance / sqrt(3)

        return euclidean_distance, depolarization

    # Polarimetric purity

    def polarimetric_purity_indices(self):
        """Calculates the polarimetric purity indices of a Mueller matrix.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 208.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.

        Returns:
            l (1x3 array): Polarimetric purity indices.
        """
        M = self.M
        # Calculate eigenvalues of covariance matrix
        H = covariance_matrix(M)
        th = np.absolute(np.trace(H))
        l_n, _ = np.linalg.eig(H)
        l_n = np.sort(np.absolute(l_n))
        # Calculate indices
        P1 = (l_n[3] - l_n[2]) / th
        P2 = (l_n[3] + l_n[2] - 2 * l_n[1]) / th
        P3 = (l_n[3] + l_n[2] + l_n[1] - 3 * l_n[0]) / th
        return [P1, P2, P3]


class Mueller(object):
    """Class for Mueller matrices

    Args:
        name (str): name of vector for string representation

    Attributes:
        self.M (numpy.matrix): 4x4 matrix
        self.parameters (class): parameters of Mueller
    """

    def _actualize(f):
        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            f(inst, *args, **kwargs)
            inst.set()
            return

        return wrapped

    def __init__(self, name='M'):
        self.name = name
        self.M = np.matrix(np.zeros((4, 4), dtype=float))
        self.parameters = Parameters_Mueller(self.M)

    def __mul__(self, other):
        """Multiplies two Mueller Matrices.

        Args:
            other (Mueller): 2nd Mueller matrix to multiply

        Returns:
            Stokes: `s3 = s1 * s2`
        """
        M3 = Mueller()

        if isinstance(other, (int, float, complex)):
            M3 = self.M * other
        elif isinstance(other, self.__class__):
            M3.M = self.M * other.M
            M3.name = self.name + " * " + other.name
        # TODO: Falta multiplicar por vector de Stokes
        else:
            raise ValueError('other is Not number or Mueller')
        return M3

    def __rmul__(self, other):
        """Multiplies two Mueller Matrices.

        Args:
            other (Mueller): 2nd Mueller matrix to multiply

        Returns:
            Stokes: `s3 = s1 * s2`
        """
        M3 = Mueller()

        if isinstance(other, (int, float, complex)):
            M3 = other * self.M
        elif isinstance(other, self.__class__):
            M3.M = other.M * self.M
            M3.name = self.name + " * " + other.name
        else:
            raise ValueError('other is Not number or Mueller')
        return M3

    def __repr__(self):
        M = np.array(self.M).squeeze()
        l_name = "{} = \n".format(self.name)
        difference = abs(M.round() - M).sum()
        if difference > eps:
            l0 = "  [{:+3.3f}, {:+3.3f}, {:+3.3f}, {:+3.3f}]\n".format(
                M[0, 0], M[0, 1], M[0, 2], M[0, 3])
            l1 = "  [{:+3.3f}, {:+3.3f}, {:+3.3f}, {:+3.3f}]\n".format(
                M[1, 0], M[1, 1], M[1, 2], M[1, 3])
            l2 = "  [{:+3.3f}, {:+3.3f}, {:+3.3f}, {:+3.3f}]\n".format(
                M[2, 0], M[2, 1], M[2, 2], M[2, 3])
            l3 = "  [{:+3.3f}, {:+3.3f}, {:+3.3f}, {:+3.3f}]\n".format(
                M[3, 0], M[3, 1], M[3, 2], M[3, 3])
        else:
            l0 = "  [{:+3.0f}, {:+3.0f}, {:+3.0f}, {:+3.0f}]\n".format(
                M[0, 0], M[0, 1], M[0, 2], M[0, 3])
            l1 = "  [{:+3.0f}, {:+3.0f}, {:+3.0f}, {:+3.0f}]\n".format(
                M[1, 0], M[1, 1], M[1, 2], M[1, 3])
            l2 = "  [{:+3.0f}, {:+3.0f}, {:+3.0f}, {:+3.0f}]\n".format(
                M[2, 0], M[2, 1], M[2, 2], M[2, 3])
            l3 = "  [{:+3.0f}, {:+3.0f}, {:+3.0f}, {:+3.0f}]\n".format(
                M[3, 0], M[3, 1], M[3, 2], M[3, 3])

        return l_name + l0 + l1 + l2 + l3

    def set(self):
        # print("inside set")
        self.parameters.M = self.M
        # print(self.parameters.M)

    def get(self):
        return self.M

    def check(self):
        """
        verifies that is a 4x4 matrix
        verifies that 4x4 Mueller matrix is properly defined
        """

        # TODO: do check function
        print("TODO")
        pass

    @_actualize
    def polarizer_linear(self, p1=1, p2=0, theta=0):
        """Mueller 4x4 matrix for pure linear polarizer
        - Gil, Ossikovski (4.79) - p. 143
        Handbook of Optics vol 2. 22.16 (Table 1) is with q=p1**2, r=p2**2

        Args:
            p1 (float): [0,1] maximum transmission value.
            p2 (float): [0,1] minimum transmission value.
            theta (float): angle of rotation_matrix with respect to 0º.

        Returns:
            ndarray: 4x4 Muller matrix

        Examples:
            >>> polarizer_linear(p1=1, p2=0, theta=0)
            [[ 1.  1.  0.  0.]
            [ 1.  1.  0.  0.]
            [ 0.  0.  0.  0.]
            [ 0.  0.  0.  0.]]

            >>> polarizer_linear(p1=1, p2=0, theta=pi/4)
            [[ 1 0 1 0]
            [ 0 0 0 0]
            [ 1 0 1 0]
            [0 0 0 0]]

            >>> polarizer_linear(p1=1, p2=0, theta=pi/2)
            [[1 1 0 0]
            [-1 1 0 0]
            [0 0 0 0]
            [0 0 0 0]]

        Note:
            # Direct method 1
            return matrix(array([[cos(theta) ** 2, sin(theta) * cos(theta)],
                [sin(theta) * cos(theta), sin(theta) ** 2]]), dtype = float)

            # Direct method 2
            c2b = cos(2 * theta)
            s2b = sin(2 * theta)

            PL = 0.5* matrix(
                array(
                    [[1, c2b, s2b, 0], [c2b, c2b**2, c2b * s2b, 0],
                     [s2b, c2b * s2b, s2b**2, 0], [0, 0, 0, 0]], ),
                dtype=float)

        """

        a = p1**2 + p2**2
        b = p1**2 - p2**2
        c = 2 * p1 * p2

        p_0 = 0.5 * matrix(
            array([[a, b, 0, 0], [b, a, 0, 0], [0, 0, c, 0], [0, 0, 0, c]]))

        if theta == 0:
            self.M = p_0
        else:
            self.M = rotation_matrix(-theta) * p_0 * rotation_matrix(theta)

        return self.M

    @_actualize
    def depolarizer_diattenuator(self, p1, p2, d=1, theta=0, verbose=False):
        """Muller 4x4 matrix for pure linear diattenuator that depolarizes.

        The final Mueller matrix is calculated as:
        M = M(depolarizer) * M(diattenuator)
        with M(depolarizer) = diag(1,d,d,d)


        Args:
            p1 (float): [0,1] maximum transmission value.
            p2 (float): [0,1] minimum transmission value.
            d (float): [1, 0] transmission of the depolarizer
            theta (float): angle of rotation_matrix with respect to 0º.

        Returns:
            ndarray: 4x4 Muller matrix"""

        # Calculate maximum and minimum intensity to use the simple formulas
        IM = (p1**4 + p2**4) / 2
        Im = (p1**2) * (p2**2)
        # Now, calculate the new p1 and p2 as function of d
        p1 = ((IM * (d + 1) + Im * (d - 1) + 2 * sqrt(
            (IM**2 - Im**2) / d)) / (2 * d))**0.25
        p2 = ((IM * (d + 1) + Im * (d - 1) - 2 * sqrt(
            (IM**2 - Im**2) / d)) / (2 * d))**0.25
        if verbose:
            print(p2)
        # Check that the d value is correct
        if np.isnan(p2):
            raise ValueError('Depolarization parameter inserted is too high.')
        # Create the Stokes matrices of the diattenuator and de depolarizer,
        # and multiply them
        M1 = self.polarizer_linear(p1, p2)
        M2 = self.depolarizer(d)
        M = M2 * M1
        # Rotate the matrix if necessary
        if theta != 0:
            M = rotate_mueller(M, theta)
        # Output
        self.M = M
        return self.M

    @_actualize
    def general_diattenuator_param(self, p1, p2, alpha, delta, carac=True):
        """Function that calculates the most general diattenuator from diattenuator
        parameters.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 137.

        Args:
            p1 (float): [0, 1] Square root of the higher transmission for one
                eigenstate.
            p2 (float): [0, 1] Square root of the lower transmission for the other
                eigenstate.
            alpha (float): [0, pi]: tan(alpha) is the ratio between amplitudes of
                the eigenstates  in Jones formalism.
            delta (float): [0, 2*pi]: phase difference between both components of
                the eigenstates in Jones formalism.
            carac (bool): [Default: True] If false, assumes alpha is azimuth and
            delta is elipticity.

        Output:
            M (4x4 matrix): Mueller matrix of the diattenuator.
        """
        # Do this in order to increase performance
        if p1 == 0 and p2 == 0:
            M = np.diag([1, 0, 0, 0])
        elif p1 == 1 and p2 == 1:
            M = np.identity(4)
        else:
            # First, calculate the Jones_vector Matrix
            J = Jones_vector()
            J.general_diattenuator(p1, p2, alpha, delta, carac)
            # Now, transform it to Mueller
            M = self.Jones_to_Mueller(J)
        self.M = M
        return self.M

    @_actualize
    def general_diattenuator_parvect(self, p1, p2, alpha, delta, carac=True):
        """Function that calculates the most general diattenuator from
        diattenuator parameters with the intermediate step of calculating the
        diattenuation vector.

        From:
            "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 142.

        Args:
            p1 (float): [0, 1] Square root of the higher transmission for one eigenstate.
            p2 (float): [0, 1] Square root of the lower transmission for the other eigenstate.
            alpha (float): [0, pi]: tan(alpha) is the ratio between amplitudes of the eigenstates  in Jones formalism.
            delta (float): [0, 2*pi]: phase difference between both components of the eigenstates in Jones formalism.
            carac (bool): [Default: True] If false, assumes alpha is azimuth and delta is elipticity.

        Output:
            M (4x4 matrix): Mueller matrix of the diattenuator.
        """
        # Do this in order to increase performance
        if p1 == 0 and p2 == 0:
            M = np.diag([1, 0, 0, 0])
        elif p1 == 1 and p2 == 1:
            M = np.identity(4)
        else:
            # Transform coordinates if necessary
            if not carac:
                alpha, delta = azimuth_elipt_2_carac_angles(alpha, delta)
            else:
                # Restrict measured values to the correct interval
                alpha = put_in_limits(alpha, "alpha")
                delta = put_in_limits(delta, "delta")
            # Calculate the diattenuation vector
            f = (p1**2 - p2**2) / (p1**2 + p2**2)
            D = array([
                f * cos(2 * alpha), f * sin(2 * alpha) * cos(delta),
                f * sin(2 * alpha) * sin(delta)
            ])
            m00 = 0.5 * (p1**2 + p2**2)
            # Now, transfor it to Mueller
            M = self.general_diattenuator_vect(D, m00)
        self.M = M
        return self.M

    @_actualize
    def general_diattenuator_vect(self, D, m00=1, verbose=True):
        """Function that calculates the most general diattenuator from the
        Diattenuation vector.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 142.

        Args:
            D (1x3 or 3x1 float): Diattenuation vector
            m00 (float, default 1): [0, 1] Parameter of average intensity
            verbose (bool): If true, print warnings.

        Output:
            M (4x4 matrix): Mueller matrix of the diattenuator.
        """
        # D must be a 1x3 row vector
        D = matrix(D)
        if not isrow(D):
            D = D.T
        if not D.size == 3:
            raise ValueError(
                'Diattenuation vector must have exactly 3 elements.')
        # Create the Mueller matrix
        d = diattenuation(D)
        # Depolarization vector may be wrong, check that
        if np.isreal(d):
            if d > 1:
                print('Warning: Diattenuation vector is not real (D > 1).')
                d = 1
            elif d < 0:
                print('Warning: Diattenuation vector is not real (D < 0).')
        else:
            raise ValueError('Diattenuation vector is not real (D complex).')
        # Now we can calculate the small m matrix. If d == 0, use the identity
        if d == 0:
            m = np.eye(3)
        else:
            skd = sqrt(1 - d**2)
            m1 = skd * np.diag([1, 1, 1])
            m2 = (1 - skd) * np.kron(D, D) / d**2
            m = m1 + np.reshape(m2, (3, 3))
        # Now we have all the necessary blocks
        self.M = create_from_blocks(D, D, m, m00)
        return self.M

    @_actualize
    def retarder(self, phase, theta=0):
        """Muller 4x4 matrix for horizontal linear retarder

        After Gil, Ossikovski (4.31) - p. 132
        Handbook of Optics vol 2. 22.16 (Table 1) coincides

        Args:
            phase (float): phase shift for the linear retarder.
            theta (float): angle of rotation_matrix with respect to 0º.

        Returns:
            ndarray: 4x4 retarder matrix
        """

        R = matrix(
            array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0,
                                                cos(phase),
                                                sin(phase)],
                   [0, 0, -sin(phase), cos(phase)]]))

        if theta == 0:
            self.M = R
        else:
            self.M = rotation_matrix(-theta) * R * rotation_matrix(theta)
        return self.M

    @_actualize
    def polarizer_retarder(self, phase, alpha, delta):
        """Muller 4x4 matrix for utils linear retarder
            Gil, Ossikovski (4.32) - p. 132

        Args:
            phase (float): phase shift for the linear retarder.
            alpha (float): rotation_matrix angle
            delta (float): ???

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """

        if alpha == 0 and delta == 0:
            self.M = self.retarder(phase, theta=0)
        else:
            self.M = self.retarder(
                -delta, theta=0) * rotation_matrix(-alpha) * self.retarder(
                    phase, theta=0) * rotation_matrix(alpha) * self.retarder(
                        delta, theta=0)
        return self.M

    @_actualize
    def quarter_wave(self, theta=0 * degrees):
        """Muller 4x4 matrix for quarter wave retarder.
        It is used to convert linear light into circular light
        Gil, Ossikovski (4.32) - p. 132

        Args:
            theta (float): angle of quarter plate wave

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """

        # Definicion de la matrix
        quarter_wave_0 = matrix(
            array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]]))

        if theta == 0:
            self.M = quarter_wave_0
        else:
            self.M = rotation_matrix(
                -theta) * quarter_wave_0 * rotation_matrix(theta)

        self.parameters.M = self.M
        return self.M

    @_actualize
    def half_wave(self, theta=0 * degrees):
        """Muller 4x4 matrix for half wave retarder.
        It is used to convert change angle of incident polarization

        Args:
            theta (float): angle of half plate wave

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """

        half_wave_0 = matrix(
            array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]))

        if theta == 0:
            self.M = half_wave_0
        else:
            self.M = rotation_matrix(-theta) * half_wave_0 * rotation_matrix(
                theta)
        return self.M

    @_actualize
    def diattenuating_retarder_deprecated(self,
                                          p1,
                                          p2,
                                          phase,
                                          theta=0 * degrees):
        """Muller 4x4 matrix for utils linear retarder with a certain diattenuation
            Gil, Ossikovski (4.98) - p. 146

        Args:
            p1 (float): maximun
            p2 (float): minimum
            phase (float): phase shift for the linear retarder.
            theta (float): angle of diattenuating retarder

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """
        ck = (p1**2 - p2**2) / (p1**2 + p2**2)
        sk = sqrt(1 - ck**2)
        c2f = cos(2 * theta)
        s2f = sin(2 * theta)
        sD = sin(phase)
        cD = cos(phase)

        R = (p1**2 / (1 + ck)) * matrix(
            array([[1, ck * c2f, ck * s2f, 0],
                   [
                       ck * c2f, c2f**2 * ck + sk * cD * s2f**2, s2f * c2f *
                       (1 - sk * cD), -sk * sD * s2f
                   ],
                   [
                       ck * s2f, s2f * c2f * (1 - sk * cD),
                       s2f**2 + sk * cD * c2f**2, sk * sD * c2f
                   ], [0, sk * sD * s2f, -sk * sD * c2f, sk * cD]]))

        if theta == 0:
            self.M = R
        else:
            self.M = rotation_matrix(-theta) * R * rotation_matrix(theta)
        return self.M

    @_actualize
    def diattenuating_retarder(self, p1, p2, phase, theta=0 * degrees):
        """Muller 4x4 matrix for utils linear retarder with a certain diattenuation
            Gil, Ossikovski (4.98) - p. 146

            Luismi, creo que aqui tienes algun fallo. Abajo te pongo mi funcion,
            que se que funciona.

        Args:
            p1 (float): maximun
            p2 (float): minimum
            phase (float): phase shift for the linear retarder.
            theta (float): angle of diattenuating retarder

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """
        ck = (p1**2 - p2**2) / (p1**2 + p2**2)
        sk = sqrt(1 - ck**2)
        c2f = cos(2 * theta)
        s2f = sin(2 * theta)
        sD = sin(phase)
        cD = cos(phase)

        a1 = array([1, ck * c2f, ck * s2f, 0])
        a2 = array([
            ck * c2f, c2f**2 * ck + sk * cD * s2f**2,
            s2f * c2f * (1 - sk * cD), -sk * sD * s2f
        ])
        a3 = array([
            ck * s2f, s2f * c2f * (1 - sk * cD), s2f**2 + sk * cD * c2f**2,
            sk * sD * c2f
        ])
        a4 = array([0, sk * sD * s2f, -sk * sD * c2f, sk * cD])

        R = (p1**2 / (1 + ck)) * matrix(array([a1, a2, a3, a4]))
        self.M = R
        return self.M

    @_actualize
    def Mueller_Real_Retarder(self, p1, p2, delta, theta=0):
        """Muller 4x4 matrix for utils linear retarder with
        a certain diattenuation

        Handbook of Optics, Chapter 22.

        Args:
            p1 (float): maximun
            p2 (float): minimum
            phase (float): phase shift for the linear retarder.
            theta (float): angle of diattenuating retarder

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """
        suma = p1**2 + p2**2
        dif = p1**2 - p2**2
        mult = 2 * p1 * p2
        cd = cos(delta)
        sd = sin(delta)
        M = 0.5 * matrix(
            array([[suma, dif, 0, 0], [dif, suma, 0, 0],
                   [0, 0, mult * cd, mult * sd], [0, 0, -mult * sd, mult * cd]
                   ]))
        self.M = rotate_mueller(M, theta)
        return self.M

    @_actualize
    def depolarizer(self, d, m00=1):
        """converts pure light into light with a certain degree of polarization.
        It is used to convert change angle of incident polarization

        Args:
            d (float or 1x3 array): degree of polarization
            m00 (float, default 1): [0, 1] Parameter of average intensity

        Returns:
            ndarray: 4x4 rotation_matrix matrix
        """
        if np.size(d) == 1:
            depolarizer = np.diag([1, d, d, d])
        else:
            depolarizer = np.diag([1, d[0], d[1], d[2]])

        self.M = m00 * depolarizer
        return self.M

    @_actualize
    def vacuum(self):
        """Muller 4x4 matrix when no sample is included

        Returns:
            ndarray: 4x4 vaccum matrix
        """

        self.M = matrix(
            array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))
        return self.M

    @_actualize
    def Mueller_to_Jones(self):
        """Takes a non-depolarizing Mueller Matrix and converts into Jones matrix

        After: Handbook of Optics vol 2. 22.36 (52-54)

        M = U * (J oX J*) * U^(-1)

        T(M*Mt)=4*m00


        Args:
            M (mumpy.matrix): Mueller matrix

        """

        #TODO: checks non-depolarizing?
        #TODO: better arctan2 than arctan?
        M = self.M
        pxx = sqrt((M[0, 0] + M[0, 1] + M[1, 0] + M[1, 1]) / 2)
        pxy = sqrt((M[0, 0] - M[0, 1] + M[1, 0] - M[1, 1]) / 2)
        pyx = sqrt((M[0, 0] + M[0, 1] - M[1, 0] - M[1, 1]) / 2)
        pyy = sqrt((M[0, 0] - M[0, 1] - M[1, 0] + M[1, 1]) / 2)

        fxy = arctan((-M[0, 3] - M[1, 3]) / (M[0, 2] + M[1, 2] + 1e-15))
        fyx = arctan((M[3, 0] + M[3, 1]) / (M[2, 0] + M[2, 1] + 1e-15))
        fyy = arctan((M[3, 2] - M[2, 3]) / (M[2, 2] + M[3, 3] + 1e-15))

        J = matrix(np.zeros((2, 2), dtype=complex))
        J[0, 0] = pxx
        J[0, 1] = pxy * exp(1j * fxy)
        J[1, 0] = pyx * exp(1j * fyx)
        J[1, 1] = pyy * exp(1j * fyy)

        return (J)

    # Auxiliar matrices
    def covariance_matrix(self):
        """Calculates the covariance matrix of a Mueller matrix.
        Warning 1: the base of matrices S is used in an uncommon order.
        Warning 2: In order to obtain the same result as in the book,
        the formula must be:
            H = 0.25 sum(m[i,j] kron(S[i], np.conj(S[J]) ))

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix 4x4): Mueller matrix or diattenuation vector.

        Returns:
            H (numpy.matrix 4x4): Covariance matrix.
        """
        M = self.M
        H = np.zeros((4, 4), dtype=complex)
        for i in range(4):
            for j in range(4):
                H += M[i, j] * np.kron(S[i], np.conj(S[j]))
                # print([i, j, np.kron(S[i], S[j])])
        return 0.25 * H

    def from_matrix(self, Matrix):
        """Creates a Mueller object directly from the matrix.

        Args:
            Matrix (4x4 numpy.matrix): Mueller matrix

        Returns:
            obj (Mueller): Mueller object."""
        self.M = Matrix
        return self.M


def decompose_polar(M,
                    decomposition='DRP',
                    tol=tol_default,
                    verbose=False,
                    co=False,
                    filter=True):
    """Polar decomposition of a general Mueller matrix in a partial depolarizer,
    retarder and a diattenuator.

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 257.

    Args:
        M (numpy.matrix): Mueller matrix or diattenuation vector.
        decomposition (string): string with the order of the elements:
            depolarizer (D), retarder (R) or diattenuator/polarizer (P).
        tol (float): Tolerance in equalities.
        verbose (float): If true, the function prints out some information
            about the matrices.
        co (bool): If true, the complete output will be thrown.
        filter (bool): If true, the algorithm attempts to filter the Mueller
            matrix before decomposition.

    Returns:
        Mr (numpy.matrix): Mueller matrix of the retarder.
        Md (numpy.matrix): Mueller matrix of the diattenuator.
        param (dictionary): Dictionary with the 9 parameters (7 independent) of
            both the retarder and the diattenuator (optional).
    """
    # Print results
    if verbose:
        print("------------------------------------------------------")
    # Filter the matrix if required
    if filter:
        M = filter_reality_conditions(M, tol)
    # If M is pure, there is no point in continuing in this path, go to the
    # pure decomposition instead
    if is_non_depolarizing(M, tol):  # False:  #
        print("The matrix M is pure.")
        Md = np.identity(4)
        Mr, Mp = decompose_pure(M, right=False, tol=tol)
        p1, p2, alphaP, deltaP, fiP, chiP = parameters_diattenuator(Mp)
    else:
        if decomposition == 'DRP':
            # Calculate the diattenuator/polarizer
            p1, p2, alphaP, deltaP, fiP, chiP = parameters_diattenuator(M)
            Mp = stokes.general_diattenuator_parvect(
                p1, p2, alphaP, deltaP, carac=True)
            D = diattenuation(M)
            # Check if the matrix M is singular or not.
            singM = is_singular2(M, tol=tol)
            singMp = is_singular2(Mp, tol=tol)
            if singMp:
                # We have to determine if only Md is singular or not
                P = polarizance(M)
                cond3 = abs(1 - P) <= tol
                if cond3:
                    # Print type of decomposition
                    if verbose:
                        print(
                            "Both the depolarizer and the polarizer are singular."
                        )
                    # Homogeneous case
                    Md = np.identity(4)
                    Mr, Mp = decompose_pure(M, right=False, tol=tol)
                else:
                    # Print type of decomposition
                    if verbose:
                        print("The polarizer is singular.")
                    # Calculate the depolarizer polarizance vector
                    Dv, Pv, m, m00 = divide_in_blocks(M)
                    Pdv = (Pv - m * Dv.T) / (1 - D**2)
                    Mr = np.identity(4)
                    cero = np.zeros(3)
                    ceroM = np.zeros((3, 3))
                    Md = create_from_blocks(cero, Pdv, ceroM)
            else:
                # Calculate the depolarizer polarizance vector
                Dv, Pv, m, m00 = divide_in_blocks(M)
                Pdv = (Pv - m * Dv.T) / (1 - D**2)
                # For calculating the small matrix m of the depolarizer we need an
                # auxiliary matrix mf
                Gaux = matrix(np.diag([1, -1, -1, -1]))
                if singM:
                    Mpinv = Gaux * Mp * Gaux / D**2
                else:
                    Mpinv = Gaux * Mp * Gaux / (1 - D**2)
                Mf = M * Mpinv
                _, _, mf, _ = divide_in_blocks(Mf)
                md2 = mf * mf.T
                qi2, mr2 = np.linalg.eig(md2)
                qi2, mr2 = order_eig(qi2, mr2)
                # check_eig(qi2, mr2, md2)
                qi = np.sqrt(qi2)
                cero = np.zeros(3)
                # Calculation method depends on Md being singular or not
                if singM:  # If M is singular and Mp is not => Md is singular
                    # Calculate the number of eigenvalues that are zero
                    nz = sum(qi < tol)
                    # Calculate other auxiliary matrices and vectors
                    md1 = mf.T * mf
                    qi12, mr1 = np.linalg.eig(md1)
                    qi12, mr1 = order_eig(qi12, mr1)
                    v1, v2, w1, w2 = (mr2[:, 0], mr2[:, 1], mr1[0, :].T,
                                      mr1[1, :].T)
                    if nz == 3:
                        # Print type of decomposition
                        if verbose:
                            print(
                                "Depolarized matrix singular case with three null eigenvalues."
                            )
                        # Trivial case
                        md = np.zeros([3, 3])
                        Md = create_from_blocks(cero, Pdv, md)
                        Mr = np.eye(4)
                    elif nz == 2:
                        # Print type of decomposition
                        if verbose:
                            print(
                                "Depolarized matrix singular case with two null eigenvalues."
                            )
                        # Depolarizer
                        md = mf * mf.T / sqrt(np.trace(mf * mf.T))
                        Md = create_from_blocks(cero, Pdv, md)
                        # Retarder
                        cR = np.trace(mf) / sqrt(np.trace(mf * mf.T))
                        R = np.arccos(cR)
                        x1 = np.cross(v1.T, w1.T)
                        Mr = stokes.general_retarder_vect(
                            R, R * x1 / np.linalg.norm(x1))
                    else:
                        # Print type of decomposition
                        if verbose:
                            print(
                                "Depolarized matrix singular case with one null eigenvalue."
                            )
                        # Depolarizer
                        md = (qi[0] + qi[1]) * (mf * mf.T + qi[0] * qi[1] *
                                                np.eye(3)).I * mf * mf.T
                        Md = create_from_blocks(cero, Pdv, md)
                        # Retarder
                        (y1, y2) = (np.cross(v1.T, v2.T), np.cross(w1.T, w2.T))
                        mr = v1 * w1.T + v2 * w2.T + y1 * y2.T / (
                            np.linalg.norm(y1) * np.linalg.norm(y2))
                        Mr = create_from_blocks(cero, cero, mr)
                else:
                    # Print type of decomposition
                    if verbose:
                        print("General case.")
                    # General case
                    s = np.sign(np.linalg.det(M))
                    md = np.diag([qi[0], qi[1], s * qi[2]])
                    md = mr2 * md * mr2.T
                    Md = create_from_blocks(cero, Pdv, md)
                    # Calculate the retarder
                    mdinv = mr2 * np.diag([1 / qi[0], 1 / qi[1], s / qi[2]
                                           ]) * mr2.T
                    mr = mdinv * mf
                    Mr = create_from_blocks(cero, cero, mr)
        else:
            raise ValueError("Decomposition not yet implemented.")
    # Order the output matrices
    Mout = [0, 0, 0]
    for ind in range(3):
        if decomposition[ind] == 'D':
            Mout[ind] = Md
        elif decomposition[ind] == 'P':
            Mout[ind] = Mp
        else:
            Mout[ind] = Mr
    # Calculate parameters
    if verbose or co:
        R, alphaR, deltaR, fiR, chiR = parameters_retarder(Mr)
        Pd = polarizance(Md)
        Desp = depolarization_degree(Md)
    # Calculate error
    if co or verbose:
        if decomposition == 'DRP':
            Mt = Md * Mr * Mp
            D = np.abs(Mt - M)
        MeanErr = np.std(np.square(D))
        MaxErr = D.max()
    # Print results
    if verbose:
        if decomposition == 'DRP':
            print("Polar decomposition of the matrix M = Mdesp * Mr * Mp:")
        for ind in range(3):
            print("")
            if decomposition[ind] == 'D':
                print("The depolarizer Mueller matrix is:")
                print(Md)
                print("Parameters:")
                print(("  - Polarizance = {}.".format(Pd)))
                print(("  - Depolarization degree = {}.".format(Desp)))
            elif decomposition[ind] == 'P':
                print("The diatenuator/polarizer Mueller matrix is:")
                print(Mp)
                print("Parameters:")
                print(("  - p1 = {}; p2 = {}.".format(p1, p2)))
                print(
                    ("  - Angle = {}º; Delay between components = {}º.".format(
                        (alphaP / degrees), (deltaP / degrees))))
                print(("  - Azimuth = {}º; Ellipticity = {}º.".format(
                    (fiP / degrees), (chiP / degrees))))
            else:
                print("The retarder Mueller matrix is:")
                print(Mr)
                print("Parameters:")
                print(("  - Delay = {}º.".format((R / degrees))))
                print(
                    ("  - Angle = {}º; Delay between components = {}º.".format(
                        (alphaR / degrees), (deltaR / degrees))))
                print(("  - Azimuth = {}º; Ellipticity = {}º.".format(
                    (fiR / degrees), (chiR / degrees))))
        print("")
        print(("The mean square error in the decomposition is: {}".format(
            MeanErr)))
        print(("The maximum error in the decomposition is: {}".format(MaxErr)))
        print("------------------------------------------------------")
    # Dictionary of parameters
    if co:
        param = dict(
            Delay=R,
            AngleR=alphaR,
            AxisDelayR=deltaR,
            AzimuthR=chiR,
            EllipticityR=fiR,
            p1=p1,
            p2=p2,
            AngleP=alphaP,
            AxisDelayP=deltaP,
            AzimuthP=fiP,
            EllipticityP=chiP,
            DespPolarizance=Pd,
            DespDegree=Desp,
            MeanError=MeanErr,
            MaxError=MaxErr)
    # Output
    if co:
        return Mout[0], Mout[1], Mout[2], param
    else:
        return Mout[0], Mout[1], Mout[2]


class Parameters_Mueller_Analysis(object):
    """Class for Analysis of Mueller Analysis
    TODO: Explanation

    Args:
        mueller_matrix (Mueller_matrix): Mueller Matrix

    Attributes:
        self.M (Mueller_matrix)
        self.dict (dict): dictionary with parameters
    """

    def __init__(self, Mueller_matrix=np.matrix(np.zeros((4, 4),
                                                         dtype=float))):
        self.M = Mueller_matrix
        self.dict = {}

    def __repr__(self):
        """print all parameters"""
        self.get_all()
        header = "parameters:\n"
        # text = json.dumps(self.dict, indent=4)
        text = self.dict.__repr__()
        text = text.replace(",", "\n    ", 7)
        text = text.replace("{", "")
        text = text.replace("}", "")

        text = "    " + text
        return header + text

    def help(self):
        """prints help about dictionary"""

        text = "Here we explain the meaning of parameters.\n"
        text = text + "    intensity: intensity of the light beam.\n"
        text = text + "    TODO"
        print(text)

    def ejemplo_de_metodo(self):
        """Un ejemplo de cómo no necesitamos colocar los metodos de Parameter
        como funciones externas o algo así, ya que podemos acceder a ellos
        desde un nuevo objeto de clase Mueller."""
        M = Mueller()
        M.from_matrix(self.M)
        # Ya podemos usar los metodos de parameters
        pol = M.parameters.polarizance()

    def parameters_diattenuator(self, param="all", diat=True):
        """Calculates all the parameters from the Mueller Matrix of a
        diattenuator.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix or 1x3 array): Mueller matrix or diattenuation or
                polarizance vector.
            param (string): Determines the output. There are three options, all,
                carac and azimuth.
            diat (bool): In case a matrix is inserted, use the diattenuation (True)
                or polarizance vector.

        Returns:
            p1, p2 (float): Axis attenuations.
            alpha (float): Rotation angle.
            delta (float): Delay between eigenstates.
            fi (float): Azimuth.
            chi (float): Ellipticity.
        """

        M = self.M
        # In case it is a matrix, extract the diattenuation or polarizance vector
        if np.size(M) == 16:
            m00 = M[0, 0]
            if diat:
                D = diattenuation(M)
                Dv = diattenuation_vect(M)
            else:
                D = polarizance(M)
                Dv = polarizance_vect(M)
        else:
            Dv = M
            m00 = 1
            D = diattenuation(M)
        # Calculate p1 and p2
        p1 = sqrt(m00 * (1 + D))
        p2 = sqrt(m00 * (1 - D))
        # If the vector is all 0, nothing can be calculated
        if (Dv == 0).all():
            alpha, delta = (0, 0)
            chi, fi = (0, 0)
        else:
            # Calculate alpha, is easy
            c2a = Dv[0] / D
            alpha = np.arccos(c2a) / 2
            # Delta is a little bit more complex
            delta = np.arctan(Dv[2] / Dv[1])
            if delta < 0:
                delta += pi
            if Dv[2] < 0:
                delta += pi
            # Restrict measured values to the correct interval (shouldn't be
            # necessary, but just in case)
            alpha = put_in_limits(alpha, "alpha")
            delta = put_in_limits(delta, "delta")
            # Measure the equivalent coordinates
            chi, fi = carac_angles_2_azimuth_elipt(alpha, delta)
        # Output
        if param == "all":
            return p1, p2, alpha, delta, chi, fi
        elif param == "carac":
            return p1, p2, alpha, delta
        else:
            return p1, p2, chi, fi

    def parameters_polarizer(self, param="all"):
        """Calculates all the parameters from the Mueller Matrix of a
        diattenuator.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.
            param (string): Determines the output. There are three options, all,
                carac and azimuth.

        Returns:
            p1, p2 (float): Axis attenuations.
            alpha (float): Rotation angle.
            delta (float): Delay between eigenstates.
            fi (float): Azimuth.
            chi (float): Ellipticity.
        """
        M = self.M
        p1, p2, alpha, delta, chi, fi = parameters_diattenuator(
            M.T, param="all", diat=False)
        # Output
        if param == "all":
            return p1, p2, alpha, delta, chi, fi
        elif param == "carac":
            return p1, p2, alpha, delta
        else:
            return p1, p2, chi, fi

    def parameters_retarder(self, param="all"):
        """Calculates all the parameters from the Mueller Matrix of a
        diattenuator.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.
            param (string): Determines the output. There are three options, all,
                carac and azimuth.

        Returns:
            R (float): Delay.
            alpha (float): Rotation angle.
            delta (float): Delay between eigenstates.
            fi (float): Azimuth.
            chi (float): Ellipticity.
        """
        M = self.M
        # Calculate the delay
        D = delay(M)
        # This formula doesn't work for D = 0 and D = pi.
        if D == 0:
            ur = array([0, 0, 0])
        elif D == pi:
            ur = array(
                [sqrt(M[1, 1] + 1),
                 sqrt(M[2, 2] + 1),
                 sqrt(M[3, 3] + 1)])
        else:
            ur = array([
                M[2, 3] - M[3, 2], M[3, 1] - M[1, 3], M[1, 2] - M[2, 1]
            ]) / (2 * sin(D))
        # Just in case, ||ur|| should be <= 1
        urmod = np.linalg.norm(ur)
        if urmod > 1:
            ur /= urmod
        # Calculate the parameters using az and el to avoid some ambiguity
        chi = np.arcsin(ur[2]) / 2
        fi = np.arcsin(ur[1] / cos(2 * chi)) / 2
        # print([fi / degrees, chi / degrees])
        if fi < 0:
            if np.sign(ur[0]) == 1:
                fi += pi
            else:
                fi = pi / 2 - fi
        else:
            if np.sign(ur[0]) == -1:
                fi = pi / 2 - fi
        alpha, delta = jones.azimuth_elipt_2_carac_angles(fi, chi)
        # Output
        if param == "all":
            return D, alpha, delta, fi, chi
        elif param == "carac":
            return D, alpha, delta
        else:
            return D, fi, chi

    def parameters_diattenuator_deprecated(self, param="all", diat=True):
        """Calculates all the parameters from the Mueller Matrix of a
        diattenuator.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        Args:
            M (numpy.matrix or 1x3 array): Mueller matrix or diattenuation or
                polarizance vector.
            param (string): Determines the output. There are three options, all,
                carac and azimuth.
            diat (bool): In case a matrix is inserted, use the diattenuation (True)
                or polarizance vector.

        Returns:
            p1, p2 (float): Axis attenuations.
            alpha (float): Rotation angle.
            delta (float): Delay between eigenstates.
            fi (float): Azimuth.
            chi (float): Ellipticity.
        """
        # In case it is a matrix, extract the diattenuation or polarizance vector
        M = self.M
        if np.size(M) == 16:
            m00 = M[0, 0]
            if diat:
                D = diattenuation(M)
                Dv = diattenuation_vect(M)
            else:
                D = polarizance(M)
                Dv = polarizance_vect(M)
        else:
            Dv = M
            m00 = 1
            D = diattenuation(M)
        # Calculate p1 and p2
        p1 = sqrt(m00 * (1 + D))
        p2 = sqrt(m00 * (1 - D))
        # If the vector is all 0, nothing can be calculated
        if (Dv == 0).all():
            alpha, delta = (0, 0)
            chi, fi = (0, 0)
        else:
            # Acoid dividing by 0
            if Dv[0] == 0:
                alpha = pi / 4
            else:
                t2a = sqrt(Dv[1]**2 + Dv[2]**2) / abs(Dv[0])
                alpha = np.arctan(t2a) / 2
            if Dv[1] == 0:
                delta = np.sign(Dv[2]) * pi / 2
            else:
                td = Dv[2] / Dv[1]
                delta = np.arctan(td)
            # Restrict measured values to the correct interval
            if alpha < limAlpha[0] or alpha > limAlpha[1]:
                aux = sin(alpha)
                alpha = np.arcsin(abs(aux))
            if delta < limDelta[0] or delta > limDelta[1]:
                delta = delta % (2 * pi)
            # Measure the equivalent coordinates
            fi, chi = carac_angles_2_azimuth_elipt(alpha, delta)
        # Output
        if param == "all":
            return p1, p2, alpha, delta, fi, chi
        elif param == "carac":
            return p1, p2, alpha, delta
        else:
            return p1, p2, fi, chi

    # # Matrix filtering
    def filter_reality_conditions(self,
                                  tol=tol_default,
                                  verbose=False,
                                  counter=0):
        """Function that filters experimental errors by forcing the Mueller matrix
        M to fulfill the conditions necessary for a matrix to be real.
        Args:
            M (4x4 matrix): Experimental Mueller matrix.
            tol (float): Tolerance in equalities.
            verbose (float): If true, the function prints out some information
                about the algorithm and matrices.
            counter (int): Auxiliar variable that shoudln't be changed
        Output:
            Mf (4x4 matrix): Filtered Mueller matrix.
        """
        M = self.M
        if verbose:
            print("The original matrix is:")
            print(M)
        # Check if the matrix is already real
        cond, inf = is_real(M, tol, True)
        # If it is not real, filter. The order of conditions is slightly altered to
        # place easy errors first and complex ones which may have higher impact,
        # later.
        if not cond and counter <= counter_max:
            # Zeroth A condition can be fixed changing the sign of m00
            data = inf['cond0a']
            if not data[1]:
                M[0, 0] = -M[0, 0]
                # Print for debug.
                if verbose:
                    print('Zero A condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M

            # Zeroth B condition can be fixed dividing M by m00
            data = inf['cond0b']
            if not data[1]:
                M = M / M[0, 0]
                # Print for debug.
                if verbose:
                    print('Zero B condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M

            # Second condition can be fixed reducing ellements to m00.
            data = inf['cond2']
            if not data[1]:
                m00 = M[0, 0]
                for indx in range(4):
                    for indy in range(4):
                        if abs(M[indx, indy]) > m00:
                            M[indx, indy] = np.sign(M[indx, indy]) * m00
                # Print for debug.
                if verbose:
                    print('Second condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M

            # Third condition can be solved easily reducing polarizance /
            # diattenuation vectors proportionally
            data = inf['cond3a']
            if not data[1]:
                D = diattenuation(M)
                M[0, 1] = M[0, 1] / D
                M[0, 2] = M[0, 2] / D
                M[0, 3] = M[0, 3] / D
                # Print for debug.
                if verbose:
                    print('Third A condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M
            # Condition 3B
            data = inf['cond3b']
            if not data[1]:
                P = polarizance(M)
                M[1, 0] = M[1, 0] / P
                M[2, 0] = M[2, 0] / P
                M[3, 0] = M[3, 0] / P
                # Print for debug.
                if verbose:
                    print('Third B condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M

            # First condition can be fixed reducing all elements except m00
            # proportionally.
            data = inf['cond1']
            if not data[1]:
                m00 = M[0, 0]
                tr = np.trace(M * M.T)
                f = 3 * m00 / sqrt(tr - m00**2)
                M = M * f
                M[0, 0] = m00
                # Print for debug.
                if verbose:
                    print('First condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                # print('Fix cond1')
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M

            # Fifth condition can be solved decreasing all matrix elements so Tmax =
            # m00*(1 + D) = 1. And as Mt must be real also, do the same with P.
            data = inf['cond5a']
            if not data[1]:
                D = diattenuation(M, normalize=False)
                m00 = M[0, 0]
                # If m00 = 1, we have a rotator here, make P vector 0
                if m00 == 1:
                    M[0, 1] = 0
                    M[0, 2] = 0
                    M[0, 3] = 0
                # If not, divide the D vector so it has the maximum possible D
                else:
                    Dnew = 1 - m00
                    M[0, 1] = M[0, 1] * Dnew / D
                    M[0, 2] = M[0, 2] * Dnew / D
                    M[0, 3] = M[0, 3] * Dnew / D
                    # Print for debug.
                if verbose:
                    print('Fifth A condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                # print('Fix cond5')
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M
            # Condition 5B
            data = inf['cond5b']
            if not data[1]:
                P = polarizance(M, normalize=False)
                m00 = M[0, 0]
                # If m00 = 1, we have a rotator here, make D vector 0
                if m00 == 1:
                    M[1, 0] = 0
                    M[2, 0] = 0
                    M[3, 0] = 0
                # If not, divide the D vector so it has the maximum possible D
                else:
                    Pnew = 1 - m00
                    M[1, 0] = M[1, 0] * Pnew / P
                    M[2, 0] = M[2, 0] * Pnew / P
                    M[3, 0] = M[3, 0] * Pnew / P
                # Print for debug.
                if verbose:
                    print('Fifth B condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                # print('Fix cond5')
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M

            # Sixth condition can be fixed by making zero low enough eigenvalues
            data = inf['cond6']
            if not data[1]:
                # Calculate covariance matrix eigenvalues
                H = covariance_matrix(M)
                qi, U = np.linalg.eig(H)
                qi, U = order_eig(qi, U)
                U = np.matrix(U)
                # Make the smaller ones zero
                for ind, q in enumerate(qi):
                    if q < tol:
                        qi[ind] = 0
                    elif q > 1:
                        qi[ind] = 1
                # Recompose the matrix
                Hf = U * np.diag(qi) * U.H
                # Go back to Mueller
                M = inverse_covariance(Hf)
                # Print for debug.
                if verbose:
                    print('Sixth condition was violated. Fixed matrix is:')
                    print(M)
                # Use recursivity to recheck the rest of conditions with the new
                # matrix
                # print('Fix cond6')
                counter = counter + 1
                M = filter_reality_conditions(M, tol, verbose, counter)
                return M
        else:
            # Print for debug.
            if verbose:
                if counter > counter_max:
                    print('Maximum number of iterations reached.')
                else:
                    print('None condition was violated.')
            # Nothing has to be done
            counter = 0
            return M

    # # Matrix decomposition

    def decompose_pure(self,
                       right=True,
                       tol=tol_default,
                       verbose=False,
                       co=False):
        """Polar decomposition of a pure Mueller matrix in a retarder and a
        diattenuator.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 151.

        Args:
            M (numpy.matrix): Mueller matrix or diattenuation vector.
            right (bool): the diattenuator is calculated to be at the right of the
                retarder.
            tol (float): Tolerance in equalities.
            verbose (float): If true, the function prints out some information
                about the matrices.
            co (bool): If true, the complete output will be thrown.

        Returns:
            Mr (numpy.matrix): Mueller matrix of the retarder.
            Md (numpy.matrix): Mueller matrix of the diattenuator.
            param (dictionary): Dictionary with the 9 parameters (7 independent) of
                both the retarder and the diattenuator (optional).
        """
        M = self.M
        # Just in case
        M = np.matrix(M)
        # Calculate the diattenuator Parameters
        if right:
            p1, p2, alphaD, deltaD, fiD, chiD = parameters_diattenuator(M)
        else:
            p1, p2, alphaD, deltaD, fiD, chiD = parameters_polarizer(M)
        # Calculate the diattenuator Matrix
        Md = stokes.general_diattenuator_parvect(
            p1, p2, alphaD, deltaD, carac=True)
        # In order to proceed, we have to know if M is singular or not.
        cond2 = is_singular2(M, tol=tol)
        if cond2:
            # Singular matrix. We have to check that P or D vectors are not nule.
            Pv = polarizance_vect(M)
            Dv = diattenuation_vect(M)
            c1 = (abs(Pv) <= tol).all()
            c2 = (abs(Dv) <= tol).all()
            if c1 and c2:
                # If P and D are 0, then we started with a retarder all the time
                Mr = M
                if co or verbose:
                    R, alphaR, deltaR, fiR, chiR = parameters_retarder(M)
            else:
                # Calculate the retarder with minimum delay
                cR = np.dot(Pv, Dv)
                R = np.arccos(cR)
                pv = np.cross(Pv, Dv)
                Rv = R * pv / np.linalg.norm(Pv)
                Mr = stokes.general_retarder_vect(R, Rv)
                # Extract the other parameters
                if co or verbose:
                    _, alphaR, deltaR, fiR, chiR = parameters_retarder(Mr)
        else:
            # Non-singular matrix. Multiply by Md^(-1) at the correct side
            if right:
                Mr = M * Md.I
            else:
                Mr = Md.I * M
            # If required, calculate the parameters from the Matrix
            if co or verbose:
                R, alphaR, deltaR, fiR, chiR = parameters_retarder(Mr)
        # Calculate error
        if co or verbose:
            if right:
                Mt = Mr * Md
            else:
                Mt = Md * Mr
            MeanErr = np.mean(sqrt(np.power(M - Mt, 2)))
            MaxErr = abs(M - Mt).max()

        # If required, print the Parameters
        if verbose:
            print("------------------------------------------------------")
            if right:
                print("Matrx M decomposed as M = Mr * Md.")
                print("")
                print("The retarder Mueller matrix is:")
                print(Mr)
                print("Parameters:")
                print(("  - Delay = {}º.".format((R / degrees))))
                print(
                    ("  - Angle = {}º; Delay between components = {}º.".format(
                        (alphaR / degrees), (deltaR / degrees))))
                print(("  - Azimuth = {}º; Ellipticity = {}º.".format(
                    (fiR / degrees), (chiR / degrees))))
                print("")
                print("The diatenuator Mueller matrix is:")
                print(Md)
                print("Parameters:")
                print(("  - p1 = {}; p2 = {}.".format(p1, p2)))
                print(
                    ("  - Angle = {}º; Delay between components = {}º.".format(
                        (alphaD / degrees), (deltaD / degrees))))
                print(("  - Azimuth = {}º; Ellipticity = {}º.".format(
                    (fiD / degrees), (chiD / degrees))))
            else:
                print("Matrx M decomposed as M = Md * Mr.")
                print("")
                print("The diatenuator Mueller matrix is:")
                print(Md)
                print("Parameters:")
                print(("  - p1 = {}; p2 = {}.".format(p1, p2)))
                print(
                    ("  - Angle = {}º; Delay between components = {}º.".format(
                        (alphaD / degrees), (deltaD / degrees))))
                print(("  - Azimuth = {}º; Ellipticity = {}º.".format(
                    (fiD / degrees), (chiD / degrees))))
                print("")
                print("The retarder Mueller matrix is:")
                print(Mr)
                print("Parameters:")
                print(("  - Delay = {}º.".format((R / degrees))))
                print(
                    ("  - Angle = {}º; Delay between components = {}º.".format(
                        (alphaR / degrees), (deltaR / degrees))))
                print(("  - Azimuth = {}º; Ellipticity = {}º.".format(
                    (fiR / degrees), (chiR / degrees))))
            print("")
            print(("The mean square error in the decomposition is: {}".format(
                MeanErr)))
            print(
                ("The maximum error in the decomposition is: {}".format(MaxErr)
                 ))
            print("------------------------------------------------------")
        #  If required, make a dictionary with the Parameters
        if co:
            param = dict(
                Delay=R,
                AngleR=alphaR,
                AxisDelayR=deltaR,
                AzimuthR=chiR,
                EllipticityR=fiR,
                p1=p1,
                p2=p2,
                AngleD=alphaD,
                AxisDelayD=deltaD,
                AzimuthD=fiD,
                EllipticityD=chiD,
                MeanError=MeanErr,
                MaxError=MaxErr)
            return Mr, Md, param
        else:
            return Mr, Md


class Parameters_Mueller_Check(object):
    """Class for Check of Mueller Matrices
    TODO: Explanation

    Args:
        mueller_matrix (Mueller_matrix): Mueller Matrix

    Attributes:
        self.M (Mueller_matrix)
        self.dict (dict): dictionary with parameters
    """

    def __init__(self, Mueller_matrix=np.matrix(np.zeros((4, 4),
                                                         dtype=float))):
        self.M = Mueller_matrix
        self.dict = {}

    def __repr__(self):
        """print all parameters"""
        self.get_all()
        header = "parameters:\n"
        # text = json.dumps(self.dict, indent=4)
        text = self.dict.__repr__()
        text = text.replace(",", "\n    ", 7)
        text = text.replace("{", "")
        text = text.replace("}", "")

        text = "    " + text
        return header + text

    def help(self):
        """prints help about dictionary"""

        text = "Here we explain the meaning of parameters.\n"
        text = text + "    intensity: intensity of the light beam.\n"
        text = text + "    TODO"
        print(text)

    def is_real(self, tol=tol_default, individual=False):
        """Conditions of physical realizability,

        After: Handbook of Optics vol 2. 22.34

        cond0a: m00 <= 1
        cond0b: m00 >= 0
        cond1: Tr(M*Mt)<=4(m00)**2
        cond2: m00>=abs(mij)
        cond3a: (m00)**2>=b**2
        cond3a: (m00)**2>=b'**2
        cond4: (m00-b)**2>=sum(m0,j-sum(mjk*ak))
        cond5a: Tmax=m00+b<=1
        cond5a: Tmax_inv=m00+b'<=1
        cond6a: Eigenvalues of H are >= 0
        cond6b:  Eigenvalues of H are <= 0

        where b=sqrt(m01**2+m02**2+m03**2) and aj=m0j/b
        and also for b'=sqrt(m10**2+m20**2+m30**2) and a'j=mj0/b'

        it also returns distance, if positive, it is fullfilled


        Args:
            M (mumpy.matrix): Mueller matrix
            tol (float): Tolerance in equality conditions
            individual (bool): If true, the function will return the individual
                conditions and distances.

        Returns:
            cond (bool): Is real or not.
            ind (dictionary): dictionary with condition, True/False, distance

        To do:
            condition 4 does not work. In addition I do not understand when
            M=matrix(sp.eye(4)) since b=0 and a= indeterminate

        """
        # M = 0.5 * matrix(sp.eye(4))
        # M[0, 0] = 1
        M = self.M
        b = sqrt(M[0, 1]**2 + M[0, 2]**2 + M[0, 3]**2)
        bp = sqrt(M[1, 0]**2 + M[2, 0]**2 + M[3, 0]**2)

        c0a = M[0, 0]
        c0b = M[0, 0]
        c1 = 4 * M[0, 0]**2 - np.trace(M * M.T)
        c2 = M[0, 0] - (abs(M).max())
        c3a = M[0, 0]**2 - b**2
        c3b = M[0, 0]**2 - bp**2
        # a = M[0, :] / b
        # t1 = float(sum(M[:, 1:-1].transpose(>) * a.transpose()))
        # c4 = (M[0, 0] - b)**2 - sum(array(M[0, 1::]) - t1)
        c5a = -M[0, 0] - b + 1
        c5b = -M[0, 0] - bp + 1

        H = covariance_matrix(M)
        l_n, _ = np.linalg.eig(H)
        l_n = np.sort(np.real(l_n))
        c6 = l_n.min()

        cond0a = c0a >= -tol
        cond0b = c0b <= 1 + tol
        cond1 = c1 >= -tol
        cond2 = c2 >= -tol
        cond3a = c3a >= -tol
        cond3b = c3b >= -tol
        cond5a = c5a >= -tol
        cond5b = c5b >= -tol
        cond6 = c6 >= -tol
        cond = cond0a and cond0b and cond1 and cond2 and cond3a and cond3b and cond5a and cond5b and cond6

        conditions = dict(
            cond0a=[c0a, cond0a],
            cond0b=[c0b, cond0b],
            cond1=[c1, cond1],
            cond2=[c2, cond2],
            cond3a=[c3a, cond3a],
            cond3b=[c3b, cond3b],
            # cond4=[c4, c4 >= 0],
            cond5a=[c5a, cond5a],
            cond5b=[c5b, cond5b],
            cond6=[c6, cond6])
        if individual:
            return cond, conditions
        else:
            return cond

    def is_non_depolarizing(self, tol=tol_default, co=False):
        """Checks if matrix is non-depolarizing (the degree of polarimetric purity
        must be 1).

        Args:
            M (4x4 numpy.matrix): Mueller matrix
            tol (float): Tolerance in equality conditions
            co (bool): If true, the complete output will be thrown.

        Returns:
            cond (bool): True if non-depolarizing
        """
        M = self.M
        PD = polarimetric_purity(M)
        cond = 1 - PD <= tol
        if co:
            return cond, PD
        else:
            return cond

    def is_homogeneous(self, tol=tol_default, co=False):
        """Checks if the matrix is homogeneous.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 119.

        The inhomogeneity parameter must be 0 if M is homogeneous

        Args:
            M (4x4 numpy.matrix): Mueller matrix.
            tol (float): Tolerance in equality conditions.
            co (bool): If true, the complete output will be thrown.

        Returns:
            (bool): True if non-depolarizing.
            (float): Inhomogeneity factor.
        """
        M = self.M
        eta = inhomogeneity(M)
        cond = eta <= tol
        if co:
            return cond, eta
        else:
            return cond

    def is_homogeneous2(self, tol=tol_default, co=False):
        """Checks if the matrix is homogeneous.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 119.

        A matrix is homogeneous if P == D (vectors).It can be measured from the
        inhomogeneity parameter.

        Args:
            M (4x4 numpy.matrix): Mueller matrix.
            tol (float): Tolerance in equality conditions.
            co (bool): If true, the complete output will be thrown.

        Returns:
            (bool): True if non-depolarizing.
            (float): Inhomogeneity factor.
        """
        M = self.M
        u = (M[1:4, 0]).T
        v = M[0, 1:4]
        d = np.power(u - v, 2)
        f = sqrt(np.sum(d)) / 3
        if abs(f) <= tol:
            cond = True
        else:
            cond = False
        if co:
            return cond, f
        else:
            return cond

    def is_retarder(self, tol=tol_default, co=False):
        """Checks if the matrix M corresponds to a pure retarder.There are three
        conditions:
            1) ||P|| = P = 0
            2) ||D|| = D = 0
            3) M^T = M^(-1)
        We can define a non-retarder factor as:
            f = sqrt(sum((M^T-M^(-1))^2))

        Args:
            M (4x4 numpy.matrix): Mueller matrix.
            tol (float): Tolerance in equality conditions.
            co (bool): If true, the complete output will be thrown.

        Returns:
            co = False
                (bool): True if is a retarder.
            co = True
                (1x4 bool): Global and each of the three conditions.
                (1x3 float): P, D and f.
        """
        # divide in blocks to take the m matrix
        M = self.M
        D, P, m, m00 = divide_in_blocks(M)
        # Check that D and P are 0.
        c1 = np.linalg.norm(P) / 3
        c2 = np.linalg.norm(D) / 3
        cond1 = c1 <= tol
        cond2 = c2 <= tol
        # Check that the matrix is not singular (if it is, its not a retarder)
        if np.linalg.det(
                m) < 1e-8:  # No use of tol here, as it is mathematical
            if co:
                return [False, False, False, False], [0, 0, 0]
            else:
                return False
        # Check that the matrix corresponds to a retarder
        aux = m.I - m.T
        f = sqrt(np.sum(np.power(aux, 2)))
        cond3 = f <= tol
        cond = cond1 and cond2 and cond3
        if co:
            return [cond, cond1, cond2, cond3], [c1, c2, f]
        else:
            return cond

    def is_polarizer(self, tol=tol_default, co=False):
        """Checks if the matrix M corresponds to a pure homogeneous polarizer.The
        condition is M = M^T.

        Args:
            M (4x4 numpy.matrix): Mueller matrix.
            tol (float): Tolerance in equality conditions.
            co (bool): If true, the complete output will be thrown.

        Returns:
            cond (bool): True if is a polarizer.
            d (float): distance to violate the condition.
        """
        M = self.M
        d = abs(M - M.T)
        d = np.sum(d) / 16
        cond = d <= tol
        if co:
            return cond, d
        else:
            return cond

    def is_singular(self, tol=tol_default, co=False):
        """Checks if the matrix is singular.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        A matrix is homogeneous if det(M) = 0.

        Args:
            M (4x4 numpy.matrix): Mueller matrix.
            tol (float): Tolerance in equality conditions.
            co (bool): If true, the complete output will be thrown.

        Returns:
            (bool): True if non-depolarizing.
        """
        M = self.M
        det = np.linalg.det(M)
        cond = abs(det) <= tol**2
        if co:
            return cond, det
        else:
            return cond

    def is_singular2(self, tol=tol_default, co=False):
        """Checks if the matrix is singular.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

        A matrix is homogeneous if any of its eigenvalues is 0.

        Args:
            M (4x4 numpy.matrix): Mueller matrix.
            tol (float): Tolerance in equality conditions.
            co (bool): If true, the complete output will be thrown.

        Returns:
            (bool): True if non-depolarizing.
        """
        M = self.M
        l, _ = np.linalg.eig(M)
        ml = min(abs(l))
        cond = ml <= tol
        if co:
            return cond, ml
        else:
            return cond
