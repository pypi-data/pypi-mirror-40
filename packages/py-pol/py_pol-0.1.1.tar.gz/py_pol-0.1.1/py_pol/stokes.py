# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------
# Authors:    Luis Miguel Sanchez Brea and Jesus del Hoyo
# Fecha       2019/01/09 (version 1.0)
# License:    GPL
# -------------------------------------
"""
We present a number of functions for polarization using Stokes framework:

## Light beams
* general
* linear light beam
* circular light beam
* elliptical light beam


## Polarization properties of light beams
* intensity
* degree of polasrization (DOP)
* degree of linear polarization (DOLP)
* degree of circular polarization (DOCP)
* ellipticity
* azimut
* eccentricity


"""
from functools import wraps
from .jones_vector import Jones_vector

import numpy as np
from numpy import arccos, arctan2, array, cos, matrix, pi, sin, sqrt

from . import eps

degrees = pi / 180.

# TODO: Draw polarization ellipse for point/s (from ellipse_parameters)
# TODO: Draw point/s in poincare' sphere (For one/several stokes parameter)
# TODO: función para luz eliptica (a, b, angulo, polarización)? No sabía hacer


# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class CustomError(Error):
    """Raised when a custom error is produced"""
    pass


class Parameters_Stokes_vector(object):
    """Class for Stokes vector Parameters

    Args:
        Stokes_vector (Stokes_vector): Stokes Vector

    Attributes:
        self.M (Stokes_vector)
        self.dict (dict): dictionary with parameters
    """

    def __init__(self, Stokes_vector=np.matrix(np.zeros((4, 1), dtype=float))):
        self.M = Stokes_vector
        self.dict = {}

    def __repr__(self):
        """print all parameters
        """
        # TODO: los angulos estan en radianes, pasar a grados?. Todo manual
        self.get_all()
        header = "parameters:\n"
        text = self.dict.__repr__()
        text = text.replace(",", "\n    ", 7)
        text = text.replace("{", "")
        text = text.replace("}", "")
        text = text.replace("'polarized'", "\n     'polarized'")
        text = text.replace("'unpolarized'", "+ 'unpolarized'")
        text = "    " + text
        return header + text

    def help(self):
        """prints help about dictionary"""

        text = "Here we explain the meaning of parameters.\n"
        text = text + "    intensity: intensity of the light beam.\n"
        text = text + "    TODO"
        print(text)

    def check(self):
        """Checks if stokes vector is real"""
        # TODO: check for stokes vectors
        pass

    def get_all(self):
        """returns a dictionary with all the parameters of Stokes vector"""
        self.dict['intensity'] = self.intensity()
        self.dict['degree_pol'] = self.degree_polarization()
        self.dict['degree_linear_pol'] = self.degree_linear_polarization()
        self.dict['degree_circular_pol'] = self.degree_circular_polarization()
        self.dict['ellipticity'] = self.ellipticity()
        self.dict['azimuth'] = self.azimuth()
        self.dict['eccentricity'] = self.eccentricity()
        self.dict['ellipse_parameters'] = self.ellipse_parameters()
        polarized, unpolarized = self.polarized_unpolarized()
        self.dict['polarized'] = np.squeeze(np.asarray(polarized)).tolist()
        self.dict['unpolarized'] = np.squeeze(np.asarray(unpolarized)).tolist()

        return self.dict

    def intensity(self):
        """
        After: Handbook of Optics vol 2. 22.16 (eq.2)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): s0
        """

        return np.asscalar(self.M[0])

    def degree_polarization(self):
        """DOP parameter to measure the degree of polarization.

        After: Handbook of Optics vol 2. 22.16 (eq.3)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): polarization degree P=sqrt(s1**2+s2**2+s3**2)/s0
        """

        s0, s1, s2, s3 = np.array(self.M).flat
        if s0 == 0:
            return np.nan
        else:
            return sqrt(s1**2 + s2**2 + s3**2) / s0

    def degree_linear_polarization(self):
        """DOLP parameter to measure the degree of linear polarization

        After: Handbook of Optics vol 2. 22.16 (eq.4)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): polarization degree P=sqrt(s1**2+s2**2)/s0
        """

        s0, s1, s2, s3 = np.array(self.M).flat
        if s0 == 0:
            return np.nan
        else:
            return sqrt(s1**2 + s2**2) / s0

    def degree_circular_polarization(self):
        """DOCP parameter to measure the degree of linear polarization

        After: Handbook of Optics vol 2. 22.16 (eq.5)

        I have included abs(P) so that it is between (0-1)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): polarization degree P=sqrt(s1**2+s2**2)/s0
        """

        s0, s1, s2, s3 = np.array(self.M).flat
        if s0 == 0:
            return np.nan
        else:
            return abs(s3 / s0)

    def polarized_unpolarized(self):
        """Stokes beam can be divided in Sp+Su, where Sp is fully-polarized
        and Su fully-unpolarized

        After: Handbook of Optics vol 2. 22.16 (eq.6)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (numpy.array): Sp, fully-polarized Stokes vector
            (numpy.array): Su, fully-unpolarized Stokes vector
        """

        DOP = self.degree_polarization()
        s0, s1, s2, s3 = np.array(self.M).flat
        Sp = matrix(array([[s0 * DOP], [s1], [s2], [s3]]))
        Su = matrix(array([[s0 * (1 - DOP)], [0], [0], [0]]))

        return Sp, Su

    def ellipticity(self):
        """When the beam is *fully polarized*, ratio between semi-axis.

        It's 0 for linearly polarized light and 1 for circulary polarized light

        If S is not fully polarized, ellipticity is computed on Sp

        After: Handbook of Optics vol 2. 22.16 (eq.7)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): e, ellipticity
        """
        S = self.M

        DOP = self.degree_polarization()
        if DOP == 1:
            Sp = S
        else:
            Sp, Su = self.polarized_unpolarized()

        s0, s1, s2, s3 = np.array(Sp).flat
        if (s0 + np.sqrt(s1**2 + s2**2)) == 0:
            return np.nan
        else:
            e = s3 / (s0 + np.sqrt(s1**2 + s2**2))

        return e

    def azimuth(self):
        """When the beam is *fully polarized*, orientation of major axis
        If S is not fully polarized, ellipticity is computed on Sp

        After: Handbook of Optics vol 2. 22.16 (eq.8)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): azimuth, orientation of major axis
        """

        S = self.M
        DOP = self.degree_polarization()
        if DOP == 1:
            Sp = S
        else:
            Sp, Su = self.polarized_unpolarized()

        s0, s1, s2, s3 = np.array(Sp).flat
        if s1 == 0:
            return np.nan
        else:
            azimuth = 0.5 * arctan2(s2, s1)

        return azimuth

    def eccentricity(self):
        """When the beam is *fully polarized*, similar to ellipticity.

        It is 0 for circular polarized light and 1 for linear polarized light.

        If S is not fully polarized, ellipticity is computed on Sp

        After: Handbook of Optics vol 2. 22.16 (eq.8)

        Args:
            S (array): Stokes vector (s0,s1,s2,s3)

        Returns:
            (float): azimuth, orientation of major axis
        """

        e = self.ellipticity()

        return sqrt(1 - e**2)

    def ellipse_parameters(self):
        """
        ellipticity, azimuth, eccentricity

        """
        # TODO: No sería mejor (a,b,angle), hacer otro para dibujar
        return self.ellipticity(), self.azimuth(), self.eccentricity()


class Stokes(object):
    """Class for Stokes vectors

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
            inst.set()
            return

        return wrapped

    def __init__(self, name='J'):
        self.name = name
        self.M = np.matrix(np.zeros((4, 1), dtype=float))
        self.parameters = Parameters_Stokes_vector(self.M)

    def __add__(self, other):
        """Adds two Stokes vectors.
        TODO: (Jesus) Chequear que funciona

        Args:
            other (Stokes): 2nd Stokes vector to add

        Returns:
            Stokes: `s3 = s1 + s2`
        """
        self.parameters.M = self.M
        # Calculate I and V parameters of the new Stokes vector, that are easy
        s0 = np.float(self.M[0] + other.M[0])
        s3 = np.float(self.M[3] + other.M[3])
        # Extract "norm" of linear part of vectors
        norm1 = self.parameters.degree_linear_polarization()
        norm2 = other.parameters.degree_linear_polarization()
        # Extract "angle" of linear part of vectors
        az1 = self.parameters.azimuth()
        az2 = other.parameters.azimuth()
        # Add them as vectors
        v1 = np.array([norm1 * cos(az1), norm1 * sin(az1)])
        v2 = np.array([norm2 * cos(az2), norm2 * sin(az2)])
        v3 = v1 + v2
        # Calculate norm and angle of final vector
        norm3 = np.linalg.norm(v3)
        if norm3 == 0:
            (s1, s2) = (0, 0)
        else:
            az3 = arccos(v3[0] / norm3)
            s1 = norm3 * cos(2 * az3)
            s2 = norm3 * sin(2 * az3)
        # Put the new result in M3
        M3 = Stokes(self.name + " + " + other.name)
        M3.from_elements(s0, s1, s2, s3)

        return M3

    def __sub__(self, other):
        """Substracts two Stokes vectors.

        Args:
            other (Stokes): 2nd Stokes vector to add

        Returns:
            Stokes: `s3 = s1 - s2`
        """
        self.parameters.M = self.M
        # Calculate I and V parameters of the new Stokes vector, that are easy
        s0 = np.float(self.M[0] - other.M[0])
        s3 = np.float(self.M[3] - other.M[3])
        # Extract "norm" of linear part of vectors
        norm1 = self.parameters.degree_linear_polarization()
        norm2 = other.parameters.degree_linear_polarization()
        # Extract "angle" of linear part of vectors
        az1 = self.parameters.azimuth()
        az2 = other.parameters.azimuth()
        # Add them as vectors
        v1 = np.array([norm1 * cos(az1), norm1 * sin(az1)])
        v2 = np.array([norm2 * cos(az2), norm2 * sin(az2)])
        v3 = v1 - v2
        # Calculate norm and angle of final vector
        norm3 = np.linalg.norm(v3)
        if norm3 == 0:
            (s1, s2) = (0, 0)
        else:
            az3 = arccos(v3[0] / norm3)
            s1 = norm3 * cos(2 * az3)
            s2 = norm3 * sin(2 * az3)
        # Put the new result in M3
        M3 = Stokes(self.name + " - " + other.name)
        M3.from_elements(s0, s1, s2, s3)

        return M3

    def __mul__(self, other):
        """Multiplies vector * number.

        Args:
            other (number): number to multiply

        Returns:
            Stokes: `s3 = number * s1`
        """
        M3 = Stokes()

        if isinstance(other, (int, float, complex)):
            M3.M = self.M * other
        else:
            raise ValueError('other is Not number')
        return M3

    def __rmul__(self, other):
        """Multiplies vector * number.

        Args:
            other (number): number to multiply

        Returns:
            Stokes: `s3 =  s1 * number`
        """
        M3 = Stokes()

        if isinstance(other, (int, float, complex)):
            M3.M = other * self.M

        else:
            raise ValueError('other is Not number')
        return M3

    def __repr__(self):
        M = np.array(self.M).squeeze()
        l_name = "{} = ".format(self.name)
        difference = abs(self.M.round() - self.M).sum()
        if difference > eps:
            l0 = "[{:+3.3f}; {:+3.3f}; {:+3.3f}; {:+3.3f}]\n".format(
                M[0], M[1], M[2], M[3])
        else:
            l0 = "[{:+3.0f}; {:+3.0f}; {:+3.0f}; {:+3.0f}]\n".format(
                M[0], M[1], M[2], M[3])
        return l_name + l0

    def set(self):
        """actualizes self.parameters.M = self.M"""
        # print("inside set")
        self.parameters.M = self.M
        # print(self.parameters.M)

    def get(self):
        """get self.M stokes vector"""
        return self.M

    def check(self):
        """
        verifies that (s0,s1,s2,s3) Stokes vector is properly defined
        verifies that is a 4x1 matrix
        """

        # TODO: do check function
        print("TODO")
        pass

    @_actualize
    def from_elements(self, s0, s1, s2, s3):
        """4x1 Stokes vector [s0, s1, s2, s3]

        Args:
            s0 (float): intensity
            s1 (float): linear 0º-90º polarization
            s2 (float): linear 45º-135º polarization
            s3 (float): circular polarization

        Returns:
            S (4x1 matrix): Stokes vector.
        """

        a = np.matrix(np.zeros((4, 1), dtype=float))
        a[0] = s0
        a[1] = s1
        a[2] = s2
        a[3] = s3

        self.M = a
        return self.M

    @_actualize
    def from_matrix(self, M):
        """Create a Stokes vector from an external matrix.

        Args:
            M (4x1 numpy matrix): New matrix

        Returns:
            np.matrix 4x1 matrix
        """
        self.M = M
        return self.M

    @_actualize
    def from_Jones(self, j, p=1):
        """4x1 Stokes vector from a 2x1 Jones vector

        Args:
            j (Jones_vector object): Jones vector
            p (float or 1x2 float): Degree of polarization, or
                [linear, circular] degrees of polarization.

        Returns:
            S (4x1 matrix): Stokes vector.
        """

        # TODO: me he cargado la circularidad porque daba problemas
        # TODO: Hay que hacerlo en el otro
        p = 1
        if np.size(p) == 1:
            (p1, p2) = (p, p)
        else:
            (p1, p2) = (p[0], p[1])

        E = j.M
        # Calculate the vector
        (Ex, Ey) = (E[0], E[1])
        S = np.zeros([1, 4])
        s0 = abs(Ex)**2 + abs(Ey)**2
        s1 = (abs(Ex)**2 - abs(Ey)**2) * p1
        s2 = 2 * np.real(Ex * np.conj(Ey)) * p1
        s3 = -2 * np.imag(Ex * np.conj(Ey)) * p2

        self.from_elements(s0, s1, s2, s3)

    @_actualize
    def to_Jones(self):
        """Function that converts Stokes light states to Jones states.

        Returns:
            j (Jones_vector object): Stokes state."""
        j = Jones_vector(self.name)
        j.from_Stokes(self)
        return j

    @_actualize
    def general_carac_angles(self,
                             alpha=0,
                             delta=0,
                             intensity=1,
                             pol_degree=1,
                             is_depolarization=False):
        """Function that calculates the Stokes vector of light given by their
        caracteristic angles.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil,
        pp 137.

        Args:
            alpha (float): [0, pi]: tan(alpha) is the ratio between field
                amplitudes of X and Y components.
            delta (float): [0, 2*pi]: phase difference between X and Y field
                components.
            intensity (float): total intensity.
            pol_degree (float): [0, 1]: polarization degree.
            pol (bool): [Default: False] If true, pol_degree is depolarization
                degree instead.

        Returns:
            S (4x1 matrix): Stokes vector.
        """
        # Change depolarization to polarization degree if required
        if is_depolarization:
            pol_degree = 1 - pol_degree
        # Initialize S
        S = np.matrix(np.array([[1.0], [0.0], [0.0], [0.0]]))
        # Calculate the other three parameters
        S[1] = pol_degree * cos(2 * alpha)
        S[2] = pol_degree * sin(2 * alpha) * cos(delta)
        S[3] = pol_degree * sin(2 * alpha) * sin(delta)
        # Normalize by intensity and return
        self.M = intensity * S
        return self.M

    @_actualize
    def general_azimuth_ellipticity(self,
                                    az=0,
                                    el=0,
                                    intensity=1,
                                    pol_degree=1,
                                    is_depolarization=False):
        """Function that calculates the Stokes vector of light given by their
        azimuth and ellipticity.

        From: "Polarized light and the Mueller Matrix approach", J. J. Gil,
        pp 137.

        Args:
            az (float): [0, pi]: azimuth.
            el (float): [-pi/4, pi/4]: ellipticity.
            intensity (float): total intensity.
            pol_degree (float): [0, 1]: polarization degree.
            pol (bool): [Default: False] If true, pol_degree is depolarization
                degree instead.

        Returns:
            S (4x1 matrix): Stokes vector.
        """
        # Change depolarization to polarization degree if required
        if is_depolarization:
            pol_degree = 1 - pol_degree
        # Initialize S
        S = np.matrix(np.array([[1.0], [0.0], [0.0], [0.0]]))
        # Calculate the other three parameters
        S[1] = pol_degree * cos(2 * az) * cos(2 * el)
        S[2] = pol_degree * sin(2 * az) * cos(2 * el)
        S[3] = pol_degree * sin(2 * el)
        # Normalize by intensity and return
        self.M = intensity * S
        return self.M

    @_actualize
    def linear_light(self, angle=0, intensity=1):
        """Stokes 4x1 vector for pure linear polarizer light

        Args:
            angle (float): angle of polarization axis with respect to 0º.
            intensity (float): Intensity of the light

        Returns:
            np.matrix 4x1 Stokes parameters
        """
        self.general_azimuth_ellipticity(
            intensity=intensity, az=angle, el=0, pol_degree=1)
        return self.M

    @_actualize
    def circular_light(self, kind='d', intensity=1):
        """Stokes 4x1 vector for pure circular polarizer light

        Args:
            kind (str): 'd','r' - right, dextro, derecha.
                        'l', 'i' - left, levo, izquierda.
            intensity (float): Intensity of the light

        Returns:
            np.matrix 4x1 Stokes parameters
        """
        # TODO: LM - no funciona esta definción en tests
        if kind in 'dr':  # derecha, right
            self.general_carac_angles(
                alpha=45 * degrees,
                delta=90 * degrees,
                intensity=1,
                pol_degree=1)

        elif kind in 'il':  # izquierda, left
            self.general_carac_angles(
                alpha=-45 * degrees,
                delta=90 * degrees,
                intensity=1,
                pol_degree=1)
        else:
            print("Not d, r, l, i in kind")

    @_actualize
    def elliptical_light(self, a=1, b=1, phase=0, angle=0, pol_degree=1):
        """2x1 Jones vector for polarizer elliptical light

        Args:
            a (float): amplitude of x axis
            b (float): amplitude of y axis
            phase (float): phase shift between axis
            angle (float): rotation_matrix_Jones angle respect to x axis
            pol_degree (float): [0, 1]: polarization degree.

        Returns:
            np.matrix 4x1 matrix
        """
        # Calculate it as Jones vector (easier)
        j = Jones_vector()
        j.elliptical_light(a, b, phase, angle)
        # Transform it to Stokes
        self.from_Jones(j)
        # Depolarize
        self.depolarize(pol_degree)
        return self.M

    @_actualize
    def depolarize(self, p):
        """Function that reduces de polarization degree of a Stokes vector
        homogeneously.

        Returns:
            S (4x1 numpy matrix): Stokes state."""
        S = self.S
        S[1] = S[1] * p
        S[2] = S[2] * p
        S[3] = S[3] * p
        self.from_matrix(S)
        return S

    @_actualize
    def to_Jones(self, p=1):
        """Function that converts Stokes light states to Jones states.

        Args:
            p (float or 1x2 float): Degree of polarization, or
                [linear, circular] degrees of polarization.

        Returns:
            j (Jones_vector object): Stokes state."""
        j = Jones_vector(self.name)
        j.from_Stokes(self)
        return j


# Imports at the end of the script allows cycling import
from .jones_vector import Jones_vector
