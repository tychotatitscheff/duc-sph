__author__ = 'salas'

import sys
import math
import numpy as np

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

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

        self.last_pos = QtCore.QPoint()

        self.troll_tech_green = QtGui.QColor.fromCmykF(0.20, 0.4, 1.0, 0.0)
        self.troll_tech_purple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

        self.draw = ()

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

    def initializeGL(self):
        self.qglClearColor(self.troll_tech_purple.darker())
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
        self.draw = self.make_object()
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)
        GL.glRotated(self.x_rot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.y_rot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.z_rot / 16.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.draw[1].bind()

        self.draw[0].bind()

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, None)

        GL.glDrawElements(GL.GL_TRIANGLES, 3, GL.GL_UNSIGNED_INT, None)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-0.5, +0.5, -0.5, +0.5, 4.0, 15.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.last_pos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.set_rotation_x(self.x_rot + 8 * dy)
            self.set_rotation_y(self.y_rot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.set_rotation_x(self.x_rot + 8 * dy)
            self.set_rotation_z(self.z_rot + 8 * dx)

        self.last_pos = QtCore.QPoint(event.pos())

    @staticmethod
    def make_object():
        vertices = None
        index = None
        for i in range(1, 3):
            if vertices is None:
                vertices = f_sphere.add_sphere_vertices(np.array([i, i, i]), 1)
                index = f_sphere.add_sphere_index()
            else:
                idx_max = np.amax(index)
                vertices = np.append(vertices, f_sphere.add_sphere_vertices(np.array([i, i, i]), 1))
                index = np.append(index, f_sphere.add_sphere_index(idx_max))
        vertexPositions = vbo.VBO(vertices)
        indexPositions = vbo.VBO(index, target=GL.GL_ELEMENT_ARRAY_BUFFER)
        return vertexPositions, indexPositions

    @staticmethod
    def normalize_angle(angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle