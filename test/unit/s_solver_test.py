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

import app.solver.model.particle as m_part
import app.solver.model.solver as m_solver
import app.solver.model.hash_table as m_hash

import app.solver.model.fluid as m_fluid
import app.solver.model.vector as m_vec

hashing = m_hash.Hash(5, 200)
solve = m_solver.SphSolver(10, 0.1, hashing)

fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
particle = m_part.ActiveParticle(hashing, m_vec.Vector([0, 0, 0]), fl, 1.)

a = solve.initial_volume(particle, "non oriented cube", "CC", size=10)
print(a)