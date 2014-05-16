#!/usr/bin/env python
# -*- coding: utf-8 -*-
from IPython.core.pylabtools import select_figure_format

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

import app.solver.helper.grouper as h_group
import app.solver.model.particule as m_part
import app.solver.model.hash_table as m_hash

import concurrent.futures

RADIUS_MULTIPLICATIVE = 3
NUM_WORKER = 25
GROUP_BY_LOW = 12

def decorable(cls):
    cls.__lshift__ = lambda obj, function: function(obj)
    return cls


@decorable
class BaseSolver():
    """
    Basic class that can be decorated.
    """
    def __init__(self, tt, dt=0.1):
        self.__tt = tt
        self.__t = 0
        self.__dt = dt
        self.__particules = None
        self.__collision_object = None
        self.__initialized = False

    @property
    def dt(self):
        return self.__dt

    @property
    def particules(self):
        return self.__particules

    def __initialisation(self, l, n):
        raise NotImplementedError

    def __compute_density_and_pressure(self):
        raise NotImplementedError

    def __compute_internal_force(self):
        raise NotImplementedError

    def __compute_external_force(self):
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
        self.__particules = solver.particules
        self.__t = solver.__tt
        self.__collision_object = solver.__collision_object
        self.__initialized = solver.__initialized
        self.__integration_step = solver.integration_step
        self.__dt = solver.dt


class SphSolver(Solver):
    """

    """
    def create_active_particle(self, location, radius, fluid):
        m_part.ActiveParticule(self.__particules, location, radius, fluid)

    def __initialisation(self, l, n):
        # Initiate acceleration structure
        self.__particules = m_hash.Hash(l, n)
        # Create collision Object
        # TODO : create collision object

    def run(self):
        # Initialize the system if not
        if not self.__initialized:
            l = None
            n = None
            self.__initialisation(l, n)
        while self.__t < self.__tt:
            # Compute density and pressure
            self.__compute_density_and_pressure()
            # Compute internal force
            self.__compute_internal_force()
            # Compute external force
            self.__compute_external_force()
            # Determine acceleration

            # Integrate speed

            # Integrate location

            #End loop
            self.__t += self.dt

    def __compute_density_and_pressure(self):
        """
        http://stackoverflow.com/questions/15143837/how-to-multi-thread-an-operation-within-a-loop-in-python
        """
        def try_compute_density(items):
            for item in items:
                try:
                    assert isinstance(item, m_part.ActiveParticule)
                    neigh = item.neighbour(RADIUS_MULTIPLICATIVE * item.radius)
                    item.density.__call__(item, neigh)
                    item.pressure.__call__(item)
                except Exception as e:
                    print(e)
        executor = concurrent.futures.ProcessPoolExecutor(NUM_WORKER)
        futures = [executor.submit(try_compute_density, group)
                   for group in h_group.grouper(self.__particules.hash_table.values(), GROUP_BY_LOW)]
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    A = BaseSolver(10)
    B = Solver(A)
    state_equation = {'force': '12 x +4'}
    pass