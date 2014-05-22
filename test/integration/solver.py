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

kern = m_kern.SpikyKernel(10)
V = ForcePressure("sals", kern, m_vec.Vector([1, 0, 2]))

pt1 = m_vec.Vector([100, 200, 300])
pt2 = m_vec.Vector([102, 201, 300])
fl = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
hashing = m_hash.Hash(1, 1000)
A = m_part.ActiveParticule(hashing, pt1, 1, fl)
B = m_part.ActiveParticule(hashing, pt2, 1, fl)
t = SurfaceTension("Tension de surface", kern, m_vec.Vector([0, 0, 0]))
print(t(A, A.neighbour(5, True)))