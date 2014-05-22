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

RAD_MUL = 2

from abc import ABCMeta, abstractmethod

from math import *

import app.solver.model.vector as m_vec
import app.solver.model.fluid as m_fluid
import app.solver.model.kernel as m_kern
"import app.solver.model.state as m_state"

import app.solver.model.hash_table as m_hash

import pytest


dict_type_particule = {}

def_fluid = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)

ATMOSPHERIC_PRESSURE = 1
GRAVITY = 9.8


class _MetaParticule(ABCMeta):
    """
    Inherit from type since its a metaclass.
    Write in list_particule each time a new type of particule is created.
    """

    def __init__(cls, nom, bases, dic):
        type.__init__(cls, nom, bases, dic)
        dict_type_particule[nom] = cls


class _Particule(metaclass=_MetaParticule):
    """
    Generic abstract particule class.
    """
    @abstractmethod
    def __init__(self, hash_particule, location: m_vec, radius: float=1., rad_mul=RAD_MUL):
        """
        :type location: point.Point
        :type radius: float
        """
        self.__density = m_state.Density("rho of " + str(self.__hash__()), m_kern.DefaultKernel(rad_mul * radius), 1)
        self.__location = m_state.Position("Current location of " + str(self.__hash__()), location)
        self.__future_location = m_state.Position("Next location of " + str(self.__hash__()), location)
        self.__radius = radius
        self.__speed = m_state.Speed("Speed of" + str(self.__hash__()), m_vec.Vector([0, 0, 0]))

        self.__forces = []
        self.__force_res = m_vec.Vector([0, 0, 0])
        self.__hash_particule = hash_particule
        self.__hash_particule.insert(self)

    def __del__(self):
        try:
            self.__hash_particule.remove(self)
        except ValueError:
            pass

    def update(self):
        self.__hash_particule.update(self)
        self.location = self.future_location

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, loc):
        self.__location = loc

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, sp):
        self.__speed = sp

    @property
    def future_location(self):
        return self.__future_location

    @future_location.setter
    def future_location(self, loc):
        self.__future_location = loc

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, rad):
        assert isinstance(rad, float)
        self.__radius = rad

    """@property
    def states(self):
        return self.__forces

    def append_force(self, state: m_state.State):
        assert isinstance(state, m_state.State)
        self.__forces.append(state)

    def delete_state(self, state: m_state.State):
        assert isinstance(state, m_state.State)
        try:
            self.__forces.remove(state)
        except ValueError:
            pass"""

    def neighbour(self, h, approx=False):
        return self.__hash_particule.search(self, h, approx=approx)


class ActiveParticule(_Particule):
    def __init__(self, hash_particule, location, radius, fluid=def_fluid):
        """
        :type fluid: fluid.Fluid
        """
        super().__init__(hash_particule, location, radius)
        self.__fluid = fluid
        self.__density = m_state.Density("rho of " + str(self.__hash__()),
                                         m_kern.Poly6Kernel(RAD_MUL * radius), fluid.rho0)
        self.__pressure = m_state.Pressure("P of " + str(self.__hash__()), ATMOSPHERIC_PRESSURE)
        self.__mass = 0
        self.__velocity = 0

    def __del__(self):
        super().__del__()

    @property
    def fluid(self):
        return self.__fluid

    @fluid.setter
    def fluid(self, flu):
        self.__fluid = flu

    @property
    def density(self):
        return self.__density

    @property
    def pressure(self):
        return self.__pressure

    @property
    def mass(self):
        return 4/3 * pi * (self.radius ** 3) * self.fluid.rho0

    @mass.setter
    def mass(self, masse):
        self.__mass = masse

    @property
    def rho(self):
        return self.__density.value

    @property
    def rho0(self):
        return self.fluid.rho

    @property
    def velocity(self):
        return self.__velocity


class GhostParticule(_Particule):
    def __init__(self, hash_particule, location, radius):
        super().__init__(hash_particule, location, radius)

    def __del__(self):
        super().__del__()


if __name__ == "__main__":
    print("")
    pt1 = m_vec.Vector([100, 200, 300])
    pt2 = m_vec.Vector([102, 201, 300])
    fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
    hashing = m_hash.Hash(1, 1000)
    A = ActiveParticule(hashing, pt1, 2., fl)
    B = GhostParticule(hashing, pt1, 2.)
    C = ActiveParticule(hashing, pt2, 2., fl)
    kern = m_kern.SpikyKernel(4)
    st = m_state.Force("F_viscosity", kern, m_vec.Vector([0, 0, 0]))


    B.__del__()

    neig = A.neighbour(5)
    print(A.neighbour(5))

    with pytest.raises(TypeError):
        C = _Particule()