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
        if isinstance(val, int):
            val = float(val)
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


class ColorField(EstimatedState):
    """
    Page 25

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """
    def __init__(self, name, kern: m_kern.Kernel, val):
        super().__init__(name, val)
        self.__kernel = kern

    @staticmethod
    def factor(neighbour):
        return neighbour.mass / neighbour.rho

    def __call__(self, particle, neighbour):
        color = 0
        for n in neighbour:
            r = particle.location.value - n.location.value
            color += self.factor(n) * self.__kernel.__call__(r)


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


class Force(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val):
        assert isinstance(val, m_vec.Vector)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kern
        self.__unit = "N"
        self.__type = "general"

    def factor(self, particle, n):
        return 1

    def __call__(self, particle, neighbour):
        #assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        if type == "PressureForce":
            for n in neighbour:
                r = particle.loc.value - neighbour.loc.value
                resultant += self.factor(particle, n) * self.__kernel.gradient(r)

        elif type == "Viscosity force":
            ui = particle.velocity
            for n in neighbour:
                r = particle.loc.value - neighbour.loc.value
                uj = n.velocity
                resultant += self.factor(n, particle) * (uj - ui) * self.__kernel.laplacian(r)
        self.value = resultant

        return resultant


class ForcePressure(Force):
    type = "PressureForce"

    def factor(self, particle, n):
        assert isinstance(particle, m_part.ActiveParticule)
        assert isinstance(n, m_part.ActiveParticule)

        mj = n.mass
        rhoj = n.density
        rhoi = particle.density
        pj = n.pressure
        pi = particle.pressure
        return -mj * rhoi * (pi / (rhoi * rhoi) + pj / (rhoj ** 2))


class ForceViscosity(Force):
    type = "ViscosityForce"

    def factor(self, particle, n):
        mj = n.mass
        rhoj = n.density
        mu = particle.fluid.mu
        return mu * mj / rhoj


class ForceGravity(Force):
    type = "Gravity"
    

class Speed(IntegratedState):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m/s"
        

class Position(IntegratedState):
    def __init__(self, name, val):
        """

        """
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m"

if __name__ == "__main__":
    kern = m_kern.SpikyKernel(10)
    V = ForceViscosity("sals", kern, m_vec.Vector([1, 0, 2]))
    print("toto")
