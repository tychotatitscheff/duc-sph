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

import app.solver.model.fluid as m_fluid
import app.solver.model.hash_table as m_hash
import app.solver.model.vector as m_vec
import app.solver.model.kernel as m_kern
import app.solver.model.solver as m_solver
import random
import pytest


def create_part_fluid():
    fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)

    solve = m_solver.SphSolver(10, 0.1)
    vec = m_vec.Vector([random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)])
    solve.initialisation(2, 100)
    solve.create_active_particle(vec, fl, 0.001)
    print(solve.particles)

if __name__ == "__main__":
    create_part_fluid()
    pass
