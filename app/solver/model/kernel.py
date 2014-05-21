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

from math import *

import app.solver.model.vector as m_vec


class Kernel(object):
    """
    Base Class for Kernel
    """
    def __init__(self, h):
        self.__h = h  # max radius

    @property
    def h(self):
        return self.__h

    def __call__(self, r):
        raise NotImplementedError

    def gradient(self, r):
        raise NotImplementedError

    def laplacian(self, r):
        raise NotImplementedError


class DefaultKernel(Kernel):
    """
    Page 16

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """
    def __call__(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return 315/(64 * pi * h ** 9) * (h ** 2 - r.norm() ** 2) ** 3
        else:
            return 0

    def gradient(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return -945/(32 * pi * h ** 9) * r * (h ** 2 - r.norm() ** 2) ** 2
        else:
            return 0

    def laplacian(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return -945/(32 * pi * h ** 9) * (h ** 2 - r.norm() ** 2) * (3 * h **2 - 7 * r.norm() ** 2)
        else:
            return 0


class SpikyKernel(Kernel):
    """
    Page 20

    M. Desbrun and M.-P. Cani. “Smoothed Particles: A new paradigm for animating highly deformable bodies”.
    In Computer Animation and Simulation ’96, pp. 61–76, 1996.

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """
    def __call__(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return 15. * ((h - r.norm()) ** 3) / (pi * (h ** 6))
        else:
            return 0

    def gradient(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return - 45. * r * ((h - r.norm()) ** 2) / (pi * r.norm() * (h ** 6))
        else:
            return 0

    def laplacian(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return - 90. * ((h - r.norm())) * ((h - 2 * r.norm())) / (pi * r.norm() * (h ** 6))
        else:
            return 0


class ViscosityKernel(Kernel):
    """
    Page 22

    M. Müller, D. Charypar, and M. Gross. “Particle-Based Fluid Simulation for Interactive Applications”.
    Proceedings of 2003 ACM SIGGRAPH Symposium on Computer Animation, pp. 154-159, 2003.
    """

    def __call__(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return 15 / (2 * pi * h ** 3) * (- r.norm() ** 3 / (2 * h ** 3) + r.norm() ** 2 / (h ** 2) + h / (2 * r.norm()) - 1)
        else:
            return 0

    def gradient(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm() <= h:
            return 15 / (2 * pi * h ** 3) * r * (- 3 * r.norm() / (2 * h ** 3) + 2 / (h ** 2) - h / (2 * r.norm() ** 3))
        else:
            return 0

    def laplacian(self, r):
        assert isinstance(r, m_vec.Vector)
        h = self.h
        if r.norm <= h:
            return 45 / (pi * h ** 6) * (h - r.norm())
        else:
            return 0


if __name__ == "__main__":
    A = SpikyKernel(10.)
    B = ViscosityKernel(1)
    a = m_vec.Vector([1, 2, 5])
    print(a)
    print(a.norm)


    print(B(m_vec.Vector([1., 2., 3.])))
    print(B.gradient(m_vec.Vector([1., 2., 3.])))
    print(A.laplacian(m_vec.Vector([1., 2., 3.])))
