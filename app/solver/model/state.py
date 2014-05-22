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


class ColourFieldLaplacian(EstimatedState):
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
        colour = 0
        for n in neighbour:
            r = particle.location.value - n.location.value
            colour += self.factor(n) * self.__kernel.laplacian(r)


class SurfaceTensionVector(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val):
        super().__init__(name, val)
        self.__kernel = kern

    @staticmethod
    def factor(neighbour):
        return neighbour.mass / neighbour.rho

    def __call__(self, particle, neighbour):
        n = m_vec.Vector([0, 0, 0])
        for neigh in neighbour:
            r = particle.location.value - neigh.location.value
            n += self.factor(neigh) * self.__kernel.gradient(r)


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

    def factor(self, particle, n):
        pass

    def __call__(self, particle, neighbour):
        #assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        for n in neighbour:
            r = particle.loc.value - neighbour.loc.value
            resultant += self.factor(particle, n) * self.__kernel.gradient(r)
        self.value = resultant
        return resultant


class PressureForce(Force):
    """
    Page 17

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """
    def factor(self, particle, n):
        assert isinstance(particle, m_part.ActiveParticule)
        assert isinstance(n, m_part.ActiveParticule)
        if n is not particle:
            return - particle.density * ((particle.pressure / particle.density ** 2)
                                         + (n.pressure / n.density ** 2)) * n.mass


class ViscosityForce(Force):
    """
    Page 22

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """
    def factor(self, particle, n):
        assert isinstance(particle, m_part.ActiveParticule)
        assert isinstance(n, m_part.ActiveParticule)
        if n is not particle:
            return particle.fluid.mu * (n.speed - particle.speed) * n.mass / n.rho


class SurfaceTension(EstimatedState):
    def __init__(self, name, kern: m_kern.Kernel, val):
        super().__init__(name, val)
        self.__kernel = kern

    def __call__(self, particle, neighbour):
        k = m_kern.DefaultKernel
        tension_vector = SurfaceTensionVector("Surface tension", k, m_vec.Vector([0, 0, 0]))
        force = - particle.fluid.sigma * ColourFieldLaplacian * tension_vector(particle, neighbour) / \
                tension_vector(particle, neighbour).norm()
        return force


class Speed(IntegratedState):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m/s"


class Position(IntegratedState):
    def __init__(self, name,  val):
        """

        """
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m"

if __name__ == "__main__":
    import app.solver.model.fluid as m_fluid
    import app.solver.model.hash_table as m_hash
    kern = m_kern.SpikyKernel(10)
    pt1 = m_vec.Vector([100, 200, 300])
    pt2 = m_vec.Vector([102, 201, 300])
    fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
    hashing = m_hash.Hash(1, 1000)
    A = m_part.ActiveParticule(hashing, pt1, 1, fl)
    B = m_part.ActiveParticule(hashing, pt2, 1, fl)
    t = SurfaceTension("Tension de surface", kern, m_vec.Vector([0, 0, 0]))
    print(t(A, A.neighbour(5, True)))
