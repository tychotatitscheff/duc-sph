from OpenGL.GL import *
from OpenGL.GLU import *
from .figure import Figure

class Sphere(Figure):
    """A single 3D sphere."""

    def __str__(self):
        """Returns a human-friendly version of this object's name."""
        return "esfera " + str(self.id)

    def do_draw(self):
        """Draws the sphere."""

        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, self.size, 36, 36)
        gluDeleteQuadric(quadric)
