#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Clément Eberhardt," \
             "Clément Léost," \
             "Benoit Picq," \
             "Théo Subtil" \
             " and Tycho Tatitscheff"
__copyright__ = "Copyright 2014, DucSph"
__credits__ = ["Clément Eberhardt",
               "Clément Léost",
               "Benoit Picq",
               "Théo Subtil",
               "Tycho Tatitscheff"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Tycho Tatitscheff"
__email__ = "tycho.tatitscheff@ensam.eu"
__status__ = "Production"


'''
Freely based on the following

Simple class for 3D vectors.
Requires: Python 2.5 and numpy 1.0.4

(c) Ilan Schnell, 2008
'''

import math

import numpy

numpy.set_printoptions(precision=2)

_TINY = 1e-15


def _xyz_to_012(c):
    if c in 'xyz':
        return ord(c) - ord('x')
    else:
        raise AttributeError("vec3 instance has no attribute '%s'" % c)


def _args_to_tuple(name, args):
    n_arg = len(args)
    if n_arg == 0:
        data = 3 * (0,)
    elif n_arg == 1:
        data = args[0]
        if len(data) != 3:
            raise TypeError('vec3.%s() takes sequence with 3 elements '
                            '(%d given),\n\t   when 1 argument is given' %
                            (name, len(data)))
    elif n_arg == 3:
        data = args
    else:
        raise TypeError('vec3.%s() takes 0, 1 or 3 arguments (%d given)' %
                        (name, n_arg))
    assert len(data) == 3
    try:
        return tuple(map(float, data))
    except (TypeError, ValueError):
        raise TypeError("vec3.%s() can't convert elements to float" % name)


class Vector(numpy.ndarray):
    def __new__(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], Vector):
                return args[0].copy()
            if isinstance(args[0], numpy.matrix):
                return Vector(args[0].flatten().tolist()[0])
        data = _args_to_tuple('__new__', args)
        arr = numpy.array(data, dtype=numpy.float, copy=True)
        return numpy.ndarray.__new__(cls, shape=(3,), buffer=arr)

    def __repr__(self):
        decimal = 5
        return "v[" + str(round(self[0], decimal)) + ", " +\
               str(round(self[0], decimal)) + ", " + str(round(self[0], decimal)) + "]"

    def __mul__(self, other):
        return numpy.dot(self, other)

    def __abs__(self):
        return math.sqrt(self * self)

    def __pow__(self, x):
        return (self * self) if x == 2 else pow(abs(self), x)

    def __eq__(self, other):
        return abs(self - other) < _TINY

    def __ne__(self, other):
        return not self == other

    def __getattr__(self, name):
        return self[_xyz_to_012(name)]

    def __setattr__(self, name, val):
        self[_xyz_to_012(name)] = val

    def norm(self):
        return math.sqrt(self ** 2)

    def a_max(self):
        return numpy.amax(self)

    def get_spherical(self):
        r = abs(self)
        if r < _TINY:
            theta = phi = 0.0
        else:
            x, y, z = self
            theta = math.acos(z / r)
            phi = math.atan2(y, x)

        return r, theta, phi

    def set_spherical(self, *args):
        r, theta, phi = _args_to_tuple('set_spherical', args)
        self[0] = r * math.sin(theta) * math.cos(phi)
        self[1] = r * math.sin(theta) * math.sin(phi)
        self[2] = r * math.cos(theta)

    def get_cylindrical(self):
        x, y, z = self
        rho = math.sqrt(x * x + y * y)
        phi = math.atan2(y, x)
        return rho, phi, z

    def set_cylindrical(self, *args):
        rho, phi, z = _args_to_tuple('set_cylindrical', args)
        self[0] = rho * math.cos(phi)
        self[1] = rho * math.sin(phi)
        self[2] = z


def cross(a, b):
    return Vector(numpy.cross(a, b))


def dot(a, b):
    return numpy.dot(a, b)


if __name__ == "__main__":
    A = Vector([0, 1, 3])
    B = Vector([2, 1, -4])
    C = Vector([2, 1, -4])

    print(A + B)
    print(A - B)

    print(cross(A, B))
    print(dot(A, B))

    print(A ** 2)
    print(A.norm())
    print(numpy.linalg.norm(A))

    print(A == B)
    print(C == B)

    print(A.get_spherical())
    print(A.get_cylindrical())