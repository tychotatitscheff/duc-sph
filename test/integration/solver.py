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


def create_part_fluid(self):
    base = m_solver.BaseSolver(10, 0.1)
    fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)

    solve = m_solver.SphSolver(base)
    vec = m_vec.Vector([random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)])
    solve.create_active_particle(vec, fl, 0.001)
    print(solve.particles)


class TestCreatePart:

    def test_call_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            create_part_fluid()




'''
kern = m_kern.SpikyKernel(10)
V = ForcePressure("sals", kern, m_vec.Vector([1, 0, 2]))

pt1 = m_vec.Vector([100, 200, 300])
pt2 = m_vec.Vector([102, 201, 300])

hashing = m_hash.Hash(1, 1000)
A = m_part.ActiveParticule(hashing, pt1, 1, fl)
B = m_part.ActiveParticule(hashing, pt2, 1, fl)
t = SurfaceTension("Tension de surface", kern, m_vec.Vector([0, 0, 0]))
print(t(A, A.neighbour(5, True)))'''