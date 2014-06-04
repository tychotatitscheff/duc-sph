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

import concurrent.futures

import math
import numpy as np

import app.solver.helper.grouper as h_group
import app.solver.model.particle as m_part
import app.solver.model.collision as m_col

import app.solver.model.kernel as m_kern
import app.solver.model.hash_table as m_hash

import app.solver.model.vector as m_vec

from app.solver.conf import *


class SphSolver():
    def __init__(self, tt, dt, hashing, collisions_objects=None):
        """

        :param tt: total times
        :param dt: interval / step
        :type tt: float
        :type dt: float
        """
        self.__tt = tt
        self.__t = 0
        self.__dt = dt
        self.__particles = hashing
        self.__collisions_objects = [] if collisions_objects is None else collisions_objects

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, t):
        self.__dt = t


    @property
    def tt(self):
        return self.__tt

    @property
    def collisions_objects(self):
        return self.__collisions_objects

    @property
    def particles(self):
        return self.__particles

    def create_active_particle(self, location, fluid, radius, fluid_type="liquid", gravity=True):
        """

        :param location: location of the particle
        :param radius: h
        :param fluid: type of the particle
        :type location: vector (m_vec)
        :type radius: float
        :type fluid: fluid
        """

        act_part = m_part.ActiveParticle(self.particles, location, fluid, radius)
        h = str(hash(act_part))
        vec_null = m_vec.Vector([0, 0, 0])

        k_d = m_kern.DefaultKernel(radius * 3)
        k_v = m_kern.ViscosityKernel(radius * 3)
        k_s = m_kern.SpikyKernel(radius * 3)

        if fluid_type == "liquid" or fluid_type == "gaz":
            d = m_part.Density("Density of " + h, k_s, fluid.rho0)

            p = m_part.Pressure("Pressure of " + h, m_part.ATMOSPHERIC_PRESSURE)

            f_p = m_part.ForcePressure("Pressure force of " + h, k_d, vec_null)
            f_v = m_part.ForceViscosity("Viscosity force of " + h, k_v, vec_null)

            f_s = m_part.ForceSurfaceTension("Surface tension force of " + h, k_d, vec_null)

            act_part.density = d
            act_part.pressure = p

            act_part.append_force(f_p)
            act_part.append_force(f_v)
            act_part.append_force(f_s)

        if gravity:
            f_g = m_part.ForceGravity("Gravity force of " + h, k_d, m_vec.Vector([0, 0, -9.8]))
            act_part.append_force(f_g, internal=False)
        return act_part

    def run(self):
        # Initialize the system if not
        while self.__t < self.__tt:
            print(self.__t)
            # Compute density and pressure
            self.__compute_density_and_pressure()
            # Compute forces and integrate
            self.__compute_forces_and_integrate()
            #Check for collision

            #Update
            self.__update()
            #End loop
            self.__t += self.dt

    def __compute_density_and_pressure(self):
        def try_compute_density(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        neigh = particle.neighbour(RADIUS_MULTIPLICATIVE * particle.radius)
                        particle.density.__call__(particle, neigh)
                        particle.pressure.__call__(particle)
                    except Exception as e:
                        print("Density computation : " + str(e))
        hashing = self.particles.hash_table.values()
        try_compute_density(hashing)

    def __compute_forces_and_integrate(self):
        def try_compute_forces_and_integrate(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        neigh = particle.neighbour(RADIUS_MULTIPLICATIVE * particle.radius)
                        particle.resultant_force = m_vec.Vector([0, 0, 0])
                        for force in particle.forces:
                            assert isinstance(force, m_part.Force)
                            force.__call__(particle, neigh)
                            particle.resultant_force += force.value
                        particle.future_acceleration.value = particle.resultant_force * 1. / particle.mass
                        particle.future_speed = particle.current_speed.value + particle.future_acceleration.value * self.dt
                        particle.future_location = particle.current_location.value + particle.future_speed.value * self.dt
                    except Exception as e:
                        print("Force computations and integration : " + str(e))
            hashing = self.particles.hash_table.values()
            try_compute_forces_and_integrate(hashing)

    def __check_for_collision(self):
        def try_check_for_collision(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        for coll_obj in self.collisions_objects:
                            assert isinstance(coll_obj, m_col.CollisionObject)
                            coll_obj.react(particle.future_location, self.dt)
                    except Exception as e:
                        print(e)
        hashing = self.particles.hash_table.values()
        try_check_for_collision(hashing)

    def __update(self):
        def try_update(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        particle.resultant_force = m_vec.Vector([0, 0, 0])
                        particle.current_speed.value = particle.future_speed.value
                        particle.current_location.value = particle.current_location.value
                    except Exception as e:
                        print(e)
        hashing = self.particles.hash_table.values()
        try_update(hashing)

    def initial_volume(self, primitive, particle, **kwargs):
        assert isinstance(particle, m_part.ActiveParticle)
        r = particle.radius
        if primitive == "non oriented cube":
            # c = kwargs['centre']
            # assert isinstance(c, m_vec.Vector)
            s = kwargs['size']
            assert isinstance(s, float)
            part_list = []
            for dim1 in np.arange(1, int(s), 2 * math.sqrt(2) * r):
                for dim2 in np.arange(1, int(s), 2 * math.sqrt(2) * r):
                    for dim3 in np.arange(1, int(s), 2 * math.sqrt(2) * r):
                        part_list.append(m_vec.Vector([r * dim1, r * dim2, r * dim3]))
            for element in part_list:
                self.create_active_particle(element, m_flu.Fluid, particle.radius)

    def generative_surface(self, length, width, normal, particle, speed):
        assert isinstance(normal, m_vec.Vector)
        assert isinstance(particle, m_part.ActiveParticle)
        assert isinstance(speed, m_vec.Vector)
        r = particle.radius
        part_list = []
        for dim1 in np.arange(1, int(length), 2 * math.sqrt(2) * r):
            for dim2 in np.arange(1, int(width), 2 * math.sqrt(2) * r):
                part_list.append(m_vec.Vector([dim1, dim2, 0]))
        for element in part_list:
            p = self.create_active_particle(element, m_flu.Fluid, particle.radius)
            p.current_speed(speed)


if __name__ == "__main__":
    A = SphSolver(100, 1, 0.1)
    H = m_hash.Hash(2, 2000)
    import app.solver.model.fluid as m_flu
    flu = m_flu.Fluid(1000, 1, 0.05, 0.00005, 1, 10, 2)
    part1 = m_part.ActiveParticle(H, m_vec.Vector([0, 0, 0]), flu, 1)
    print(A.initial_volume("non oriented cube", part1, size=20.))
