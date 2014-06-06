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
import app.solver.model.particle as m_part
import app.solver.model.solver as m_solver
import random
import pytest

hashing = m_hash.Hash(3, 1000)
solve = m_solver.SphSolver(10, 0.1, hashing)
fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
# random_vec = lambda: m_vec.Vector([random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)])
# list_vec = [random_vec() for i in range(0, 1000)]
# for vec in list_vec:
#     solve.create_active_particle(vec, fl, 1.)
random.seed()
particle = m_part.ActiveParticle(hashing, m_vec.Vector([0, 0, 0]), fl, 1.)
solve.initial_volume(particle, "non oriented cube", "CFC", size=10, speed="random")
particle.__del__()
solve.run()
print("")


