__author__ = 'salas'
import sys

import qdarkstyle
from PyQt4 import QtGui, QtCore

import app.gui.widgets.glViewer as g_gl
import app.gui.widgets.nodeEditor as g_ne


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
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

        self.main_layout = QtGui.QVBoxLayout(self.central_widget)
        self.splitter_v = QtGui.QSplitter(QtCore.Qt.Vertical)

        self.gl_widget = g_gl.GLWidget()
        self.splitter_v.addWidget(self.gl_widget)

        self.node_editor = g_ne.NodeEditor()
        self.splitter_v.addWidget(self.node_editor)

        self.splitter_h = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter_h.addWidget(self.splitter_v)

        self.properties = QtGui.QFrame()
        self.splitter_h.addWidget(self.properties)

        self.main_layout.addWidget(self.splitter_h)

        self.setCentralWidget(self.central_widget)

        self.setWindowTitle(self.tr("Duc-sph"))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    window = Window()
    window.show()
    sys.exit(app.exec_())