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

from app.solver.model import vector, kernel


class State(object):
    """
    This class defines a state (force, temp).
    """
    def __init__(self, val):
        self.__value = val


class Force(State):
    def __init__(self, val, kern):
        assert isinstance(val, vector.Vector)
        assert isinstance(kernel, kernel.Kernel)
        super().__init__(val)
        self.__kernel = kern

    def __call__(self, neighboor):
        for n in neighboor:
            pass




if __name__ == "__main__":
    k = kernel.Kernel
    A = Force(vector.Vector([10, 11, 13]), k)
    A("test")
    A.__call__("test")
    pass

