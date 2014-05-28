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

import pytest
import app.solver.model.hash_table as s_h
import app.solver.model.particle as s_p
import app.solver.model.fluid as s_f
import app.solver.model.vector as m_vec

h1 = s_h.Hash(76, 212)
f1 = s_f.Fluid(1, 1, 1, 1, 1, 1, 1)
p = s_p.ActiveParticle(h1, [3, 3, 3], f1, 1, m_vec.Vector(1, 1, 1), m_vec.Vector([0, 0, 1]), 5)


class TestHash:    def test_compute_r_chap_return_float_(self):

        assert isinstance(h1.compute_r_chap(p, future=False), int)

    def test_compute_r_chap_raise_attribute_error(self):
        with pytest.raises(AssertionError):
            h1.compute_r_chap("a")

