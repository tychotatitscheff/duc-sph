__author__ = 'salas'

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

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL import GLU


import app.gui.figure.sphere as f_sphere


class GLWidget(QtOpenGL.QGLWidget):
    GL_MULTISAMPLE = 0x809D
    GLX_SAMPLE_BUFFERS = 1
    GLX_SAMPLES = 4

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.object = 0
        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.x_trans = 0.5
        self.y_trans = 0.5
        self.scale = .5

        self.last_pos = QtCore.QPoint()

        self.troll_tech_green = QtGui.QColor.fromCmykF(0.20, 0.4, 1.0, 0.0)
        self.troll_tech_purple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.vertices = None
        self.index = None
        self.color = None

    def get_rotation_x(self):
        return self.x_rot

    def get_rotation_y(self):
        return self.y_rot

    def get_rotation_z(self):
        return self.z_rot

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def set_rotation_x(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self.x_rot:
            self.x_rot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.updateGL()

    def set_rotation_y(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self.y_rot:
            self.y_rot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.updateGL()

    def set_rotation_z(self, angle):
        angle = self.normalize_angle(angle)
        if angle != self.z_rot:
            self.z_rot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.updateGL()

    def set_scale(self, scale):
        if scale != self.scale:
            self.scale = abs(scale)
            self.emit(QtCore.SIGNAL("ScaleChanged(int)"), scale)
            self.updateGL()

    def set_trans_x(self, trans):
        if trans != self.x_trans:
            self.x_trans = trans
            self.emit(QtCore.SIGNAL("xTransChanged(int)"), trans)
            self.updateGL()

    def set_trans_y(self, trans):
        if trans != self.y_trans:
            self.y_trans = trans
            self.emit(QtCore.SIGNAL("yTransChanged(int)"), trans)
            self.updateGL()

    def initializeGL(self):
        self.qglClearColor(self.troll_tech_purple.darker())
        self.make_object()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_POINT_SMOOTH)
        GL.glEnable(GLWidget.GL_MULTISAMPLE)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
        GL.glHint(GL.GL_POINT_SMOOTH_HINT, GL.GL_NICEST)
        GL.glHint(GL.GL_POLYGON_SMOOTH_HINT, GL.GL_NICEST)
        GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glLoadIdentity()
        GL.glTranslate(self.x_trans, self.y_trans, -50)
        GL.glRotated(self.x_rot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.y_rot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.z_rot / 16.0, 0.0, 0.0, 1.0)
        GL.glScale(self.scale, self.scale, self.scale)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)
        GL.glVertexPointerf(self.vertices)
        GL.glColorPointerf(self.color)
        GL.glDrawElementsui(GL.GL_QUADS, self.index.tolist())

    def resizeGL(self, width, height):
        side = min(width, height)
        #GL.glViewport(int((width - side) / 2), int((height - side) / 2), side, side)
        #
        # GL.glMatrixMode(GL.GL_PROJECTION)
        # GL.glLoadIdentity()
        #GL.glOrtho(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0)
        # GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.last_pos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & QtCore.Qt.MiddleButton:
            self.set_trans_x(self.x_trans + .1 * dx)
            self.set_trans_y(self.y_trans - .1 * dy)
        elif event.buttons() & QtCore.Qt.LeftButton:
            self.set_rotation_x(self.x_rot + 8 * dy)
            self.set_rotation_z(self.z_rot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.set_scale(self.scale + .05 * dy)

        self.last_pos = QtCore.QPoint(event.pos())

    def wheelEvent(self, event):
        delta = event.delta()
        self.set_scale(self.scale + delta / 180)

    def make_object(self):
        col = [0.8, 0.8, 0.8]
        for j in range(1, 10):
            v = f_sphere.add_sphere_vertices(np.array([2.4 * j, 0, 0]), 1)
            if self.vertices is None:
                i = f_sphere.add_sphere_index()
                c = [col for x in i]
                self.vertices = v
                self.index = i
                self.color = c
            else:
                idx_max = np.amax(self.index) + 1
                i = f_sphere.add_sphere_index(idx_max)
                c = [col for x in i]
                self.vertices = np.append(self.vertices, v, axis=0)
                self.index = np.append(self.index, i)
                self.color.extend(c)


    @staticmethod
    def normalize_angle(angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle