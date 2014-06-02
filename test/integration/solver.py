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

hashing = m_hash.Hash(2, 2001)
solve = m_solver.SphSolver(10, 0.1, hashing)
fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
vec = m_vec.Vector([random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)])
solve.create_active_particle(vec, fl, 1.)
print("")


