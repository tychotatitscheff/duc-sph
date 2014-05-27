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
import app.solver.model.hash_table as m_hash

import app.solver.model.vector as m_vec

RADIUS_MULTIPLICATIVE = 3
NUM_WORKER = 25
GROUP_BY_LOW = 12


class BaseSolver():
    """
    Basic class that can be decorated.
    """
    def __init__(self, tt, dt=0.1):
        self.__tt = tt
        self.__t = 0
        self.__dt = dt
        self.__particles = None
        self.__collisions_object = None
        self.__initialized = False

    @property
    def dt(self):
        return self.__dt

    @property
    def particles(self):
        return self.__particles

    def __initialisation(self, l, n):
        raise NotImplementedError

    def __compute_density_and_pressure(self):
        raise NotImplementedError

    def __compute__forces_and_integrate(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class Solver(BaseSolver):
    """
    Solver decorated by the decorator design pattern
    """
    def __init__(self, solver):
        super().__init__(solver.integration_step)
        self.__solver = solver
        self.__particles = solver.particles
        self.__t = solver.__tt
        self.__collision_object = solver.__collision_object
        self.__initialized = solver.__initialized
        self.__integration_step = solver.integration_step
        self.__dt = solver.dt

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, t):
        self.__dt = t


class SphSolver(Solver):
    """

    """
    def create_active_particle(self, location, radius, fluid):
        m_part.ActiveParticle(self.__particles, location, radius, fluid)

    def __initialisation(self, l, n):
        # Initiate acceleration structure
        self.__particles = m_hash.Hash(l, n)
        # Create collision Object
        # TODO : create collision object

    def run(self):
        # Initialize the system if not
        if not self.__initialized:
            # TODO l, n
            l = None
            n = None
            self.__initialisation(l, n)
        while self.__t < self.__tt:
            # Compute density and pressure
            self.__compute_density_and_pressure()
            # Compute forces and integrate
            self.__compute_forces_and_integrate()
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
                    particle.future_acceleration = particle.resultant_force / particle.mass
                    particle.future_speed = particle.current_speed + particle.future_acceleration * self.dt
                    particle.future_location = particle.current_location + particle.future_speed * self.dt
                except Exception as e:
                    print(e)

        executor = concurrent.futures.ProcessPoolExecutor(NUM_WORKER)
        futures = [executor.submit(try_compute_forces_and_integrate, group)
                   for group in h_group.grouper(self.__particles.hash_table.values(), GROUP_BY_LOW)]
        concurrent.futures.wait(futures)

    def __update(self):
        pass


if __name__ == "__main__":
    A = BaseSolver(10)
    B = Solver(A)
    state_equation = {'force': '12 x +4'}
    pass