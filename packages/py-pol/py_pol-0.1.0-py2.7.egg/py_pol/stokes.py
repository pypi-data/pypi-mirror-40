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

import numpy as np
from numpy import array, cos, matrix, pi, sin, sqrt

from . import eps

degrees = pi / 180.

# TODO: Draw polarization ellipse for point/s (from ellipse_parameters)
# TODO: Draw point/s in poincare' sphere (For one/several stokes parameter)
# TODO: función para luz eliptica (a, b, angulo, polarización)??? No sabía hacer


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
        # TODO: los angulos estan en radianes, pasar a grados. Todo manual
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
        """Stokes beam can be divided in Sp+Su beams, where Sp is fully-polarized
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

        It is 0 for linearly polarized light and 1 for circulary polarized light.

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
            azimuth = 0.5 * np.arctan(s2 / s1)

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
        #TODO: No sería mejor (a,b,angle), hacer otro para dibujar
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
        TODO: Esta mal la suma de vectores

        Args:
            other (Stokes): 2nd Stokes vector to add

        Returns:
            Stokes: `s3 = s1 + s2`
        """

        M3 = Stokes()
        M3.M = self.M + other.M
        M3.parameters.M = M3.M
        M3.name = self.name + " + " + other.name

        return M3

    def __sub__(self, other):
        """Substracts two Stokes vectors.

        Args:
            other (Stokes): 2nd Stokes vector to add

        Returns:
            Stokes: `s3 = s1 - s2`
        """

        M3 = Stokes()
        M3.M = self.M - other.M
        M3.parameters.M = M3.M
        M3.name = self.name + " - " + other.name

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
            l0 = "[{:+3.3f}, {:+3.3f}, {:+3.3f}. {:+3.3f}]\n".format(
                M[0], M[1], M[2], M[3])
        else:
            l0 = "[{:+3.0f}, {:+3.0f}, {:+3.0f}. {:+3.0f}]\n".format(
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
    def custom(self, s0, s1, s2, s3):
        """2x2 Stokes vector [s0, s1, s2, s3]

        Args:
            s0 (float): intensity
            s1 (float): linear 0º-90º polarization
            s2 (float): linear 45º-135º polarization
            s3 (float): circular polarization

        Returns:
            S (4x1 matrix): Stokes vector.
        """

        self.M = np.matrix(np.array([[s0], [s1], [s2], [s3]]))
        self.parameters.M = self.M
        return self.M

    @_actualize
    def general(self,
                alpha=0,
                delta=0,
                intensity=1,
                pol_degree=1,
                carac=True,
                pol=True):
        """Function that calculates the most general diattenuator retarder
        from the parameters.

        TODO: yo haría dos funciones y quitaría carac
        From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 137.

        Args:
            alpha (float): [0, pi]: tan(alpha) is the ratio between amplitudes of
                the eigenstates  in Stokes formalism.
            delta (float): [0, 2*pi]: phase difference between both components of
                the eigenstates in Stokes formalism.
            intensity (float): Total intensity.
            pol_degree (float): [0, 1]: Polarization degree.
            carac (bool): [Default: True] If false, assumes alpha is azimuth and
                delta is elipticity.
            pol (bool): [Default: True] If false, pol_degree is depolarization
                degree instead.

        Returns:
            S (4x1 matrix): Stokes vector.
        """
        # Change depolarization to polarization degree if required
        if not pol:
            pol_degree = 1 - pol_degree
        # Initialize S
        S = np.matrix(np.array([[1.0], [0.0], [0.0], [0.0]]))
        # Calculate the other three parameters
        if carac:
            S[1] = pol_degree * cos(2 * alpha)
            S[2] = pol_degree * sin(2 * alpha) * cos(delta)
            S[3] = pol_degree * sin(2 * alpha) * sin(delta)
        else:
            S[1] = pol_degree * cos(2 * alpha) * cos(2 * delta)
            S[2] = pol_degree * sin(2 * alpha) * cos(2 * delta)
            S[3] = pol_degree * sin(2 * delta)
        # Normalize by intensity and return
        self.M = intensity * S
        self.parameters.M = self.M
        return self.M

    @_actualize
    def polarized_light(self,
                        intensity=1,
                        angle=0,
                        phase=0,
                        pol_degree=1,
                        is_field=False,
                        is_degree=False):
        """Stokes 4x1 vector for utils light beam consrtructed directly from fields:
        $ (I, Q, U, V) = (s0, P*s1, P*s2, P*s3)  = ( <Ex Ex*> + <Ey Ey*>
        <Ex Ex*> - <Ey Ey*>
        <Ex Ey*> + <Ey Ex*>
        i<Ex ux*> + i <Ey Ey*>$

        TODO: Que diferencia hay con general... tiene de todo ésta.

        Args:
            intensity (float): intensity of light
            angle (float): angle of axis with respect to 0º.
            phase (float): phaseshift: 0=linear, pi/2=circular, else=elliptical
            pol_degree (float) [0, 1]: Polarization degree.
            is_field (bool): If True intensity parameter is field parameter.
            is_degree (bool): If True phase is circular polarization degree .

        Returns:
            ndarray: 4x1 Stokes parameters

        """
        # TODO: rehacer

        if is_field:
            intensity = intensity**2

        ax = intensity * cos(angle)
        ay = intensity * sin(angle)

        if not is_degree:
            # TODO: Hay algo raro con los ángulos
            # TODO, mejor 2 funciones?
            S = matrix(
                array([[intensity], [pol_degree * (ax**2 - ay**2)],
                       [2 * pol_degree * ax * ay * cos(phase)],
                       [2 * pol_degree * ax * ay * sin(phase)]]))
        else:
            (pol_degree_lin,
             pol_degree_circ) = (sqrt(pol_degree**2 - phase**2), phase)
            S = matrix(
                array([[intensity], [pol_degree_lin * (ax**2 - ay**2)],
                       [2 * pol_degree_lin * ax * ay],
                       [2 * pol_degree_circ * ax * ay]]))

        self.M = S
        self.parameters.M = S
        return S

    @_actualize
    def linear_light(self, angle=0, intensity=1, is_field=False):
        """Stokes 4x1 vector for pure linear polarizer light

        Args:
            angle (float): angle of polarization axis with respect to 0º.
            intensity (float): Intensity of the light
            is_field (bool): If true, intensity is considered field instead.

        Returns:
            ndarray: 4x1 Stokes parameters

        """

        self.polarized_light(
            intensity=intensity,
            angle=angle,
            phase=0,
            pol_degree=1,
            is_field=is_field)

    @_actualize
    def circular_light(self, kind='d', intensity=1, is_field=False):
        """Stokes 4x1 vector for pure circular polarizer light

        Args:
            kind (str): 'd','r' - right, dextro, derecha.
                        'l', 'i' - left, levo, izquierda.
            intensity (float): Intensity of the light
            is_field (bool): If true, intensity will be considered field instead

        Returns:
            ndarray: 4x1 Stokes parameters

        """

        if kind in 'dr':  # derecha, right
            self.polarized_light(
                intensity=intensity,
                angle=pi / 4,
                phase=pi / 2,
                pol_degree=1,
                is_field=is_field)

        elif kind in 'il':  # izquierda, left
            self.polarized_light(
                intensity=intensity,
                angle=pi / 4,
                phase=-pi / 2,
                pol_degree=1,
                is_field=is_field)
        else:
            print("Not d, r, l, i in kind")
