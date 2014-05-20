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
import app.solver.model.kernel as m_kern
import app.solver.model.particule as m_part


class State(object):
    """
    This class defines a state (force, temp).
    """

    def __init__(self, name, val):
        self.__value = val
        self.__name = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


class EstimatedState(State):
    pass


class IntegratedState(State):
    pass


class Density(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val):
        assert isinstance(val, float) or isinstance(val, int)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kern
        self.__unit = "kg / m^3"

    @staticmethod
    def factor(neighbour):
        return neighbour.mass

    def __call__(self, particle, neighbour):
        density = 0
        for n in neighbour:
            r = particle.location.value - n.location.value
            density += self.factor(n) * self.__kernel.__call__(r)
        self.value = density


class Pressure(EstimatedState):
    def __init__(self, name, val):
        assert isinstance(val, float) or isinstance(val, int)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__unit = "Pa"

    @staticmethod
    def factor(particle: m_part.ActiveParticule):
        return particle.density.value * particle.fluid.k

    def __call__(self, particle):
        pressure = self.factor(particle)
        self.value = pressure


class ForcePre(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val):
        assert isinstance(val, m_vec.Vector)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kern
        self.__unit = "N"

    @staticmethod
    def factor(neighbour, particle: m_part.ActiveParticule):
        mj = neighbour.mass
        rhoj = neighbour.density
        rhoi = particle.density
        pj = neighbour.pressure
        pi = particle.pressure
        return -mj * rhoi * (pi / (rhoi * rhoi) + pj / (rhoj * rhoj))

    def __call__(self, particle, neighbour):
        #assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        for n in neighbour:
            r = particle.loc.value - neighbour.loc.value
            forcepre += self.factor(n, particle) * self.__kernel.gradient(r)
            pass


class ForceVis(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val):
        assert isinstance(val, m_vec.Vector)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kern
        self.__unit = "N"

    @staticmethod
    def factor(neighbour, particle: m_part.ActiveParticule):
        mj = neighbour.mass
        rhoj = neighbour.density
        mu = particle.fluid.mu
        return mu * mj / rhoj

    def __call__(self, particle, neighbour):
        #assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        ui = particle.velocity
        for n in neighbour:
            uj = neighbour.velocity
            r = particle.loc.value - neighbour.loc.value
            forcevis += self.factor(n, particle) * (uj - ui) * self.__kernel.laplacian(r)
            pass


class FExter(EstimatedState):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__unit = "N"
        "à completer"


class FGravity(EstimatedState):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__unit = "N"

    def __call__(self, particle):
        #assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        fgravity = particle.density * gravity


class Position(IntegratedState):
    def __init__(self, name, val):
        """

        """
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m"


if __name__ == "__main__":
    ker = m_kern.Kernel(10)
    A = Force("Fg", ker, m_vec.Vector([10, 11, 13]))
    A("test")
    B = State("test", 10)
    A.__call__("test")
    pass

