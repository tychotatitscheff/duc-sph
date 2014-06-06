import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
import numpy as np


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.y_rot_deg = 0.0
        self.vertices = np.array([[]])
        self.faces = np.array([])

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 150))
        self.add_sphere(np.array([0, 0, 0]), 1)

        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        if height == 0:
            height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslate(0.0, 0.0, -50.0)
        glScale(20.0, 20.0, 20.0)
        glRotate(self.y_rot_deg, 0.2, 1.0, 0.3)
        glTranslate(-0.5, -0.5, -0.5)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vertices)
        glDrawElementsui(GL_TRIANGLES, self.faces)

    def add_sphere(self, position, radius):
        vertices = np.array(
            [[0.000000, -1.000000, 0.000000], [0.723607, -0.447220, 0.525725], [-0.276388, -0.447220, 0.850649],
             [-0.894426, -0.447216, 0.000000], [-0.276388, -0.447220, -0.850649], [0.723607, -0.447220, -0.525725],
             [0.276388, 0.447220, 0.850649], [-0.723607, 0.447220, 0.525725], [-0.723607, 0.447220, -0.525725],
             [0.276388, 0.447220, -0.850649], [0.894426, 0.447216, 0.000000], [0.000000, 1.000000, 0.000000],
             [-0.162456, -0.850654, 0.499995], [0.425323, -0.850654, 0.309011], [0.262869, -0.525738, 0.809012],
             [0.850648, -0.525736, 0.000000], [0.425323, -0.850654, -0.309011], [-0.525730, -0.850652, 0.000000],
             [-0.688189, -0.525736, 0.499997], [-0.162456, -0.850654, -0.499995], [-0.688189, -0.525736, -0.499997],
             [0.262869, -0.525738, -0.809012], [0.951058, 0.000000, 0.309013], [0.951058, 0.000000, -0.309013],
             [0.000000, 0.000000, 1.000000], [0.587786, 0.000000, 0.809017], [-0.951058, 0.000000, 0.309013],
             [-0.587786, 0.000000, 0.809017], [-0.587786, 0.000000, -0.809017], [-0.951058, 0.000000, -0.309013],
             [0.587786, 0.000000, -0.809017], [0.000000, 0.000000, -1.000000], [0.688189, 0.525736, 0.499997],
             [-0.262869, 0.525738, 0.809012], [-0.850648, 0.525736, 0.000000], [-0.262869, 0.525738, -0.809012],
             [0.688189, 0.525736, -0.499997], [0.162456, 0.850654, 0.499995], [0.525730, 0.850652, 0.000000],
             [-0.425323, 0.850654, 0.309011], [-0.425323, 0.850654, -0.309011], [0.162456, 0.850654, -0.499995]])

        faces = np.array(
            [1, 14, 13, 2, 14, 16, 1, 13, 18, 1, 18, 20, 1, 20, 17, 2, 16, 23, 3, 15, 25, 4, 19, 27,
             5, 21, 29, 6, 22, 31, 2, 23, 26, 3, 25, 28, 4, 27, 30, 5, 29, 32, 6, 31, 24, 7, 33, 38,
             8, 34, 40, 9, 35, 41, 10, 36, 42, 11, 37, 39, 13, 15, 3, 13, 14, 15, 14, 2, 15, 16, 17, 6,
             16, 14, 17, 14, 1, 17, 18, 19, 4, 18, 13, 19, 13, 3, 19, 20, 21, 5, 20, 18, 21, 18, 4, 21,
             17, 22, 6, 17, 20, 22, 20, 5, 22, 23, 24, 11, 23, 16, 24, 16, 6, 24, 25, 26, 7, 25, 15, 26,
             15, 2, 26, 27, 28, 8, 27, 19, 28, 19, 3, 28, 29, 30, 9, 29, 21, 30, 21, 4, 30, 31, 32, 10,
             31, 22, 32, 22, 5, 32, 26, 33, 7, 26, 23, 33, 23, 11, 33, 28, 34, 8, 28, 25, 34, 25, 7, 34,
             30, 35, 9, 30, 27, 35, 27, 8, 35, 32, 36, 10, 32, 29, 36, 29, 9, 36, 24, 37, 11, 24, 31, 37,
             31, 10, 37, 38, 39, 12, 38, 33, 39, 33, 11, 39, 40, 38, 12, 40, 34, 38, 34, 7, 38, 41, 40, 12,
             41, 35, 40, 35, 8, 40, 42, 41, 12, 42, 36, 41, 36, 9, 41, 39, 42, 12, 39, 37, 42, 37, 10, 42])

        self.vertices = np.append(self.vertices, vertices * radius + position)
        if np.alen(self.faces) > 0:
            self.faces = np.append(self.faces, faces + np.amax(self.faces))

        else:
            print(faces)
            self.faces = faces

    def spin(self):
        self.y_rot_deg = (self.y_rot_deg + 1) % 360.0
        self.parent.statusBar().showMessage('rotation %f' % self.y_rot_deg)
        self.updateGL()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(300, 300)
        self.setWindowTitle('GL Cube Test')

        self.initActions()
        self.initMenus()

        glWidget = GLWidget(self)
        self.setCentralWidget(glWidget)

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        QtCore.QObject.connect(timer, QtCore.SIGNAL('timeout()'), glWidget.spin)
        timer.start()


    def initActions(self):
        self.exitAction = QtGui.QAction('Quit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.connect(self.exitAction, QtCore.SIGNAL('triggered()'), self.close)

    def initMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

    def close(self):
        QtGui.qApp.quit()


app = QtGui.QApplication(sys.argv)

win = MainWindow()
win.show()

sys.exit(app.exec_())

