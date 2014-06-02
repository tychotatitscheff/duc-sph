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

import app.solver.helper.grouper as h_group
import app.solver.model.particle as m_part
import app.solver.model.collision as m_col
import app.solver.model.hash_table as m_hash
import app.solver.model.vector as m_vec

RADIUS_MULTIPLICATIVE = 3
NUM_WORKER = 25
GROUP_BY_LOW = 12


class SphSolver():
    def __init__(self, tt, dt):
        self.__tt = tt
        self.__t = 0
        self.__dt = dt
        self.__particles = None
        self.__collisions_objects = []
        self.__initialized = False

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

    @property
    def initialized(self):
        return self.__initialized

    @initialized.setter
    def initialized(self, val):
        self.__initialized = val

    def create_active_particle(self, location, radius, fluid):
        m_part.ActiveParticle(self.particles, location, radius, fluid)

    def initialisation(self, l, n):
        # Initiate acceleration structure
        self.__particles = m_hash.Hash(l, n)
        # Append collision Object

    def run(self):
        # Initialize the system if not
        if not self.__initialized:
            # TODO l, n
            l = 3
            n = 100
            self.initialisation(l, n)
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
                    for coll_obj in self.collision_objects:
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

    def initial_volume(self, primitive, particle, **kwargs):
        assert isinstance(particle, m_part.ActiveParticle)
        r = particle.radius
        if primitive == "non oriented cube":
            # c = kwargs['centre']
            # assert isinstance(c, m_vec.Vector)
            s = kwargs['size']
            assert isinstance(s, float)
            partlist = []
            dim1 = 0
            dim2 = 0
            dim3 = 0
            while dim1 < s:
                if :
                    partlist.append([dim1, r, r])
                while dim2 < s:
                    if [r, dim2, r] in partlist is False:
                        partlist.append([r, dim2, r])
                    while dim3 < s:
                        if [r, r, dim3] in partlist is False:
                            partlist.append([r, r, dim3])
                        dim3 += 1
                        if dim3 > s:
                            break
                    dim2 += 1
                    if dim2 > s:
                        break
                dim1 += 1
                if dim1 > s:
                    break
            return partlist

if __name__ == "__main__":
    A = SphSolver(100, 1)
    H = m_hash.Hash(2, 2000)
    import app.solver.model.fluid as m_flu
    flu = m_flu.Fluid(1000, 1, 0.05, 0.00005, 1, 10, 2)
    part1 = m_part.ActiveParticle(H, m_vec.Vector([0, 0, 0]), flu, 1)
    print(A.initial_volume("non oriented cube", part1, size=4.))