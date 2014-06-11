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
import app.solver.model.kernel as s_k
import app.solver.model.vector as s_v


# test default kernel
k1 = s_k.SpikyKernel(10)


class TestDefaultKernel:
    def test_call_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k1()

    def test_call_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k1("a")

    def test_call_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k1(3)

    def test_call_shall_return_float_1(self):
        assert isinstance(k1(s_v.Vector([1, 2, 3])), float)

    def test_call_shall_return_float_2(self):
        assert isinstance(k1(s_v.Vector([10, 20, 30])), float)

    def test_gradient_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k1.gradient()

    def test_gradient_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k1.gradient("a")

    def test_gradient_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k1.gradient(3)

    def test_gradient_shall_return_float_0(self):
        assert isinstance(k1.gradient(s_v.Vector([0, 0, 0])), s_v.Vector)

    def test_gradient_shall_return_float_1(self):
        assert isinstance(k1.gradient(s_v.Vector([1, 2, 3])), s_v.Vector)

    def test_gradient_shall_return_float_2(self):
        assert isinstance(k1.gradient(s_v.Vector([10, 20, 30])), s_v.Vector)

    def test_laplacian_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k1.laplacian()

    def test_laplacian_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k1.laplacian("a")

    def test_laplacian_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k1.laplacian(3)

    def test_laplacian_shall_return_float_1(self):
        assert isinstance(k1.laplacian(s_v.Vector([1, 2, 3])), float)

    def test_laplacian_shall_return_float_2(self):
        assert isinstance(k1.laplacian(s_v.Vector([10, 20, 30])), float)


# test spiky kernel
k2 = s_k.SpikyKernel(10)


class TestSpikyKernel:
    def test_call_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k2()

    def test_call_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k2("a")

    def test_call_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k2(3)

    def test_call_shall_return_float_1(self):
        assert isinstance(k2(s_v.Vector([1, 2, 3])), float)

    def test_call_shall_return_float_2(self):
        assert isinstance(k2(s_v.Vector([10, 20, 30])), float)

    def test_gradient_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k2.gradient()

    def test_gradient_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k2.gradient("a")

    def test_gradient_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k2.gradient(3)

    def test_gradient_shall_return_float_0(self):
        assert isinstance(k2.gradient(s_v.Vector([0, 0, 0])), s_v.Vector)

    def test_gradient_shall_return_float_1(self):
        assert isinstance(k2.gradient(s_v.Vector([1, 2, 3])), s_v.Vector)

    def test_gradient_shall_return_float_2(self):
        assert isinstance(k2.gradient(s_v.Vector([10, 20, 30])), s_v.Vector)

    def test_laplacian_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k2.laplacian()

    def test_laplacian_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k2.laplacian("a")

    def test_laplacian_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k2.laplacian(3)

    def test_laplacian_shall_return_float(self):
        assert isinstance(k1.laplacian(s_v.Vector([1, 2, 3])), float)

    def test_laplacian_shall_return_float_2(self):
        assert isinstance(k1.laplacian(s_v.Vector([10, 20, 30])), float)


# test spiky kernel
k3 = s_k.ViscosityKernel(10)


class TestViscosityKernel:
    def test_call_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k3()

    def test_call_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k3("a")

    def test_call_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k3(3)

    def test_call_shall_return_float_1(self):
        assert isinstance(k3(s_v.Vector([1, 2, 3])), float)

    def test_call_shall_return_float_2(self):
        assert isinstance(k3(s_v.Vector([10, 20, 30])), float)

    def test_gradient_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k3.gradient()

    def test_gradient_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k3.gradient("a")

    def test_gradient_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k2.gradient(3)

    def test_gradient_shall_return_float_0(self):
        assert isinstance(k3.gradient(s_v.Vector([0, 0, 0])), s_v.Vector)

    def test_gradient_shall_return_float_1(self):
        assert isinstance(k3.gradient(s_v.Vector([1, 2, 3])), s_v.Vector)

    def test_gradient_shall_return_float_2(self):
        assert isinstance(k3.gradient(s_v.Vector([10, 20, 30])), s_v.Vector)

    def test_laplacian_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k3.laplacian()

    def test_laplacian_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k3.laplacian("a")

    def test_laplacian_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k3.laplacian(3)

    def test_laplacian_shall_return_float(self):
        assert isinstance(k3.laplacian(s_v.Vector([1, 2, 3])), float)

    def test_laplacian_shall_return_float_2(self):
        assert isinstance(k3.laplacian(s_v.Vector([10, 20, 30])), float)

# test spiky kernel
k4 = s_k.Poly6Kernel(10)


class TestPoly6Kernel:
    def test_call_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k4()

    def test_call_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k4("a")

    def test_call_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k4(3)

    def test_call_shall_return_float_1(self):
        assert isinstance(k4(s_v.Vector([1, 2, 3])), float)

    def test_call_shall_return_float_2(self):
        assert isinstance(k4(s_v.Vector([10, 20, 30])), float)

    def test_gradient_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k4.gradient()

    def test_gradient_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k4.gradient("a")

    def test_gradient_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k4.gradient(3)

    def test_gradient_shall_return_float_1(self):
        assert isinstance(k4.gradient(s_v.Vector([1, 2, 3])), s_v.Vector)

    def test_gradient_shall_return_float_2(self):
        assert isinstance(k4.gradient(s_v.Vector([10, 20, 30])), s_v.Vector)

    def test_laplacian_raise_attribute_error_0(self):
        with pytest.raises(TypeError):
            k4.laplacian()

    def test_laplacian_raise_attribute_error_1(self):
        with pytest.raises(AssertionError):
            k4.laplacian("a")

    def test_laplacian_raise_attribute_error_2(self):
        with pytest.raises(AssertionError):
            k4.laplacian(3)

    def test_laplacian_shall_return_float(self):
        assert isinstance(k4.laplacian(s_v.Vector([1, 2, 3])), float)

    def test_laplacian_shall_return_float_2(self):
        assert isinstance(k4.laplacian(s_v.Vector([10, 20, 30])), float)