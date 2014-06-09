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

import concurrent.futures

import math
import numpy as np
import random

import app.solver.model.fluid as m_flu
import app.solver.model.particle as m_part
import app.solver.model.collision as m_col
import app.solver.model.kernel as m_kern
import app.solver.model.vector as m_vec

from app.solver.conf import *


class SphSolver():
    def __init__(self, tt, dt, hashing, collisions_objects=None):
        """

        :param tt: total times
        :param dt: interval / step
        :type tt: float
        :type dt: float
        """
        self.__tt = tt
        self.__t = 0
        self.__dt = dt
        self.__particles = hashing
        self.__collisions_objects = [] if collisions_objects is None else collisions_objects

    @property
    def t(self):
        return self.__t

    @t.setter
    def t(self, t):
        self.__t = t

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, t):
        self.__dt = t

    @property
    def tt(self):
        return self.__tt

    @property
    def collisions_objects(self):
        return self.__collisions_objects

    @property
    def particles(self):
        return self.__particles

    def create_active_particle(self, location, fluid, radius, fluid_type="liquid", gravity=True, speed=m_vec.Vector([0, 0, 0])):
        """

        :param location: location of the particle
        :param radius: h
        :param fluid: type of the particle
        :type location: vector (m_vec)
        :type radius: float
        :type fluid: fluid
        """

        act_part = m_part.ActiveParticle(self.particles, location, fluid, radius, speed=speed)
        h = str(hash(act_part))
        vec_null = m_vec.Vector([0, 0, 0])

        k_d = m_kern.Poly6Kernel(radius * 3)
        k_v = m_kern.ViscosityKernel(radius * 3)
        k_s = m_kern.SpikyKernel(radius * 3)

        if fluid_type == "liquid" or fluid_type == "gaz":
            d = m_part.Density("Density of " + h, k_s, fluid.rho0)

            p = m_part.Pressure("Pressure of " + h, m_part.ATMOSPHERIC_PRESSURE)

            f_p = m_part.ForcePressure("Pressure force of " + h, k_d, vec_null)
            f_v = m_part.ForceViscosity("Viscosity force of " + h, k_v, vec_null)

            act_part.density = d
            act_part.pressure = p

            act_part.append_force(f_p)
            act_part.append_force(f_v)

            if fluid_type == "liquid":
                f_s = m_part.ForceSurfaceTension("Surface tension force of " + h, k_d, vec_null)
                act_part.append_force(f_s, internal=False)

        if gravity:
            f_g = m_part.ForceGravity("Gravity force of " + h, k_d, m_vec.Vector([0, 0, -9.8]))
            act_part.append_force(f_g, internal=False)
        return act_part

    def step(self):
        print(self.t)
        # Compute density and pressure
        self.__compute_density_and_pressure()
        # Compute forces and integrate
        self.__compute_forces_and_integrate()
        # Check for collision
        self.__check_for_collision()
        # Generate numpy array
        np_array = self.__generate_numpy_array()
        # Update
        self.__update()
        return np_array

    def __compute_density_and_pressure(self):
        def try_compute_density(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        neigh = particle.neighbour(RADIUS_MULTIPLICATIVE * particle.radius)
                        particle.density.__call__(particle, neigh)
                        particle.pressure.__call__(particle)
                    except Exception as e:
                        print("Density computation : " + str(e))
        hashing = self.particles.hash_table.values()
        try_compute_density(hashing)

    def __compute_forces_and_integrate(self):
        def try_compute_forces_and_integrate(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        neigh = particle.neighbour(RADIUS_MULTIPLICATIVE * particle.radius)
                        particle.resultant_force = m_vec.Vector([0, 0, 0])
                        for force in particle.forces:
                            assert isinstance(force, m_part.Force)
                            force.__call__(particle, neigh)
                            particle.resultant_force += force.value
                        particle.future_acceleration.value = particle.resultant_force * 1. / particle.mass
                        particle.future_speed.value = particle.current_speed.value + particle.future_acceleration.value * self.dt
                        particle.future_location.value = particle.current_location.value + particle.future_speed.value * self.dt
                    except Exception as e:
                        print("Force computations and integration : " + str(e))
        hashing = self.particles.hash_table.values()
        try_compute_forces_and_integrate(hashing)

    def __check_for_collision(self):
        def try_check_for_collision(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        for coll_obj in self.collisions_objects:
                            assert isinstance(coll_obj, m_col.CollisionObject)
                            coll_obj.react(particle.future_location, self.dt)
                    except Exception as e:
                        print(e)
        hashing = self.particles.hash_table.values()
        try_check_for_collision(hashing)

    def __generate_numpy_array(self):
        def try_generate_numpy_array(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        loc = particle.current_location.value
                        speed = particle.future_speed.value
                        acc = particle.future_acceleration.value
                        col_loc = particle.reaction_location.value - particle.future_location.value
                        col_speed = particle.reaction_speed.value - particle.future_speed.value
                        force_pres, force_visc, force_st = m_vec.Vector([0, 0, 0])
                        for force in particle.forces:
                            if isinstance(force, m_part.ForcePressure):
                                force_pres = force.value
                            if isinstance(force, m_part.ForceViscosity):
                                force_visc = force.value
                            if isinstance(force, m_part.ForceSurfaceTension):
                                force_st = force.value
                        part_array = np.array([loc, speed, acc, col_loc, col_speed, force_pres, force_visc, force_st])
                        particles.append(part_array)
                    except Exception as e:
                        print(e)
        particles = []
        hashing = self.particles.hash_table.values()
        try_generate_numpy_array(hashing)
        return np.array(particles)

    def __update(self):
        def try_update(structure):
            for list_particles in structure:
                for particle in list_particles:
                    try:
                        assert isinstance(particle, m_part.ActiveParticle)
                        particle.resultant_force = m_vec.Vector([0, 0, 0])
                        particle.current_speed.value = particle.future_speed.value
                        particle.current_location.value = particle.current_location.value
                    except Exception as e:
                        print(e)
        hashing = self.particles.hash_table.values()
        try_update(hashing)

    def initial_volume(self, particle, primitive="non oriented cube", distribution="CFC", **kwargs):
        assert isinstance(particle, m_part.ActiveParticle)
        r = particle.radius
        part_list = []
        if 'speed' in kwargs:
            if kwargs['speed'] == "random":
                x = random.random()
                y = random.random()
                z = random.random()
                u = m_vec.Vector([x, y, z])
            else:
                isinstance(kwargs['speed'], m_vec.Vector)
                u = kwargs['speed']
        if primitive == "non oriented cube":
            if distribution == "CC":
                s = kwargs['size']
                dec = False
                for z in np.arange(r, s - r, 2 / math.sqrt(3) * r):
                    if dec:
                        a = 2 / math.sqrt(3) * r
                    else:
                        a = 0
                    for x in np.arange(a + r, s - r, 4 / math.sqrt(3) * r):
                        for y in np.arange(a + r, s - r, 4 / math.sqrt(3) * r):
                            part_list.append(m_vec.Vector([r * x, r * y, r * z]))
                    dec = not dec
            if distribution == "CFC":
                s = kwargs['size']
                dec = False
                for z in np.arange(r, s - r, 2 / math.sqrt(3) * r):
                    if dec:
                        a = 2 / math.sqrt(3) * r
                    else:
                        a = 0
                    for x in np.arange(a + r, s - r, 4 / math.sqrt(3) * r):
                        for y in np.arange(a + r, s - r, 4 / math.sqrt(3) * r):
                            part_list.append(m_vec.Vector([r * x, r * y, r * z]))
                    dec = not dec
        for element in part_list:
            if u is None:
                self.create_active_particle(element, particle.fluid, particle.radius)
            else:
                if kwargs['speed'] == "random":
                    x = random.random()
                    y = random.random()
                    z = random.random()
                    u = m_vec.Vector([x, y, z])
                self.create_active_particle(element, particle.fluid, particle.radius, speed=u)
        particle.__del__()
        return part_list

    def generative_surface(self, length, width, normal, particle, speed):
        assert isinstance(normal, m_vec.Vector)
        assert isinstance(particle, m_part.ActiveParticle)
        assert isinstance(speed, m_vec.Vector)
        r = particle.radius
        part_list = []
        for dim1 in np.arange(1, int(length), 2 * math.sqrt(2) * r):
            for dim2 in np.arange(1, int(width), 2 * math.sqrt(2) * r):
                part_list.append(m_vec.Vector([dim1, dim2, 0]))
        for element in part_list:
            p = self.create_active_particle(element, m_flu.Fluid, particle.radius)
            p.current_speed(speed)

