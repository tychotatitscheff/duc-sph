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
import app.solver.model.particle as m_part


fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
solve = m_solver.SphSolver(10, 0.1)
solve.initialisation(2, 100)

def create_part_fluid():

    vec = m_vec.Vector([random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)])
    print(vec)

    solve.create_active_particle(vec, fl, 0.001)
    for key, value in solve.particles.hash_table.items():
        for part in value:
            assert isinstance(part, m_part.ActiveParticle)
            print(part.density.value, part.current_location.value)


if __name__ == "__main__":
    create_part_fluid()

    for key, value in solve.particles.hash_table.items():
        for part in value:
            assert isinstance(part, m_part.ActiveParticle)
            print(part.density.value, part.current_location.value)
    pass
print("yy")