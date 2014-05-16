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


class ODE(object):
    """
    We want solve this kind of ODE : a * x'' + b * x' + c * x = d

    Programming of Differential Equations
    (Appendix E)
    Hans Petter Langtangen
    Simula Research Laboratory
    University of Oslo, Dept. of Informatics
    """
    def __init__(self, a, b, c, d):
        # Constant Terms
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d

    def __call__(self, u: list):
        return [u[1], - self.__b * u[1] / self.__a - self.__c * u[0] / self.__a]
