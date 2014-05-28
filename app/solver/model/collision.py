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
import math


class CollisionObject(object):
    def __init__(self, cr):
        self.__cr = cr

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
    def __init__(self, cr, is_containing=True):
        super().__init__(cr)
        self.__is_containing = is_containing

    def __implicit_function(self, x):
        assert isinstance(x, m_vec.Vector)
        return 0

    def __detect(self, x):
        is_c = self.__is_containing
        f_neg = (self.__implicit_function(x) < 0)
        return (is_c and f_neg) or (not is_c and not f_neg)


class Sphere(ImplicitPrimitive):
    def __init__(self, cr, c, r, is_containing=True):
        """

        :param cr:
        :param c:
        :param r:
        :param is_containing:
        """
        super().__init__(cr, is_containing)
        self.__c = c
        self.__r = r

    def __implicit_function(self, x):
        c = self.__c
        r = self.__r
        return (x - c) ** 2 - r ** 2

    def react(self, particle, dt):
        assert isinstance(particle, m_part.ActiveParticle)
        x = particle.future_location.value
        u = particle.future_speed.value
        c = self.__c
        r = self.__r
        f = self.__implicit_function(x)

        if self.__detect(x):
            cp = c + r * (x - c) / (x - c).norm()
            d = math.fabs((x - c).norm() - r)
            n_cp = math.copysign(1, f) * (x - c) / (c - x).norm()

            self.__reaction(particle, cp, d, n_cp, dt)


class Box(ImplicitPrimitive):
    def __implicit_function(self, **kwargs):
        pass


