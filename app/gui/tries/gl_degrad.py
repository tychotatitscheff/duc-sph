from PyQt4.QtOpenGL import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from OpenGL.GL import *
from OpenGL.GLU import *

from .scene import Scene
from .sphere import Sphere

class GlWidget(QGLWidget):
    """An OpenGL canvas widget."""

    def __init__(self, parent=None):
        """Constructor. Allows the user to specify a parent (optional)."""
        super(GlWidget, self).__init__(parent)
        self.scene = Scene(self.width(), self.height())
        # Initialize action (dragging) variables.
        self.action_button = Qt.NoButton
        self.action_x = 0
        self.action_y = 0
        self.action_nomove = False

    def initializeGL(self):
        """Callback for OpenGL initialization."""
        # Set general lightning attributes.
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.25, 0.25, 0.25])
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)
        
        # Set up the light source.
        light_direction = [1.0, 2.0, 3.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE | GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glEnable(GL_LIGHT0)

    def paintGL(self):
        """Callback for redrawing the window."""
        # Reset the matrices
        self.scene.reset_matrices()
        # Let the scene draw itself.
        self.scene.draw()
        # Display the number of figures.
        self.window().statusBar().count_label.setText("Figuras: {0}"
            .format(len(self.scene.figures)))

    def resizeGL(self, width, height):
        """Callback for resizing the window."""
        # Change the viewport to avoid stretching.
        glViewport(0, 0, width, height)
        self.scene.set_width(width)
        self.scene.set_height(height)

    def keyPressEvent(self, keyEvent):
        """Callback for handling keypresses."""
        # When user presses C: create a cube.
        if keyEvent.key() == Qt.Key_C:
            self.addFigure(Cube())

        # When user presses E: create a sphere.
        elif keyEvent.key() == Qt.Key_E:
            self.addFigure(Sphere())

        # When user presses X: delete selected object.
        elif keyEvent.key() == Qt.Key_X:
            figure = self.scene.selected_figure
            if figure != None:
                self.scene.remove(figure)
                self.window().statusBar().showMessage(
                    "{0} apagado(a) em ({1:.3}, {2:.3}, {3:.3})."
                    .format(str(figure).capitalize(), figure.position[0],
                    figure.position[1], figure.position[2]), 1000)
                self.updateGL()
            else:
                self.window().statusBar().showMessage(
                    "Nenhuma figura selecionada. Nao e possivel apagar.", 500)

        # When user presses Home: reposition the camera.
        elif keyEvent.key() == Qt.Key_Home:
            self.scene.show_all()
            self.window().statusBar().showMessage("Camera reposicionada.", 1000)
            self.updateGL()

        # Ignore other keypresses.
        else:
            keyEvent.ignore()

    def mousePressEvent(self, mouseEvent):
        """Callback for handling mouse button pressings.
        Marks down the initial mouse position of the movement."""
        # Only one action allowed at a time.
        if self.action_button != Qt.NoButton:
            return
        # Save the button and initial position.
        self.action_button = mouseEvent.button()
        self.action_x = mouseEvent.x()
        self.action_y = mouseEvent.y()
        self.action_nomove = True

    def mouseMoveEvent(self, mouseEvent):
        """Callback for handling mouse movement."""
        self.window().statusBar().mouse_label.setText("({0}, {1})"
            .format(mouseEvent.x(), mouseEvent.y()))

        # Apply a highlight effect on hovered figures, but only when not pressing anything.
        if self.action_button == Qt.NoButton:
            figure = self.scene.get_figure_at(mouseEvent.x(), self.height() - mouseEvent.y())
            self.scene.highlight(figure)
            self.updateGL()
            # The rest of the code only matters when a button is pressed.
            return
        else:
            self.scene.highlight(None)


        # Select what we're going to move: a figure or the scene.
        object = self.scene.selected_figure
        mult = 1
        if object == None:
            object = self.scene
            mult = -1

        # Action 1: moving/panning.
        if self.action_button == Qt.LeftButton:
            # Get the space coordinates of the mouse movement.
            old_coords = self.scene.get_coords_at(self.action_x, self.height() - self.action_y, object)
            new_coords = self.scene.get_coords_at(mouseEvent.x(), self.height() - mouseEvent.y(), object)
            # Move the object.
            self.window().statusBar().showMessage("Movimentando {0}.".format(object))
            object.move((new_coords[0] - old_coords[0]) * mult,
                        (new_coords[1] - old_coords[1]) * mult,
                        (new_coords[2] - old_coords[2]) * mult)

        # Action 2: rotating.
        elif self.action_button == Qt.RightButton:
            # Get the space coordinates of the mouse movement.
            old_coords = gluUnProject(self.action_x, self.height() - self.action_y, 0)
            new_coords = gluUnProject(mouseEvent.x(), self.height() - mouseEvent.y(), 0)
            # Get the rotation using arcball.
            arcball = ObjArcBall(object.get_size(), object.get_center())
            arcball.setStartPoint(old_coords[0], old_coords[1], old_coords[2])
            arcball.setEndPoint(new_coords[0], new_coords[1], new_coords[2])
            # Apply the rotation.
            rotation = arcball.getRot()
            object.rotate(rotation[0], rotation[1][0], rotation[1][1], rotation[1][2])
            self.window().statusBar().showMessage("Rotacionando {0}.".format(object))

        # Action 3: zooming (scene only).
        elif self.action_button == Qt.MidButton:
            self.window().statusBar().showMessage("Aplicando zoom na cena.")
            self.scene.scale((self.action_y - mouseEvent.y()) / 10.0)

        # Update the action variables and redraw the screen.
        self.action_nomove = False
        self.updateGL()

    def mouseReleaseEvent(self, mouseEvent):
        """Callback for handling the release of a mouse button.
        Ends a movement-based action, or performs a figure selection."""
        # Only the initially pressed button matters.
        if mouseEvent.button() != self.action_button:
            return

        # Apply the movement.
        object = self.scene.selected_figure
        if object == None:
            object = self.scene
        if self.action_button == Qt.LeftButton:
            object.move_end()
        if self.action_button == Qt.RightButton:
            object.rotate_end()
        if self.action_button == Qt.MidButton:
            object.scale_end()

        # Mark the movement as finished.
        self.action_button = Qt.NoButton
        self.window().statusBar().clearMessage()

        # If this was the left button AND the user didn't move the mouse,
        # we consider this to be a selection attempt.
        if mouseEvent.button() == Qt.LeftButton and self.action_nomove:
            figure = self.scene.get_figure_at(self.action_x, self.height() - self.action_y)
            if figure == None:
                if self.scene.selected_figure != None:
                    self.window().statusBar().showMessage("Selecao removida.", 500)
            else:
                self.window().statusBar().showMessage(
                "{0} selecionado(a) em ({1:.3}, {2:.3}, {3:.3})."
                .format(str(figure).capitalize(), figure.position[0],
                figure.position[1], figure.position[2]), 1000)
            self.scene.select(figure)

        # Update the screen.
        self.updateGL()

    def wheelEvent(self, wEvent):
        """Callback for handling mousewheel scrolling events.
        Scales the scene or the selected object."""
        object = self.scene.selected_figure
        if object == None:
            object = self.scene
        self.window().statusBar().showMessage(
            "Aplicando escala no(a) {0}.".format(object), 300)
        object.scale(wEvent.delta() / 120)
        object.scale_end()
        self.updateGL()

    def addFigure(self, figure):
        """Adds the given figure to the scene (based on the current mouse
        coordinates), sets the statusbar text and triggers a screen refresh."""

        # Get screen and scene coordinates.
        pos = self.mapFromGlobal(QCursor.pos())
        (x, y, z) = self.scene.get_coords_at(pos.x(), self.height() - pos.y(), None)

        # Position, add and highlight the figure.
        figure.move(x, y, z)
        figure.move_end()
        self.scene.add(figure)
        self.scene.highlight(figure)

        # Show message and refresh the screen.
        self.window().statusBar().showMessage(
            "{0} criado(a) em ({1:.3}, {2:.3}, {3:.3})."
            .format(str(figure).capitalize(), x, y, z), 1000)
        self.updateGL()

    def restart(self):
        """Resets the scene."""
        self.scene = Scene(self.width(), self.height())
        self.window().statusBar().showMessage("Cena reiniciada ({0})."
            .format(QTime.currentTime().toString("HH:mm:ss")) , 2000)
        self.updateGL()
