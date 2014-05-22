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
    def factor(particle: m_part.ActiveParticule, isotherm):
        if isotherm:
            return (particle.density.value - particle.fluid.rho0) * particle.fluid.k
        else:
            # P = nRT / V
            pass

    def __call__(self, particle, isotherm=True):

            pressure = self.factor(particle, isotherm)
            self.value = pressure


class Force(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val, kern_type="gradient"):
        assert isinstance(val, m_vec.Vector)
        #assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kern
        self.__kernel_type = kern_type
        self.__unit = "N"

    def factor(self, particle, n):
        raise NotImplementedError

    def __call__(self, particle, neighbour):
        #assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        k_type = self.__kernel_type
        if k_type == "gradient":
            w = self.__kernel.gradient
        elif k_type == "laplacian":
            w = self.__kernel.laplacian
        else:
            w = self.__call__
        for n in neighbour:
            r = particle.loc.value - neighbour.loc.value
            resultant += self.factor(particle, n) * w(r)

        return resultant


class ForcePressure(Force):
    type = "PressureForce"

    def factor(self, particle, n):
        assert isinstance(particle, m_part.ActiveParticule)
        assert isinstance(n, m_part.ActiveParticule)

        mj = n.mass
        rho_j = n.density
        rho_i = particle.density
        pj = n.pressure
        pi = particle.pressure
        return -mj * rho_i * (pi / (rho_i ** 2) + pj / (rho_j ** 2))


class ForceViscosity(Force):
    type = "ViscosityForce"

    def factor(self, particle, n):
        u_i = particle.velocity
        u_j = n.velocity
        m_j = n.mass
        rho_i = particle.density
        mu = particle.fluid.mu
        return (u_j - u_i) * mu * m_j / rho_i


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
    V = ForcePressure("sals", kern, m_vec.Vector([1, 0, 2]))

    print("toto")
