__author__ = 'salas'

import sys
from PyQt4 import QtGui, QtCore

import app.gui.widget_node as g_no


class NodeEditor(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        #on place le point de pivot des transformation au niveau du pointeur
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        #on cache les scrollBar
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #active l’antialiasing
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        #creation du scene qui contient les items et sera dans la QView
        self.scene = QtGui.QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)

        #Ajout d'une grille en fond
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(60, 60, 60), QtCore.Qt.CrossPattern))

        #creation de deux elipse simple a la scene, selectable et movable
        ep = self.scene.addEllipse(20, 40, 50, 50)
        ep.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        ep.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        node1 = g_no.Node(self)
        node2 = g_no.Node(self)

        self.scene.addItem(node1)
        self.scene.addItem(node2)

        self.scene.addItem(g_no.Edge(node1, node2))

        #parametrage du drag mode  rubber …. permet davoir un lasso rectangulaire de selection
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
        self.setScene(self.scene)


    #alt drag scroll bar, permet de se deplacer dans le graph grace a la touche alt.
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

# app = QtGui.QApplication(sys.argv)
# d = NodeEditor()
# d.show()
# sys.exit(app.exec_())