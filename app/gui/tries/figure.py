from math import cos, pi
from operator import add, mul
from random import seed, random

from OpenGL.GL import *
from OpenGL.GLU import *

from misc import get_identity_matrix

class Figure:
    """A general 3D figure."""

    # Initialize static variables.
    seed()
    color_seed = random() * pi
    id_counter = 0

    def __init__(self):
        """Initializes a new instance with the default attributes."""
        # Coordinate-related attributes.
        self.size = 0.2 # Size is the radius of the sphere that "contains" the figure.
        self.size_perm = self.size
        self.position = [0.0, 0.0, 0.0]
        self.position_perm = self.position
        self.rotation_matrix = get_identity_matrix()
        self.rotation_matrix_perm = self.rotation_matrix
        # General attributes.
        self.id = Figure.id_counter
        Figure.id_counter += 1
        self.selected = False
        self.highlighted = False
        self.color = self.get_color_from_id()

    def __str__(self):
        """Returns a human-friendly version of this object's name."""
        return "figura " + str(self.id)

    def get_size(self):
        """Returns this figure's size."""
        return self.size

    def get_center(self):
        """Returns this figure's center."""
        return self.position

    def draw(self):
        """Draws the figure based on its current attributes."""

        # Set the color.
        glColorMaterial(GL_FRONT_AND_BACK, GL_EMISSION)
        if self.highlighted and not self.selected:
            glColor3f(0.2, 0.2, 0.2)
        else:
            glColor3f(0.0, 0.0, 0.0)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT)
        glColor3fv(map(mul, self.get_draw_color(), [0.5, 0.5, 0.5]))
        glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
        glColor3fv(map(mul, self.get_draw_color(), [0.8, 0.8, 0.8]))
        glColorMaterial(GL_FRONT_AND_BACK, GL_SPECULAR)
        glColor3fv(map(mul, self.get_draw_color(), [1.0, 1.0, 1.0]))
        glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 100)

        # Set the drawing matrix.
        glMatrixMode(GL_MODELVIEW)

        # Duplicate the top matrix so the modelview matrix isn't affected by the cube drawing.
        glPushMatrix()

        # Position the object on it's position attributes.
        glTranslatef(self.position[0], self.position[1], self.position[2])

        # Rotate to the object's rotation attributes.
        glMultMatrixf(self.rotation_matrix)

        # Set the figure's name for picking.
        glLoadName(self.id)

        # Do the actual drawing.
        self.do_draw()

        # Restablish the previous (scene) modelview matrix configurations.
        glPopMatrix()

    def do_draw(self):
        """Performs the actual drawing. Must be overridden in the derived classes."""
        pass

    def select(self, selecting=True):
        """Selects or unselects this figure."""
        self.selected = selecting

    def highlight(self, highlighting=True):
        """Marks this figure as highlighted or not."""
        self.highlighted = highlighting

    def move(self, x, y, z):
        """Moves temporarily this figure relative to its current position."""
        self.position = map(add, self.position_perm, [x, y, z])

    def move_end(self):
        """Permanently applies the figure movement."""
        self.position_perm = self.position

    def rotate(self, angle, x, y, z):
        """Rotates temporarily this figure relative to its current rotation."""
        angle *= 500 # Figures have a higher sensibility than the scene.
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glRotatef(angle, x, y, z)
        glMultMatrixf(self.rotation_matrix_perm)
        self.rotation_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

    def rotate_end(self):
        """Permanently applies the figure rotation."""
        self.rotation_matrix_perm = self.rotation_matrix

    def scale(self, increment):
        """Scales temporarily the figure."""
        if increment > 0:
            self.size = self.size_perm * (1 + (increment / 100.0))
        else:
            self.size = self.size_perm / (1 - (increment / 100.0))
        if self.size < 0.0001:
            self.size = 0.0001

    def scale_end(self):
        """Permanently applies the figure scaling."""
        self.size_perm = self.size

    def get_win_coords(self):
        """Returns the projected coordinates of the figure's center."""
        return gluProject(self.position_perm[0], self.position_perm[1], self.position_perm[2])

    def get_draw_color(self):
        """Gets the color the figure should be drawn with."""
        if self.selected:
            return [0.8, 0.0, 0.0]
        else:
            return self.color

    def get_color_from_id(self):
        """Builds a figure color based on the current id."""
        increment = 2 * pi / 3
        r = 0.5 + (cos((self.id / 5.0) + (increment * 0) + Figure.color_seed) / 4)
        g = 0.5 + (cos((self.id / 5.0) + (increment * 1) + Figure.color_seed) / 4)
        b = 0.5 + (cos((self.id / 5.0) + (increment * 2) + Figure.color_seed) / 4)
        return [r, g, b]
