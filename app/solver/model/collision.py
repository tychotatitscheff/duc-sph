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
import math


class CollisionObject(object):
    def __init__(self, cr):
        self.__cr = cr

    def __detect(self, x):
        pass

    def __react(self, x):
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

    def __react(self, x):
        c = self.__c
        r = self.__r
        f = self.__implicit_function(x)

        if self.__detect(x):
            contact_point = c + r * (x - c) / (x - c).norm()
            penetration_length = math.fabs((x - c).norm() - r)
            surface_normal_at_contact = math.copysign(1, f) * (x - c) / (c - x).norm()
        else:
            contact_point, penetration_length, surface_normal_at_contact = None

        return contact_point, penetration_length, surface_normal_at_contact


class Box(ImplicitPrimitive):
    def __implicit_function(self, **kwargs):
        pass


