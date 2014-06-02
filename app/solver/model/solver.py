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

import app.solver.helper.grouper as h_group
import app.solver.model.particle as m_part
import app.solver.model.collision as m_col

import app.solver.model.kernel as m_kern
import app.solver.model.hash_table as m_hash

import app.solver.model.vector as m_vec

RADIUS_MULTIPLICATIVE = 3
NUM_WORKER = 25
GROUP_BY_LOW = 12


class SphSolver():
    def __init__(self, tt, dt, hashing):
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
        self.__collisions_objects = []

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
        act_part = m_part.ActiveParticle(self.particles, location, fluid, radius)
        if fluid_type == "liquid":
            vec_null = m_vec.Vector([0, 0, 0])

            k_d = m_kern.DefaultKernel(radius * 3)
            k_v = m_kern.ViscosityKernel(radius * 3)

            f_p = m_part.ForcePressure("Pressure", k_d, vec_null)
            act_part.append_force(f_p)

            f_v = m_part.ForceViscosity("Viscosity", k_v, vec_null)
            act_part.append_force(f_v)

    def run(self):
        # Initialize the system if not
        while self.__t < self.__tt:
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
        """
        http://stackoverflow.com/questions/15143837/how-to-multi-thread-an-operation-within-a-loop-in-python
        """
        def try_compute_density(items):
            for item in items:
                try:
                    assert isinstance(item, m_part.ActiveParticle)
                    neigh = item.neighbour(RADIUS_MULTIPLICATIVE * item.radius)
                    item.density.__call__(item, neigh)
                    item.pressure.__call__(item)
                except Exception as e:
                    print(e)

        executor = concurrent.futures.ProcessPoolExecutor(NUM_WORKER)
        futures = [executor.submit(try_compute_density, group)
                   for group in h_group.grouper(self.__particles.hash_table.values(), GROUP_BY_LOW)]
        concurrent.futures.wait(futures)

    def __compute_forces_and_integrate(self):
        def try_compute_forces_and_integrate(items):
            for particle in items:
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
                    print(e)

        executor = concurrent.futures.ProcessPoolExecutor(NUM_WORKER)
        futures = [executor.submit(try_compute_forces_and_integrate, group)
                   for group in h_group.grouper(self.__particles.hash_table.values(), GROUP_BY_LOW)]
        concurrent.futures.wait(futures)

    def __check_for_collision(self):
        def try_check_for_collision(items):
            for particle in items:
                try:
                    assert isinstance(particle, m_part.ActiveParticle)
                    for coll_obj in self.collisions_objects:
                        assert isinstance(coll_obj, m_col.CollisionObject)
                        coll_obj.react(particle.future_location, self.dt)
                except Exception as e:
                    print(e)

        executor = concurrent.futures.ProcessPoolExecutor(NUM_WORKER)
        futures = [executor.submit(try_check_for_collision, group)
                   for group in h_group.grouper(self.__particles.hash_table.values(), GROUP_BY_LOW)]
        concurrent.futures.wait(futures)

    def __update(self):
        def try_compute_forces_and_integrate(items):
            for particle in items:
                try:
                    assert isinstance(particle, m_part.ActiveParticle)
                    particle.resultant_force = m_vec.Vector([0, 0, 0])
                    particle.current_speed.value = particle.future_speed.value
                    particle.current_location.value = particle.current_location.value
                except Exception as e:
                    print(e)
        executor = concurrent.futures.ProcessPoolExecutor(NUM_WORKER)
        futures = [executor.submit(try_compute_forces_and_integrate, group)
                   for group in h_group.grouper(self.__particles.hash_table.values(), GROUP_BY_LOW)]
        concurrent.futures.wait(futures)

