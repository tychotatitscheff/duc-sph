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


# Following decorator is freely adapted from "Apprenez à programmer en python" from  'Vincent Le Golf' book
def check_type_of_args(*spec_args, **spec_kwargs):
    """
    We wait as parameters for this decorator function the types
        that the function should have.
    The function could be call with an undetermined number argument,
        that's why the use of unnamed *args and named **kwargs
    """
    def decorator(called_function):
        """
        Our decorator. It should return modified function.
        """
        def modified_function(*args, **kwargs):
            """
            Our modified function. It verifies the type of arguments.
            """

            # The number of args should be the same as specified
            if len(spec_args) > len(args):
                raise TypeError("Their is not enough args.")
            elif len(spec_args) < len(args):
                raise TypeError("Their is too much args.")

            # Check the type of unnamed args
            for i, arg in enumerate(args):
                if not isinstance(args[i], spec_args[i]):
                    raise TypeError("Unnamed argument {0} is not type {1}".format(i, spec_args[i]))

            # Check the type of named args
            for cle in kwargs:
                if cle not in spec_kwargs:
                    raise TypeError("Named argument {} as no specified type".format(repr(cle)))
                if not isinstance(kwargs[cle], spec_kwargs[cle]):
                    raise TypeError("Argument {0} is not type {1}".format(repr(cle), spec_args[cle]))

            return called_function(*args, **kwargs)
        return modified_function
    return decorator