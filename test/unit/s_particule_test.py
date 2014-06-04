#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Benoit'
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
import app.solver.model.vector as m_vec
import app.solver.model.fluid as m_fluid
import app.solver.model.hash_table as m_hash
import app.solver.model.particle as s_p

# test de la class ActiveParticle
hash1 = m_hash.Hash(2, 100)
fluid1 = m_fluid.Fluid(1, 1, 1, 1, 1, 1, 1)
p1 = s_p.ActiveParticule(hash1, m_vec.Vector([1, 2, 3]), 6, fluid1)


class TestActiveParticule:
    def test_fluid_raise_attribute_error_0(self):
        with pytest.raises(AssertionError):
            p1.fluid = "a"

    def test_fluid_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            p1.fluid = 3

    def test_radius_raises_attribute_error_0(self):
        with pytest.raises(AssertionError):
            p1.radius = "a"

    def test_mass_shall_return_float_0(self):
        assert isinstance(p1.mass, float)
