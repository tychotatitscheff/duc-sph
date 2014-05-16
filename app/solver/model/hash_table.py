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

from collections import defaultdict
from math import *

import app.solver.helper.prime as m_pr
import app.solver.model.vector as m_vec
#import app.solver.model.particule as m_part


class Hash():
    def __init__(self, l, n, p1=73856093, p2=19349663, p3=83492791):
        """
        l : cell size
        n : number of particle
        """
        self.__l = l
        self.__n = n
        self.__n_h = next(m_pr.primes_above(2 * n))

        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3

        self.__hash_table = defaultdict(list)

    @property
    def hash_table(self):
        return self.__hash_table

    def insert(self, _object):
        r_chap = self.compute_r_chap(_object)
        h = self.compute_hash(r_chap)
        self.__hash_table[h].append(_object)

    def remove(self, _object):
        r_chap = self.compute_r_chap(_object)
        h = self.compute_hash(r_chap)
        self.__hash_table[h].remove(_object)

    def update(self, _object):
        r_chap_old = self.compute_r_chap(_object)
        r_chap_new = self.compute_r_chap(_object, future=True)

        h_old = self.compute_hash(r_chap_old)
        h_new = self.compute_hash(r_chap_new)

        self.__hash_table[h_old].remove(_object)
        self.__hash_table[h_new].append(_object)

    def compute_r_chap(self, _object, future=False):
        l = self.__l

        if not future:
            r_x = _object.location.value[0]
            r_y = _object.location.value[1]
            r_z = _object.location.value[2]
        else:
            r_x = _object.future_location.value[0]
            r_y = _object.location.value[1]
            r_z = _object.location.value[2]

        r_chap = m_vec.Vector([floor(r_x / l), floor(r_y / l), floor(r_z / l)])

        return r_chap

    def compute_hash(self, r_chap):
        n_h = self.__n_h
        p1 = self.__p1
        p2 = self.__p2
        p3 = self.__p3

        ap = int(r_chap[0]*p1)
        bp = int(r_chap[1]*p2)
        cp = int(r_chap[2]*p3)

        __hash = (ap ^ bp ^ cp) % n_h

        return __hash

    def query(self, x, y, z):
        __hash = self.compute_hash(m_vec.Vector([x, y, z]))
        if __hash in self.__hash_table:
            return self.__hash_table[__hash]

    def search(self, _object, kernel_h, approx=True):
        l = self.__l

        r_chap_obj = self.compute_r_chap(_object)
        assert isinstance(r_chap_obj, m_vec.Vector)
        bounding_box_demi_size = m_vec.Vector(floor(kernel_h / l), floor(kernel_h / l), floor(kernel_h / l))
        r_chap_low = r_chap_obj - bounding_box_demi_size
        r_chap_high = r_chap_obj + bounding_box_demi_size

        possible = []

        for x in range(int(r_chap_low[0]), int(r_chap_high[0])):
            for y in range(int(r_chap_low[1]), int(r_chap_high[1])):
                for z in range(int(r_chap_low[2]), int(r_chap_high[2])):
                    query = self.query(x, y, z)
                    if query is not None:
                        for q in query:
                            possible.append(q)

        if approx:
            return possible
        else:
            val = []
            for it in possible:
                distance = (it.location.value - _object.location.value).norm()
                if distance < kernel_h:
                    val.append(it)
            return val


if __name__ == "__main__":
    import random
    import cProfile
    import io
    from pstats import Stats

    a = [m_vec.Vector([random.randint(0, 10),
                       random.randint(0, 10),
                       random.randint(0, 10)]) for i in range(200)]
    #b = [m_part.ActiveParticule(vec, 2) for vec in a]
    _hash = Hash(4, 8000)

    pr1 = cProfile.Profile()
    pr1.enable()
    #for part in b:
        #_hash.insert(part)
    pr1.disable()

    pr2 = cProfile.Profile()
    pr2.enable()
    #print(b[106])
    #print(_hash.search(b[106], 5, approx=False))
    pr2.disable()

    s1 = io.StringIO()
    s2 = io.StringIO()
    sort_by = 'tottime'

    ps1 = Stats(pr1, stream=s1).sort_stats(sort_by)
    ps1.print_stats()
    print(s1.getvalue())

    ps2 = Stats(pr2, stream=s2).sort_stats(sort_by)
    ps2.print_stats()
    print(s2.getvalue())
