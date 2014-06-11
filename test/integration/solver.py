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

import cProfile
import io
from pstats import Stats

import numpy as np

hashing = m_hash.Hash(3, 1000)
solve = m_solver.SphSolver(10, 0.1, hashing)
fl = m_fluid.Fluid(993.29, 0, 3.5, .0728, 7.065, 3, 0.02)
# random_vec = lambda: m_vec.Vector([random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)])
# list_vec = [random_vec() for i in range(0, 1000)]
# for vec in list_vec:
#     solve.create_active_particle(vec, fl, 1.)
random.seed()
particle = m_part.ActiveParticle(hashing, m_vec.Vector([0, 0, 0]), fl, 1.)
pr1 = cProfile.Profile()
pr1.enable()
# solve.initial_volume(particle, "non oriented cube", "CFC", size=30, speed="random")
solve.initial_volume(particle, "non oriented cube", "CFC", size=4)
pr1.disable()
particle.__del__()

# array = solve.step()
# import app.plot.generate_images as p_gen
#
# I = p_gen.Image(array)
# I.generate()

pr2 = cProfile.Profile()
pr2.enable()
while solve.t < solve.tt:
    solve.step()
    solve.t += solve.dt
pr2.disable()

s1 = io.StringIO()
s2 = io.StringIO()
sort_by = 'cumtime'

ps1 = Stats(pr1, stream=s1).sort_stats(sort_by)
ps1.print_stats()
print(s1.getvalue())

ps2 = Stats(pr2, stream=s2).sort_stats(sort_by)
ps2.print_stats()
print(s2.getvalue())


