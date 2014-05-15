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

import app.solver.model.particule as m_part


def decorable(cls):
    cls.__lshift__ = lambda obj, function: function(obj)
    return cls


@decorable
class BaseSolver():
    """
    Basic class that can be decorated.
    """
    def __init__(self, integration_step):
        self.__integration_step = integration_step
        self.__state_equations = dict()
        self.__particules = m_part.list_particules

    @property
    def integration_step(self):
        return self.__integration_step

    @property
    def state_equations(self):
        return self.__state_equations

    @property
    def particules(self):
        return self.__particules

    def integration_method(self):
        pass

    def smoothing_function(self):
        pass

    def run(self):
        pass


class Solver(BaseSolver):
    """
    Solver decorated by the decorator design pattern
    """
    def __init__(self, solver):
        super().__init__(solver.integration_step)
        self.__solver = solver
        self.__list_particules = m_part.list_particules
        self.__integration_step = solver.integration_step
        self.__state_equations = solver.state_equations


class ReplaceIntegrationMethod(Solver):
    def __init__(self, solver, method):
        super().__init__(solver)
        self.integration_function = method


class ReplaceSmoothingMFunction(Solver):
    def __init__(self, solver, method):
        super().__init__(solver)
        self.smoothing_function = method


class ReplaceRun(Solver):
    def __init__(self, solver, method):
        super().__init__(solver)
        self.run = method


class AddStateEquation(Solver):
    def __init__(self, solver, state_equation: dict):
        super().__init__(solver)
        self.retract = None
        for (key, value) in state_equation.items():
            if key not in self.state_equations:
                self.state_equations[key] = value


def add_state_equation(solver, state_equation):
    return AddStateEquation(solver, state_equation)


class DelStateEquation(Solver):
    def __init__(self, solver, state):
        super().__init__(solver)
        self.retract = None
        if state in self.state_equations:
            del self.state_equations[state]


if __name__ == "__main__":
    A = BaseSolver(10)
    B = Solver(A)
    state_equation = {'force': '12 x +4'}
    C = AddStateEquation(B, state_equation)
    D = DelStateEquation(C, 'force')
    print(isinstance(D, Solver))
    E = ReplaceIntegrationMethod(C, lambda x: 2*x)
    print(E.integration_function(2))
    pass