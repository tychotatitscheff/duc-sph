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

import numpy


class ODESolver:
    def __init__(self, f, dt, u0):
        self.f = f
        self.dt = dt
        self.u = u0

    def step(self):
        raise NotImplementedError


class ForwardEuler(ODESolver):
    def step(self):
        u, dt, f = self.u, self.dt, self.f
        u_new = u + dt * f(u)
        return u_new