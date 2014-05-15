#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Clément Eberhardt," \
             "Clément Léost," \
             "Benoit Picq," \
             "Théo Subtil" \
             "and Tycho Tatitscheff"
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

from abc import ABCMeta, abstractmethod

from app.solver.model import point, fluid, state, vector

import pytest

dict_type_particule = {}
list_particules = []
def_fluid = fluid.Fluid(0)


class _MetaParticule(ABCMeta):
    """
    Inherit from type since its a metaclass.
    Write in list_particule each time a new type of particule is created.
    """

    def __init__(cls, nom, bases, dic):
        type.__init__(cls, nom, bases, dic)
        dict_type_particule[nom] = cls


class _Particule(metaclass=_MetaParticule):
    """
    Generic abstract particule class.
    """
    @abstractmethod
    def __init__(self, location: point.Point, radius: float=1.):
        """
        :type location: point.Point
        :type radius: float
        """
        self.__location = location
        self.__radius = radius

        self.__force = state.Force(vector.Vector([0, 0, 0]))

        list_particules.append(self)

    def __del__(self):
        try:
            list_particules.remove(self)
        except ValueError:
            pass

    @property
    def loc(self):
        return self.__location

    @loc.setter
    def loc(self, loc):
        assert isinstance(loc, point.Point)
        self.__location = loc

    @property
    def rad(self):
        return self.__radius

    @rad.setter
    def rad(self, rad):
        assert isinstance(rad, float)
        self.__radius = rad


class ActiveParticule(_Particule):
    def __init__(self, location, radius, _fluid=def_fluid):
        """
        :type _fluid: fluid.Fluid
        """
        super().__init__(location, radius)
        self.__fluid = _fluid

    def __del__(self):
        super().__del__()

    @property
    def fluid(self):
        return self.__fluid

    @fluid.setter
    def fluid(self, flu):
        assert isinstance(flu, fluid.Fluid)
        self.__fluid = flu


class GhostParticule(_Particule):
    def __init__(self, loc: point.Point):
        super().__init__(loc)

    def __del__(self):
        super().__del__()


if __name__ == "__main__":
    pt = point.Point(1, 2, 3)
    fl = fluid.Fluid(1)
    A = ActiveParticule(pt, 2., fl)
    B = GhostParticule(pt)
    print(list_particules)
    print(A.loc)
    A.loc = 4
    B.__del__()
    print(list_particules)

    with pytest.raises(TypeError):
        C = _Particule()