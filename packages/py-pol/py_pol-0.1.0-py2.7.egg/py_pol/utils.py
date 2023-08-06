# !/usr/local/bin/python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Name:        common.py
# Purpose:     Common functions to classes
#
# Author:      Luis Miguel Sanchez Brea
#
# Created:     2017
# Copyright:   AOCG / UCM
# Licence:     GPL
# ----------------------------------------------------------------------
""" Common functions to classes """

import datetime
import multiprocessing
import time
from math import sqrt

import numpy as np
import scipy as sp
from numpy import array, cos, matrix, ones_like, pi, sin, tan, zeros

# Angle limit variables
limAlpha = [0, pi / 2]
limDelta = [0, 2 * pi]
limAz = [0, pi]
limEl = [-pi / 4, pi / 4]
degrees = pi / 180


def rotation_matrix_2(theta=0):
    """2x2 rotation matrix

    Args:
        theta (float): angle of rotation, in radians.

    Returns:
        ndarray: 2x2 matrix
    """

    return matrix(
        array([[cos(theta), sin(theta)], [-sin(theta), cos(theta)]]),
        dtype=float)


def azimuth_elipt_2_carac_angles(az, el):
    """Function that converts azimuth and elipticity to caracteristic angles in
    Jones space.

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 137
    and 1543.

    cos(2*alpha) = cos(2*az) * cos(2*el)
    tan(delta) = tan(2*el) / sin(2*az)

    Args:
        az (float) [0, pi]: Azimuth (angle of rotation).
        el (float) [-pi/4, pi/4]: Elipticity angle.

    Examples:


    Returns:
        alpha (float) [0, pi]: tan(alpha) is the ratio between the maximum amplitudes of the polarization elipse in X-Y coordinates.
        delta (float) [0, 2*pi]: phase difference between both components of
            the eigenstates in Jones formalism.
    """
    # Check that the angles belong to the correct interval. If not, fix it.
    az = put_in_limits(az, "az")
    el = put_in_limits(el, "el")
    # Calculate values using trigonometric functions
    alpha = 0.5 * np.arccos(cos(2 * az) * cos(2 * el))
    # Avoid dividing by 0
    if az == 0:
        delta = np.sign(tan(2 * el)) * pi / 2
    elif az == pi:
        delta = -np.sign(tan(2 * el)) * pi / 2
    else:
        delta = np.arctan(tan(2 * el) / sin(2 * az))
    # Use the other possible value from the arcs functions if necessary
    Qel = which_quad(el)
    Qaz = which_quad(az)
    if Qel == -1:
        if Qaz == 1 or Qaz == 2:
            delta = delta % (2 * pi)
        else:
            delta += pi
    else:
        if Qaz == 3 or Qaz == 4:
            delta += pi
    # Make sure the output values are in the allowed limits
    alpha = put_in_limits(alpha, "alpha")
    delta = put_in_limits(delta, "delta")
    # End
    return alpha, delta


def carac_angles_2_azimuth_elipt(alpha, delta):
    """Function that converts azimuth and elipticity to caracteristic angles in
    Jones space.

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil, pp 137
    and 1543.

    cos(2*alpha) = cos(2*az) * cos(2*el)
    tan(delta) = tan(2*el) / sin(2*az)

    Args:
        alpha (float) [0, pi]: tan(alpha) is the ratio between the maximum
        amplitudes of the polarization elipse in X-Y coordinates.
        delta (float) [0, 2*pi]: phase difference between both components of
            the eigenstates in Jones formalism.

    Output
        az (float) [0, pi]: Azimuth (angle of rotation).
        el (float) [-pi/4, pi/4]: Elipticity angle.
    """
    # Check that the angles belong to the correct interval. If not, fix it.
    alpha = put_in_limits(alpha, "alpha")
    delta = put_in_limits(delta, "delta")
    # Calculate values using trigonometric functions
    az = 0.5 * np.arctan(tan(2 * alpha) * cos(delta))
    el = 0.5 * np.arcsin(sin(2 * alpha) * sin(delta))
    # Use the other possible value from the arcs functions if necessary
    Qalpha = which_quad(alpha)
    Mdelta = which_quad(delta, octant=False)
    if Qalpha == 2:
        az += pi / 2
    else:
        if Mdelta == 2 or Mdelta == 3:
            az += pi
    if Mdelta == 0 and Qalpha == 2.5:
        az += pi
    elif Mdelta == 1.5 or Mdelta == 2.5 or Mdelta == 3.5:
        if Qalpha == 1.5 or Qalpha == 2.5:
            az += pi
    # Check that the outpit values are in the correct interval
    az = put_in_limits(az, "az")
    el = put_in_limits(el, "el")
    # End
    return az, el


def which_quad(angle, octant=True):
    """Auxiliary function to calculate which quadrant or octant angle belongs
    to."""
    if octant:
        if angle == -pi / 4:
            q = -1.5
        elif angle < 0:
            q = -1
        elif angle == 0:
            q = 0
        elif angle < pi / 4:
            q = 1
        elif angle == pi / 4:
            q = 1.5
        elif angle < pi / 2:
            q = 2
        elif angle == pi / 2:
            q = 2.5
        elif angle < 3 / 4 * pi:
            q = 3
        elif angle == 3 / 4 * pi:
            q = 3.5
        elif angle < 2 * pi:
            q = 4
        else:
            q = 4.5
    else:
        if angle == 0:
            q = 0
        elif angle < pi / 2:
            q = 1
        elif angle == pi / 2:
            q = 1.5
        elif angle < pi:
            q = 2
        elif angle == pi:
            q = 2.5
        elif angle < 3 * pi / 2:
            q = 3
        elif angle == 3 / 2 * pi:
            q = 3.5
        else:
            q = 4
    return q


def put_in_limits(x, type):
    """When dealing with polarization elipse coordinates, make sure that they
    are in the valid limits, which are set in the declaration of this class.

    Args:
        x (float): Value
        type (string): Which type of variable is: alpha, delta, az or el.

    Returns:
        y (float): Corresponding angle inside the valid limits.
    """
    # Change x only if necessary
    if type == "alpha" or type == "Alpha":
        if x < limAlpha[0] or x > limAlpha[1]:
            aux = sin(x)
            x = np.arcsin(abs(aux))
    elif type == "delta" or type == "Delta":
        if x < limDelta[0] or x > limDelta[1]:
            x = x % (2 * pi)
    elif type == "az" or type == "Az":
        if x < limAz[0] or x > limAz[1]:
            aux = cos(x)
            x = np.arccos(abs(aux))
    elif type == "el" or type == "El":
        if x < limEl[0] or x > limEl[1]:
            aux = tan(x)
            if aux > 1:
                aux = 1 / aux
            x = np.arctan(abs(aux))
    # Output
    return x


# execute multiprocessing
def execute_multiprocessing(__function_process__,
                            dict_parameters,
                            num_processors,
                            verbose=False):
    """
    executes multiprocessing reading a dictionary
    inputs:
        __function_process__ function tu process, it only accepts a dictionary
        dict_parameters, dictionary / array with parameters
        num_processors, if 1 no multiprocessing is used
        verbose, prints processing time

    output:
        data: reults of multiprocessing
        processing time

    examples of function and dictionary:
        def __function_process__(xd):
            x = xd['x']
            y = xd['y']
            # grt = copy.deepcopy(grating)
            suma = x + y
            return dict(sumas=suma, ij=xd['ij'])

        def creation_dictionary_multiprocessing():
            # create parameters for multiprocessing
            t1 = time.time()
            X = sp.linspace(1, 2, 10)
            Y = sp.linspace(1, 2, 1000)
            dict_parameters = []
            ij = 0
            for i, x in enumerate(X):
                for j, y in enumerate(Y):
                    dict_parameters.append(dict(x=x, y=y, ij=[ij]))
                    ij += 1
            t2 = time.time()
            print "time creation dictionary = {}".format(t2 - t1)
            return dict_parameters
    """
    t1 = time.time()
    if num_processors == 1 or len(dict_parameters) < 2:
        data_pool = [__function_process__(xd) for xd in dict_parameters]
    else:
        pool = multiprocessing.Pool(processes=num_processors)
        data_pool = pool.map(__function_process__, dict_parameters)
        pool.close()
        pool.join()
    t2 = time.time()
    if verbose is True:
        print("num_proc: {}, time={}".format(num_processors, t2 - t1))
    return data_pool, t2 - t1


def create_from_blocks(D, P, m, m00=1):
    """Function that creates a mueller matrix from their block components.

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

    Args:
        D (1x3 or 3x1 float): Diattenuation vector.
        P (1x3 or 3x1 float): Diattenuation vector.
        m (3x3 matrix): Small m matrix.
        m00 (float, default 1): [0, 1] Parameter of average intensity

    Output:
        M (4x4 matrix): Mueller matrix of the diattenuator.
    """
    M = np.matrix(
        np.array([[1, D[0], D[1], D[2]], [P[0], m[0, 0], m[0, 1], m[0, 2]],
                  [P[1], m[1, 0], m[1, 1], m[1, 2]],
                  [P[2], m[2, 0], m[2, 1], m[2, 2]]]))
    return m00 * M


def divide_in_blocks(M):
    """Function that creates a mueller matrix from their block components.

    From: "Polarized light and the Mueller Matrix approach", J. J. Gil.

    Args:
        M (4x4 matrix): Mueller matrix of the diattenuator.

    Output:
        D (1x3 or 3x1 float): Diattenuation vector.
        P (1x3 or 3x1 float): Diattenuation vector.
        m (3x3 matrix): Small m matrix.
        m00 (float, default 1): [0, 1] Parameter of average intensity.
    """
    m00 = M[0, 0]
    M = M / m00
    D = matrix(M[0, 1:4])
    P = matrix(M[1:4, 0])
    m = matrix(M[1:4, 1:4])
    return D, P, m, m00


def _pickle_method(method):
    """
    function for multiprocessing in class
    """
    func_name = method.__func__.__name__
    obj = method.__self__
    cls = method.__self__.__class__
    # deal with mangled names
    if func_name.startswith('__') and not func_name.endswith('__'):
        cls_name = cls.__name__.lstrip('_')
        func_name = '_' + cls_name + func_name
    return _unpickle_method, (func_name, obj, cls)


def _unpickle_method(func_name, obj, cls):
    """
    function for multiprocessing in class
    """
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


def iscolumn(v):
    """Checks if the array v is a column array or not.
    Args:
        v (array): Array to be tested.
    Output:
        cond (bool): True if v is a column array."""
    cond = False
    s = v.shape
    if len(s) == 2:
        if s[0] == 1 and s[1] > 1:
            cond = True
    return cond


def isrow(v):
    """Checks if the array v is a row array or not.
    Args:
        v (array): Array to be tested.
    Output:
        cond (bool): True if v is a row array."""
    cond = False
    s = v.shape
    if len(s) == 1:
        cond = True
    elif len(s) == 2:
        if s[1] == 1:
            cond = True
    return cond


def delta_kron(a, b):
    """Computes the Kronecker delta.
    Args:
        a, b (int): Numbers.
    Output:
        d (int): Result."""

    if a == b:
        d = 1
    else:
        d = 0
    return d


def order_eig(q, m):
    """Function that orders the eigenvalues from max to min, and then orders
    the eigenvectors following the same order.
    Args:
        q (float array): Array of eigenvalues
        m (numpy matrix): Matrix with the eigenvectors as columns
    Output:
        q (float array): Array of ordered eigenvalues
        m (numpy matrix): Matrix with the eigenvectors ordered as columns
        """
    # Find correct order
    order = np.flip(np.argsort(q), 0)
    # Order eigenvalues
    q = np.flip(np.sort(q), 0)
    # Order eigenvectors
    s = m.shape
    m2 = np.zeros(s)
    for ind in range(s[1]):
        ind2 = order[ind]
        m2[:, ind] = np.squeeze(m[:, ind2])
    # Output
    return q, np.matrix(m2)


def check_eig(q, m, M):
    """Function that checks the eigenvalues and eigenvectors."""
    dif = np.zeros(len(q))
    for ind, qi in enumerate(q):
        v = m[:, ind]
        v2 = M * v
        d = v2 - qi * v
        dif[ind] = np.linalg.norm(d)
        print(("The eigenvalue {} has an eigenvector {}.".format(qi, v.T)))
    M2 = m * M * m.T
    d = M2 - M
    dif2 = sqrt(np.sum(np.square(d)))
    dif3 = (abs(d)).max()
    d = m.T - m.I
    dif4 = sqrt(np.sum(np.square(d)))
    print('The eigenvalues are:')
    print(q)
    print('The deviation respect to the eigenvectors is:')
    print(dif)
    print(
        ('The mean square difference in the decomposition is: {}.'.format(dif2)
         ))
    print(('The maximum difference in the decomposition is: {}.'.format(dif3)))
    print(('The matrix of eigenvalues is orthogonal with deviation {}'.format(
        dif4)))
    print(M)
    print(M2)


def date_in_name(filename):
    """introduces a date in the filename
    """
    divided = filename.split(".")
    extension = divided[-1]
    rest = divided[0:-1]
    initial_name = ".".join(rest)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%H_%M_%S_%f")
    filename_2 = "{}_{}.{}".format(initial_name, date, extension)
    return filename_2


def seq(start, stop, step=1):
    n = int(round((stop - start) / float(step)))
    if n > 1:
        return ([start + step * i for i in range(n + 1)])
    else:
        return ([])


def distance(x1, x2):
    """
    calcula la distance entre 2 vectores
    """
    x1 = array(x1)
    x2 = array(x2)
    print(x1.ndim)

    dist2 = 0
    for i in range(x1.ndim):
        dist2 = dist2 + (x1[i] - x2[i])**2

    return sp.sqrt(dist2)


def nearest(vector, numero):
    """calcula la posicion de numero en el vector
        actualmente esta implementado para 1-D, pero habria que hacerlo para nD
        inputs:
        *vector es un array donde estan los points
        *numero es un dato de los points que se quieren compute

        outputs:
        *imenor - orden del elemento
        *value  - value del elemento
        *distance - diferencia entre el value elegido y el incluido
    """
    indexes = np.abs(vector - numero).argmin()
    values = vector.flat[indexes]
    distances = values - numero
    return indexes, values, distances


def nearest2(vector, numero):
    """calcula la posocion de numero en el vector
        actualmente esta implementado para 1-D, pero habria que hacerlo para nD

        inputs:
        *vector es un array donde estan los points
        *numero es un array de los points que se quieren compute

        outputs:
        *imenor - orden del elemento
        *value  - value del elemento
        *distance - diferencia entre el value elegido y el incluido

        mejoras:
        *incluir n-dimensiones
    """
    indexes = np.abs(np.subtract.outer(vector, numero)).argmin(0)
    values = vector[indexes]
    distances = values - numero
    return indexes, values, distances


def ndgrid(*args, **kwargs):
    """n-dimensional gridding like Matlab's NDGRID

        The input *args are an arbitrary number of numerical sequences,
        e.g. lists, arrays, or tuples.
        The i-th dimension of the i-th output argument
        has copies of the i-th input argument.

        Optional keyword argument:
        same_dtype : If False (default), the result is an ndarray.
                     If True, the result is a lists of ndarrays, possibly with
                       different dtype. This can save space if some *args
                       have a smaller dtype than others.

        Typical usage:
        >>> x, y, z = [0, 1], [2, 3, 4], [5, 6, 7, 8]
        >>> X, Y, Z = ndgrid(x, y, z)
        # unpacking the returned ndarray into X, Y, Z

        Each of X, Y, Z has shape [len(v) for v in x, y, z].
        >>> X.shape == Y.shape == Z.shape == (2, 3, 4)
        True
        >>> X
        array([[[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]],
                   [[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1]]])
        >>> Y
        array([[[2, 2, 2, 2],
                        [3, 3, 3, 3],
                        [4, 4, 4, 4]],
                   [[2, 2, 2, 2],
                        [3, 3, 3, 3],
                        [4, 4, 4, 4]]])
        >>> Z
        array([[[5, 6, 7, 8],
                        [5, 6, 7, 8],
                        [5, 6, 7, 8]],
                   [[5, 6, 7, 8],
                        [5, 6, 7, 8],
                        [5, 6, 7, 8]]])

        With an unpacked argument list:
        >>> V = [[0, 1], [2, 3, 4]]
        >>> ndgrid(*V) # an array of two arrays with shape (2, 3)
        array([[[0, 0, 0],
                        [1, 1, 1]],
                   [[2, 3, 4],
                        [2, 3, 4]]])

        For input vectors of different data kinds,
        same_dtype=False makes ndgrid()
        return a list of arrays with the respective dtype.
        >>> ndgrid([0, 1], [1.0, 1.1, 1.2], same_dtype=False)
        [array([[0, 0, 0], [1, 1, 1]]),
         array([[ 1. ,  1.1,  1.2], [ 1. ,  1.1,  1.2]])]

        Default is to return a single array.
        >>> ndgrid([0, 1], [1.0, 1.1, 1.2])
        array([[[ 0. ,  0. ,  0. ], [ 1. ,  1. ,  1. ]],
                   [[ 1. ,  1.1,  1.2], [ 1. ,  1.1,  1.2]]])
        """
    same_dtype = kwargs.get("same_dtype", True)
    V = [array(v) for v in args]  # ensure all input vectors are arrays
    shape = [len(v) for v in args]  # common shape of the outputs
    result = []
    for i, v in enumerate(V):
        # reshape v so it can broadcast to the common shape
        # http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html
        zero = zeros(shape, dtype=v.dtype)
        thisshape = ones_like(shape)
        thisshape[i] = shape[i]
        result.append(zero + v.reshape(thisshape))
    if same_dtype:
        return array(result)  # converts to a common dtype
    else:
        return result  # keeps separate dtype for each output


def save_mat(filename, nombresVariables, variables):
    """guarda un archivo MAT con los data"""
    import scipy.io

    mdict = {}

    for nombre, variable in zip(nombresVariables, variables):
        mdict[nombre] = variable

    scipy.io.savemat(filename, mdict)


def load_mat(filename):
    import scipy.io
    data = scipy.io.loadmat(filename)

    #     for (nombre,value) in data.items():
    #         print nombre
    #         print value
    #         exec(nombre+'='+u(value).encode('utf-8')) o algo así

    return data
