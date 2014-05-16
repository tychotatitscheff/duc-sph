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


import app.solver.model.vector as m_vec
import app.solver.model.fluid as m_fluid
import app.solver.model.kernel as m_kern
import app.solver.model.state as m_state

import app.solver.model.hash_table as m_hash

import pytest

dict_type_particule = {}
hash_particule = m_hash.Hash(3, 20)
def_fluid = m_fluid.Fluid(0)


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
    def __init__(self, location: m_vec, radius: float=1.):
        """
        :type location: point.Point
        :type radius: float
        """
        self.__density = m_state.Density("rho of " + str(self.__hash__()), m_kern.DefaultKernel(RAD_MUL * radius), 1)
        self.__location = m_state.Position("Location of " + str(self.__hash__()), location)
        self.__future_location = m_state.Position("Old location of " + str(self.__hash__()), location)
        self.__radius = radius

        self.__forces = []
        self.__force_res = m_vec.Vector([0, 0, 0])

        hash_particule.insert(self)

    def __del__(self):
        try:
            hash_particule.remove(self)
        except ValueError:
            pass

    def update(self):
        hash_particule.update(self)
        self.location = self.future_location

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, loc):
        self.__location = loc

    @property
    def future_location(self):
        return self.__future_location

    @future_location.setter
    def future_location(self, loc):
        self.__future_location = loc

    @property
    def rad(self):
        return self.__radius

    @rad.setter
    def rad(self, rad):
        assert isinstance(rad, float)
        self.__radius = rad

    @property
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
            pass

    def neighbour(self, h, approx=False):
        return hash_particule.search(self, h, approx=approx)


class ActiveParticule(_Particule):
    def __init__(self, location, radius, fluid=def_fluid):
        """
        :type fluid: fluid.Fluid
        """
        super().__init__(location, radius)
        self.__fluid = fluid
        self.__density = m_state.Density("rho of " + str(self.__hash__()),
                                         m_kern.DefaultKernel(RAD_MUL * radius), fluid.rho0)

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
    def rho(self):
        return self.__density.value

    @property
    def rho0(self):
        return self.fluid.rho


class GhostParticule(_Particule):
    def __init__(self, location):
        super().__init__(location)

    def __del__(self):
        super().__del__()


if __name__ == "__main__":
    print("")
    pt1 = m_vec.Vector([100, 200, 300])
    pt2 = m_vec.Vector([102, 201, 300])
    fl = m_fluid.Fluid(1)
    A = ActiveParticule(pt1, 2., fl)
    B = GhostParticule(pt1)
    C = ActiveParticule(pt2, 2., fl)
    kern = m_kern.SpikyKernel(4)
    st = m_state.Force("F_viscosity", kern, m_vec.Vector([0, 0, 0]))
    print(hash_particule.hash_table)
    B.__del__()
    print(hash_particule.hash_table)
    neig = A.neighbour(5)
    print(A.neighbour(5))

    with pytest.raises(TypeError):
        C = _Particule()