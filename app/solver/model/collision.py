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

import app.solver.model.vector as m_vec
import app.solver.model.particle as m_part
import numpy as np

import math
import functools


class CollisionObject(object):
    def __init__(self, cr_co=1):
        self.__cr_co = cr_co

    def __detect(self, x):
        pass

    @staticmethod
    def __reaction(particle, cp, d, n_cp, dt):
        u = particle.future_speed.value
        cr = particle.fluid.cr

        u -= (1 + cr * d / (dt * u.norm)) * m_vec.dot(u, n_cp) * n_cp

        particle.future_location.value = cp
        particle.future_speed.value = u

    def react(self, particle, dt):
        pass


class ImplicitPrimitive(CollisionObject):
    def __init__(self, cr_co=1, is_containing=True):
        super().__init__(cr_co)
        self.__is_containing = is_containing

    def __implicit_function(self, x):
        assert isinstance(x, m_vec.Vector)
        return 0

    def __detect(self, x):
        is_c = self.__is_containing
        f_neg = (self.__implicit_function(x) < 0)
        return (is_c and f_neg) or (not is_c and not f_neg)


class Sphere(ImplicitPrimitive):
    def __init__(self, center, radius, cr_co=1, is_containing=True):
        super().__init__(cr_co, is_containing)
        self.__center = center
        self.__radius = radius

    def __implicit_function(self, x):
        c = self.__center
        r = self.__radius
        return (x - c) ** 2 - r ** 2

    def react(self, particle, dt):
        assert isinstance(particle, m_part.ActiveParticle)
        x = particle.future_location.value
        u = particle.future_speed.value
        c = self.__center
        r = self.__radius
        f = self.__implicit_function(x)

        if self.__detect(x):
            cp = c + r * (x - c) / (x - c).norm()
            d = math.fabs((x - c).norm() - r)
            n_cp = math.copysign(1, f) * (x - c) / (c - x).norm()

            self.__reaction(particle, cp, d, n_cp, dt)


class Box(ImplicitPrimitive):
    def __init__(self, c, a, e, cr_co=1):
        assert isinstance(e, m_vec.Vector)
        assert isinstance(a, m_vec.Vector)
        super().__init__(cr_co)
        self.__center = c
        self.__axis = a
        self.__axis_extends = e
        self.__rotation = self.__rotation_matrix()
        self.__rotation_t = np.transpose(self.__rotation)

    def __rotation_matrix(self):
        """http://afni.nimh.nih.gov/pub/dist/src/pkundu/meica.libs/nibabel/eulerangles.py"""
        # TODO : débuger cette zamerde

        x = math.radians(self.__axis[0]) if self.__axis[0] != 0 else None
        y = math.radians(self.__axis[1]) if self.__axis[1] != 0 else None
        z = math.radians(self.__axis[2]) if self.__axis[2] != 0 else None

        m_s = []

        if z:
            cos_z = math.cos(z)
            sin_z = math.sin(z)
            m_s.append(np.array(
                [[cos_z, -sin_z, 0],
                 [sin_z, cos_z, 0],
                 [0, 0, 1]]))
        if y:
            cos_y = math.cos(y)
            sin_y = math.sin(y)
            m_s.append(np.array(
                [[cos_y, 0, sin_y],
                 [0, 1, 0],
                 [-sin_y, 0, cos_y]]))
        if x:
            cos_x = math.cos(x)
            sin_x = math.sin(x)
            m_s.append(np.array(
                [[1, 0, 0],
                 [0, cos_x, -sin_x],
                 [0, sin_x, cos_x]]))
        if m_s:
            return functools.reduce(np.dot, m_s[::-1])
        else:
            return np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def __x_local(self, i):
        # TODO : débuger cette zamerde
        r_t = self.__rotation_t
        c = self.__center
        return np.dot(r_t, (i - c))

    def implicit_function(self, x):
        ext = self.__axis_extends
        x_loc = self.__x_local(x)
        return (m_vec.Vector(np.abs(x_loc)) - ext).a_max()

    def react(self, particle, dt):
        pass


if __name__ == '__main__':
    center = m_vec.Vector([0, 1, 0])
    axis = m_vec.Vector([0, 0, 0])
    extend = m_vec.Vector([5, 4, 3])
    box = Box(center, axis, extend)
    print(box.implicit_function(m_vec.Vector([3, 2, 1])))
