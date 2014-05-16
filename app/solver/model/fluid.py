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


from math import *

class Fluid(object):
    """
    This class represent one kind of fluid.
    """
    def __init__(self, rho0, b, mu, sigma, l, k, cr):
        self.__rho0 = rho0  # Rest density
        self.__b = b  # Buoyancy diffusion
        self._mu = mu  # Viscosity
        self.__sigma = sigma  # Surface tension
        self.__l = l  # Threshold for normal computation in surface tension computation
        self.__k = k  # Gas stiffness
        self.__cr = cr
        self.__x = floor(self.__rho0 / self.__l ** 2)

    @property
    def rho0(self):
        return self.__rho0

    @property
    def k(self):
        return self.__k
