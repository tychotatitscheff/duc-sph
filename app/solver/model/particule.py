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
import app.solver.model.hash as m_hash

import pytest

dict_type_particule = {}
hash_particule = m_hash.Hash(2, 800)
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
        self.__new_location = m_state.Position("Old location of " + str(self.__hash__()), location)
        self.__radius = radius

        self.__forces = []
        self.__force_res = m_vec.Vector([0, 0, 0])

        hash_particule.insert(self)

    def __del__(self):
        try:
            hash_particule.remove(self)
        except ValueError:
            pass

    def __repr__(self):
        return "Particule " + str(self.location.value)

    def update(self):
        hash_particule.update(self)
        self.location = self.__new_location

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, loc):
        self.__location = loc

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

    def neighbour(self):
        return hash_particule.search(self, 2.5 * self.rad, approx=False)


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
    pt = m_vec.Vector([1, 2, 3])
    fl = m_fluid.Fluid(1)
    A = ActiveParticule(pt, 2., fl)
    B = GhostParticule(pt)
    kern = m_kern.SpikyKernel(4)
    st = m_state.Force("F_viscosity", kern, m_vec.Vector([0, 0, 0]))
    print(list_particules)
    print(A.loc)
    A.loc = 4
    B.__del__()
    print(list_particules)

    with pytest.raises(TypeError):
        C = _Particule()