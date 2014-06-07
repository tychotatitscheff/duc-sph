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

import sys

import qdarkstyle
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class ProjectWindows(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFixedSize(800, 300)
        self.setWindowTitle("Title")
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        self.list_widget = QListWidget()

        self.layout_v = QVBoxLayout()
        self.layout_v.addWidget(self.list_widget)

        self.layout_h = QHBoxLayout()
        self.b_create = QPushButton("Create new")

        self.b_ok = QPushButton("Select and &quit")
        self.layout_h.addWidget(self.b_create)
        self.layout_h.addWidget(self.b_ok)

        #QWidget.connect(self.ok, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        self.b_ok.clicked.connect(self.close)
        self.b_create.clicked.connect(self.create_new)

        self.layout_v.addLayout(self.layout_h)

        self.setLayout(self.layout_v)

        self.project = None

    def add_item(self, name):
        item = QListWidgetItem(name)
        item.setIcon(QIcon(r"raindrop.png"))
        self.list_widget.addItem(item)

    @staticmethod
    def get_project(list_projects, parent=None):
        window = ProjectWindows(parent)
        for project in list_projects:
            window.add_item(project)
        window.exec_()
        if window.project is None:
            return list_projects[window.list_widget.currentRow()]
        else:
            return window.project

    def create_new(self):
        self.setEnabled(False)
        self.project = NewProject().new()
        self.close()


class NewProject(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.l_name = QLineEdit(self)
        self.b_create = QPushButton('create', self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.l_name)
        layout.addWidget(self.b_create)
        self.b_create.clicked.connect(self.close)

    @staticmethod
    def new(parent=None):
        window = NewProject(parent)
        window.exec_()
        return window.l_name.text()




