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
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class CreateProjectWindows(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Title")
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        self.tt = QLineEdit()
        self.dt = QLineEdit()
        self.l = QLineEdit()
        self.n = QLineEdit()

        self.layout_f = QFormLayout()
        self.layout_f.addRow("Total time", self.tt)
        self.layout_f.addRow("Time step", self.dt)
        self.layout_f.addRow("Grid size", self.l)
        self.layout_f.addRow("Number of particles", self.n)

        self.layout_v = QVBoxLayout()
        self.b_ob = QPushButton('&Ok')
        self.b_ob.clicked.connect(self.close)
        self.layout_v.addLayout(self.layout_f)
        self.layout_v.addWidget(self.b_ob)

        self.setLayout(self.layout_v)

    @staticmethod
    def get_properties(parent=None):
        window = CreateProjectWindows(parent)
        window.exec_()
        return float(window.tt.text()), float(window.dt.text()), float(window.l.text()), float(window.n.text())


