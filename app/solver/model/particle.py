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

import app.solver.model.vector as m_vec
import app.solver.model.kernel as m_kern

RAD_MUL = 2
ATMOSPHERIC_PRESSURE = 1
GRAVITY = m_vec.Vector([0, 0, -9.8])

############################################# Definition of the particles ##############################################


class ActiveParticle(object):
    """
    Particle class.
    """
    def __init__(self, hash_particle, location: m_vec, fluid, radius, speed=m_vec.Vector([0, 0, 0]),
                 acceleration=m_vec.Vector([0, 0, 0]), rad_mul=RAD_MUL):
        """
        :type location: point.Point
        :type radius: float
        """
        # Structure
        self.__hash_particle = hash_particle

        # Constant properties
        self.__radius = radius
        self.__fluid = fluid

        # Mass
        self.__mass = 0

        # Density and pressure
        self.__density = Density("rho of " + str(self.__hash__()),
                                 m_kern.DefaultKernel(rad_mul * radius), fluid.rho0)
        self.__pressure = Pressure("P of " + str(self.__hash__()), ATMOSPHERIC_PRESSURE)

        # Forces
        self.__internal_forces = []
        self.__external_forces = []
        self.__resultant_force = m_vec.Vector([0, 0, 0])

        # Integrated properties
        self.__current_location = Position("Current location of " + str(self.__hash__()), location)
        self.__future_location = Position("Future location of " + str(self.__hash__()), location)

        self.__current_speed = Speed("Current speed of" + str(self.__hash__()), speed)
        self.__future_speed = Speed("Future speed of" + str(self.__hash__()), speed)

        self.__current_acceleration = Acceleration("Current acceleration of" + str(self.__hash__()), acceleration)
        self.__future_acceleration = Acceleration("Future acceleration of" + str(self.__hash__()), acceleration)

        # Append particle to acceleration structure
        self.__hash_particle.insert(self)

    def __del__(self):
        """
        Delete particle
        """
        try:
            self.__hash_particle.remove(self)
        except ValueError:
            pass

    ### Acceleration structure

    @property
    def hash_particle(self):
        return self.__hash_particle

    ### Radius and fluid

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, rad):
        assert isinstance(rad, float)
        self.__radius = rad

    @property
    def fluid(self):
        return self.__fluid

    @fluid.setter
    def fluid(self, flu):
        self.__fluid = flu

    @property
    def rho(self):
        return self.__density.value

    @property
    def rho0(self):
        return self.fluid.rho

    ### Mass

    @property
    def mass(self):
        return 4/3 * pi * (self.radius ** 3) * self.fluid.rho0

    @mass.setter
    def mass(self, mass):
        self.__mass = mass

    ### Density and pressure

    @property
    def density(self):
        return self.__density

    @property
    def pressure(self):
        return self.__pressure

    ### Location

    @property
    def current_location(self):
        return self.__current_location

    @current_location.setter
    def current_location(self, loc):
        self.__current_location = loc

    @property
    def future_location(self):
        return self.__future_location

    @future_location.setter
    def future_location(self, loc):
        self.__future_location = loc

    ### Speed

    @property
    def current_speed(self):
        return self.__current_speed

    @current_speed.setter
    def current_speed(self, sp):
        self.__current_speed = sp

    @property
    def future_speed(self):
        return self.__future_speed

    @future_speed.setter
    def future_speed(self, sp):
        self.__future_speed = sp

    ### Acceleration

    @property
    def current_acceleration(self):
        return self.__current_acceleration

    @current_acceleration.setter
    def current_acceleration(self, acc):
        self.__current_acceleration = acc

    @property
    def future_acceleration(self):
        return self.__future_acceleration

    @future_acceleration.setter
    def future_acceleration(self, acc):
        self.__future_acceleration = acc

    ### Forces

    @property
    def external_forces(self):
        return self.__external_forces

    @property
    def internal_forces(self):
        return self.__internal_forces

    @property
    def resultant_force(self):
        return self.__resultant_force

    @resultant_force.setter
    def resultant_force(self, vec):
        assert isinstance(vec, m_vec.Vector)
        self.__resultant_force = vec

    @property
    def forces(self):
        forces = []
        forces.extend(self.external_forces)
        forces.extend(self.external_forces)
        yield forces

    def append_force(self, force, internal=True):
        if internal:
            self.__internal_forces.append(force)
        else:
            self.__external_forces.append(force)

    def delete_force(self, force):
        if force in self.external_forces:
            self.__external_forces.remove(force)
        elif force in self.internal_forces:
            self.__internal_forces.remove(force)
        else:
            raise TypeError

    #### Functions

    def neighbour(self, h, approx=False):
        return self.hash_particle.search(self, h, approx=approx)

    def update(self):
        self.hash_particle.update(self)
        self.current_location = self.future_location

############################################### Definition of the states ###############################################


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


class Density(State):
    def __init__(self, name, kernel: m_kern.Kernel, val):
        assert isinstance(val, float) or isinstance(val, int)
        if isinstance(val, int):
            val = float(val)
        assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kernel
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


class ColourField(State):
    """
    Page 25

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """
    def __init__(self, name, kernel: m_kern.Kernel, val):
        super().__init__(name, val)
        self.__kernel = kernel

    @staticmethod
    def factor(neighbour):
        return neighbour.mass / neighbour.rho

    def __call__(self, particle, neighbour):
        colour = 0
        for n in neighbour:
            r = particle.location.value - n.location.value
            colour += self.factor(n) * self.__kernel.__call__(r)

    def laplacian(self, particle, neighbour):
        colour = 0
        for n in neighbour:
            r = particle.location.value - n.location.value
            colour += self.factor(n) * self.__kernel.laplacian(r)


class SurfaceTensionDirection(State):
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
            n += self.factor(neigh) * self.__kernel.__call__(r)

    def gradient(self, particle, neighbour):
        n = m_vec.Vector([0, 0, 0])
        for neigh in neighbour:
            r = particle.location.value - neigh.location.value
            n += self.factor(neigh) * self.__kernel.gradient(r)


class SurfaceTension(State):
    def __init__(self, name, kern: m_kern.Kernel, val, particle):
        super().__init__(name, val)
        self.__kernel = kern

    def __call__(self, part, neighbour):
        assert isinstance(part, ActiveParticle)
        force = 0
        CF = ColourField("CF", m_kern.Kernel, 0)
        STD = SurfaceTensionDirection("STD", m_kern.Kernel, 0)
        for n in neighbour:
            force = - part.fluid.sigma * CF.laplacian(part, n) * STD.gradient(part, n) / \
                    STD.gradient(part, n).m_vec.Vector.norm(n)
        return force


class Pressure(State):
    def __init__(self, name, val):
        assert isinstance(val, float) or isinstance(val, int)
        super().__init__(name, val)
        self.__unit = "Pa"

    @staticmethod
    def factor(particle: ActiveParticle):
        return particle.density.value * particle.fluid.k

    def __call__(self, particle):
        pressure = self.factor(particle)
        self.value = pressure


class Force(State):
    def __init__(self, name, kernel: m_kern.Kernel, val, kern_type="gradient"):
        assert isinstance(val, m_vec.Vector)
        assert isinstance(kernel, m_kern.Kernel)
        super().__init__(name, val)
        self.__kernel = kernel
        self.__kernel_type = kern_type
        self.__unit = "N"

    def factor(self, particle, n):
        raise NotImplementedError

    def __call__(self, particle, neighbour):
        assert isinstance(particle, ActiveParticle)
        assert isinstance(neighbour, list)
        resultant = m_vec.Vector([0, 0, 0])
        k_type = self.__kernel_type
        if k_type == "gradient":
            w = self.__kernel.gradient
        elif k_type == "laplacian":
            w = self.__kernel.laplacian
        else:
            w = self.__kernel.__call__
        for n in neighbour:
            assert isinstance(neighbour, ActiveParticle)
            r = particle.current_location.value - neighbour.current_location.value
            resultant += self.factor(particle, n) * w(r)
        return resultant


class ForcePressure(Force):
    def factor(self, particle, n):
        assert isinstance(particle, ActiveParticle)
        assert isinstance(n, ActiveParticle)

        mj = n.mass
        rho_j = n.density.value
        rho_i = particle.density.value
        p_j = n.pressure.value
        p_i = particle.pressure.value
        return -mj * rho_i * (p_i / (rho_i ** 2) + p_j / (rho_j ** 2))


class ForceViscosity(Force):
    def factor(self, particle, n):
        assert isinstance(particle, ActiveParticle)
        assert isinstance(n, ActiveParticle)

        u_i = particle.current_speed.value
        u_j = n.current_speed.value
        m_j = n.mass
        rho_i = particle.density.value
        mu = particle.fluid.mu
        return (u_j - u_i) * mu * m_j / rho_i


class ForceGravity(Force):
    def __call__(self, particle, n):
        assert isinstance(particle, ActiveParticle)
        assert isinstance(n, ActiveParticle)
        g = GRAVITY
        rho_i = particle.rho
        return rho_i * g


class Position(State):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m"


class Speed(State):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m/s"


class Acceleration(State):
    def __init__(self, name, val):
        assert isinstance(val, m_vec.Vector)
        super().__init__(name, val)
        self.__unit = "m/s^-2"