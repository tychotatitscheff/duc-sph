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

import numpy as np
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt


class Image():
    def __init__(self, array, N=60j, disp_angle=None, selected_state=None):
        if not disp_angle:
            disp_angle = ['x', 'y']
        if not selected_state:
            selected_state = ['speed', 'acceleration', 'reaction_location_diff', 'reaction_speed_diff',
                              'pressure_force', 'viscosity_force', 'surface_tension_force']
        self.__selected_state = selected_state
        self.__disp = disp_angle

        # slice the array to get position
        self.__x = array[:, 0, 0]
        self.__y = array[:, 0, 1]

        self.__extent = (np.min(self.__x), np.max(self.__x), np.min(self.__y), np.max(self.__y))

        self.__xs, self.__ys = np.mgrid[self.__extent[0]:self.__extent[1]:N, self.__extent[2]:self.__extent[3]:N]

        if 'speed' in selected_state:
            # slice the array and compute the norm of the speed
            self.__s_x = griddata(self.__x, self.__y, array[:, 1, 0], self.__xs, self.__ys)
            self.__s_y = griddata(self.__x, self.__y, array[:, 1, 1], self.__xs, self.__ys)
            self.__s_z = griddata(self.__x, self.__y, array[:, 1, 2], self.__xs, self.__ys)
            s = array[:, 1, :]
            self.__s = griddata(self.__x, self.__y, np.sqrt((s * s).sum(axis=1)), self.__xs, self.__ys)

        if 'acceleration' in selected_state:
            # slice the array and compute the norm of the acceleration
            self.__a_x = griddata(self.__x, self.__y, array[:, 2, 0], self.__xs, self.__ys)
            self.__a_y = griddata(self.__x, self.__y, array[:, 2, 1], self.__xs, self.__ys)
            self.__a_z = griddata(self.__x, self.__y, array[:, 2, 2], self.__xs, self.__ys)
            a = array[:, 2, :]
            self.__a = griddata(self.__x, self.__y, np.sqrt((a * a).sum(axis=1)), self.__xs, self.__ys)

        if 'reaction_location_diff' in selected_state:
            # slice the array and compute the norm of the collision location
            self.__cl_x = griddata(self.__x, self.__y, array[:, 3, 0], self.__xs, self.__ys)
            self.__cl_y = griddata(self.__x, self.__y, array[:, 3, 1], self.__xs, self.__ys)
            self.__cl_z = griddata(self.__x, self.__y, array[:, 3, 2], self.__xs, self.__ys)
            cl = array[:, 3, :]
            self.__cl = griddata(self.__x, self.__y, np.sqrt((cl * cl).sum(axis=1)), self.__xs, self.__ys)

        if 'reaction_speed_diff' in selected_state:
            # slice the array and compute the norm of the collision speed
            self.__cs_x = griddata(self.__x, self.__y, array[:, 4, 0], self.__xs, self.__ys)
            self.__cs_y = griddata(self.__x, self.__y, array[:, 4, 1], self.__xs, self.__ys)
            self.__cs_z = griddata(self.__x, self.__y, array[:, 4, 2], self.__xs, self.__ys)
            cs = array[:, 4, :]
            self.__cs = griddata(self.__x, self.__y, np.sqrt((cs * cs).sum(axis=1)), self.__xs, self.__ys)

        if 'pressure_force' in selected_state:
            # slice the array and compute the norm of the pressure force
            self.__fp_x = griddata(self.__x, self.__y, array[:, 5, 0], self.__xs, self.__ys)
            self.__fp_y = griddata(self.__x, self.__y, array[:, 5, 1], self.__xs, self.__ys)
            self.__fp_z = griddata(self.__x, self.__y, array[:, 5, 2], self.__xs, self.__ys)
            fp = array[:, 5, :]
            self.__fp = griddata(self.__x, self.__y, np.sqrt((fp * fp).sum(axis=1)), self.__xs, self.__ys)

        if 'viscosity_force' in selected_state:
            # slice the array and compute the norm of the pressure force
            self.__fv_x = griddata(self.__x, self.__y, array[:, 6, 0], self.__xs, self.__ys)
            self.__fv_y = griddata(self.__x, self.__y, array[:, 6, 1], self.__xs, self.__ys)
            self.__fv_z = griddata(self.__x, self.__y, array[:, 6, 2], self.__xs, self.__ys)
            fv = array[:, 6, :]
            self.__fv = griddata(self.__x, self.__y, np.sqrt((fv * fv).sum(axis=1)), self.__xs, self.__ys)

        if 'surface_tension_force' in selected_state:
            # slice the array and compute the norm of the pressure force
            self.__fs_x = griddata(self.__x, self.__y, array[:, 7, 0], self.__xs, self.__ys)
            self.__fs_y = griddata(self.__x, self.__y, array[:, 7, 1], self.__xs, self.__ys)
            self.__fs_z = griddata(self.__x, self.__y, array[:, 7, 2], self.__xs, self.__ys)
            fs = array[:, 7, :]
            self.__fs = griddata(self.__x, self.__y, np.sqrt((fs * fs).sum(axis=1)), self.__xs, self.__ys)

    def generate(self):
        selected_state = self.__selected_state
        if 'speed' in selected_state:
            plt.imshow(self.__s.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de la vitesse  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_sp.png')
            plt.clf()
            plt.imshow(self.__s_x.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Vitesse selon x  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_sp_x.png')
            plt.clf()
            plt.imshow(self.__s_y.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Vitesse selon y (step=0)")
            plt.colorbar()
            plt.savefig('000_sp_y.png')
            plt.clf()
            plt.imshow(self.__s_z.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Vitesse selon z  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_sp_z.png')
            plt.clf()
        if 'acceleration' in selected_state:
            plt.imshow(self.__a.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de l'accélération  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_acc.png')
            plt.clf()
            plt.imshow(self.__a_x.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Accélération selon x  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_acc_x.png')
            plt.clf()
            plt.imshow(self.__a_y.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Accélération selon y  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_acc_y.png')
            plt.clf()
            plt.imshow(self.__a_z.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Accélération selon z  \n (step=0)")
            plt.colorbar()
            plt.savefig('000_acc_z.png')
            plt.clf()
        if 'reaction_location_diff' in selected_state:
            plt.imshow(self.__cl.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de la correction de position  en cas de collision \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cl.png')
            plt.clf()
            plt.imshow(self.__cl_x.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Correction de position selon x  en cas de collision \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cl_x.png')
            plt.clf()
            plt.imshow(self.__cl_y.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Correction de position selon y  en cas de collision \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cl_y.png')
            plt.clf()
            plt.imshow(self.__cl_z.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Correction de position selon z  en cas de collision \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cl_z.png')
            plt.clf()
        if 'reaction_speed_diff' in selected_state:
            plt.imshow(self.__cs.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de la correction de vitesse en cas de collision \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cs.png')
            plt.clf()
            plt.imshow(self.__cs_x.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Correction de vitesse selon x \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cs_x.png')
            plt.clf()
            plt.imshow(self.__cs_y.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Correction de vitesse selon y \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cs_y.png')
            plt.clf()
            plt.imshow(self.__cs_z.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Correction de vitesse selon z \n (step=0)")
            plt.colorbar()
            plt.savefig('000_cs_z.png')
            plt.clf()
        if 'pressure_force' in selected_state:
            plt.imshow(self.__fp.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de l'action de la pression \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fp.png')
            plt.clf()
            plt.imshow(self.__fp_x.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Action de la pression selon x \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fp_x.png')
            plt.clf()
            plt.imshow(self.__fp_y.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Action de la pression selon y \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fp_y.png')
            plt.clf()
            plt.imshow(self.__fp_z.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Action de la pression selon z \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fp_z.png')
            plt.clf()
        if 'viscosity_force' in selected_state:
            plt.imshow(self.__fv.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de la force de viscosité (step=0)")
            plt.colorbar()
            plt.savefig('000_fv.png')
            plt.clf()
            plt.imshow(self.__fv_x.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Force de viscosité selon x \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fv_x.png')
            plt.clf()
            plt.imshow(self.__fv_y.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Force de viscosité selon y \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fv_y.png')
            plt.clf()
            plt.imshow(self.__fv_z.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Force de viscosité selon z \n (step=0)")
            plt.colorbar()
            plt.savefig('000_fv_z.png')
            plt.clf()
        if 'surface_tension_force' in selected_state:
            plt.imshow(self.__fs.T, extent=self.__extent)
            plt.plot(self.__x, self.__y, "w.")
            plt.title("Norme de la force tension de surface (step=0)")
            plt.colorbar()
            plt.savefig('000_fs.png')
            plt.clf()

