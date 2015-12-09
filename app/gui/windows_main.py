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

import sys

import qdarkstyle
from PyQt4 import QtGui, QtCore

#import widgets.glViewer as g_gl


class MainWindows(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.showMaximized()
        exit_action = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)

        self.statusBar()
        self.central_widget = QtGui.QWidget(self)

        # Menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)
        simulation_menu = menu_bar.addMenu('Simulation')

        self.main_layout = QtGui.QVBoxLayout(self.central_widget)
        self.splitter_v = QtGui.QSplitter(QtCore.Qt.Vertical)

        #self.gl_widget = g_gl.GLWidget()
        #self.splitter_v.addWidget(self.gl_widget)

        self.node_editor = QtGui.QFrame()
        self.splitter_v.addWidget(self.node_editor)

        self.splitter_v.setStretchFactor(0, 2)
        self.splitter_v.setStretchFactor(1, 1)

        self.splitter_h = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter_h.addWidget(self.splitter_v)

        self.properties = QtGui.QFrame()
        self.splitter_h.addWidget(self.properties)

        self.splitter_h.setStretchFactor(0, 7)
        self.splitter_h.setStretchFactor(1, 1)

        self.main_layout.addWidget(self.splitter_h)

        self.setCentralWidget(self.central_widget)

        self.setWindowTitle(self.tr("Duc-sph"))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    window = MainWindows()
    window.show()
    sys.exit(app.exec_())
