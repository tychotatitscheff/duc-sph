import math
from app.gui.tries.misc import *
from operator import add, sub

from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *


class Scene:
    """A scene in a 3D world."""

    def __init__(self, width, height):
        """Initializes a new instance with the given width and height."""
        # Set figure-related variables.
        Figure.id_counter = 1
        self.figures = []
        self.selected_figure = None
        self.highlighted_figure = None

        # Set scalars.
        self.camera_near = 1.0
        self.camera_far = 20.0
        self.width = width
        self.height = height

        # Set angles and vectors.
        self.position = [0.0, 0.0, (self.camera_near + self.camera_far) / 2]
        self.position_perm = self.position
        self.camera_position = [0.0, 0.0, -self.camera_near]
        self.camera_position_perm = self.camera_position
        self.rotation_matrix = get_identity_matrix()
        self.rotation_matrix_perm = self.rotation_matrix
        self.up = [0.0, 1.0, 0.0]
        self.up_perm = self.up
        self.zoom_angle = 65.0
        self.zoom_perm = self.zoom_angle

    def __str__(self):
        """Returns a human-friendly version of this object's name."""
        return "cena"

    def get_size(self):
        """Returns the scene's radius."""
        center = self.get_center()
        dist = 0
        for figure in self.figures:
            tempdist = math.sqrt(vector_module(map(sub, figure.position, center)))
            if tempdist > dist:
                dist = tempdist
        return dist

    def get_center(self):
        """Returns the scene's center."""
        return self.position
        # Use the center of figures as the scene's center. Currently not working.
        #(minx, minx_figure, maxx, maxx_figure,
        #    miny, miny_figure, maxy, maxy_figure,
        #    minz, minz_figure, maxz, maxz_figure) = self.get_extreme_figures()
        #return [(minx + maxx) / 2, (miny + maxy) / 2, (minz + maxz) / 2]

    def draw(self):
        """Draws the entire scene."""
        # Clear all buffers and matrices.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        # Set the perspective
        self.set_perspective()

        # Set the point of view
        self.set_camera()

        # Draw every figure, one by one
        for figure in self.figures:
            figure.draw()

    def get_figure_at(self, x, y):
        """Returns the nearest figure located at the given
        x and y screen coordinates."""
        # Set the current OpenGL mode as selection.
        glSelectBuffer(128)
        glRenderMode(GL_SELECT)

        # Reset the matrices
        self.reset_matrices()

        # Set the picking matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPickMatrix(x, y, 3, 3, glGetIntegerv(GL_VIEWPORT))

        # Initialize the names matrix
        glInitNames()
        glPushName(0)

        # Draw the scene
        self.draw()
        glFlush()

        # Set the mode back to rendering and obtain the hits
        hits = glRenderMode(GL_RENDER)

        # Find the corresponding figure and return it
        if len(hits) > 0:
            for figure in self.figures:
                if figure.id == hits[0]["names"][0]:
                    return figure

        # No figure found...
        return None

    def get_coords_at(self, x, y, figure):
        """Returns a (x, y, z) tuple with scene coordinates of the given x and y
        screen coordinates. If figure is supplied, its screen depth is used."""
        if figure == None or figure == self:
            win_z = 0.5
        else:
            win_z = figure.get_win_coords()[2]
        return gluUnProject(x, y, win_z)

    def get_win_coords(self):
        """Returns the projected coordinates of the scene's center."""
        return gluProject(self.position[0], self.position[1], self.position[2])

    def select(self, figure):
        """Selects a different figure.
        Removes the current selection if figure is None."""
        if self.selected_figure != None:
            self.selected_figure.select(False)
        if figure != None:
            figure.select(True)
        self.selected_figure = figure

    def highlight(self, figure):
        """Highlights a different figure.
        Removes the current mark if figure is None."""
        if self.highlighted_figure != None:
            self.highlighted_figure.highlight(False)
        if figure != None:
            figure.highlight(True)
        self.highlighted_figure = figure

    def add(self, figure):
        """Adds a figure to the scene."""
        self.figures.append(figure)

    def remove(self, figure):
        """Removes a figure from the scene."""
        self.figures.remove(figure)

        # If the figure was selected, de-select it.
        if self.selected_figure == figure:
            self.select(None)

    def move(self, x, y, z):
        """Pans temporarily the scene, relative to its current position in space."""
        self.position = map(add, self.position_perm, [x, y, z])
        self.camera_position = map(add, self.camera_position_perm, [x, y, z])

    def move_end(self):
        """Permanently applies the scene translation."""
        self.position_perm = self.position
        self.camera_position_perm = self.camera_position

    def rotate(self, angle, x, y, z):
        """Rotates temporarily the scene relative to its current rotation."""
        angle *= -200 # Scene has a lower sensibility than figures.
                      # Negative because we're moving the camera, not the scene.
        # Update the rotation matrix.
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glRotatef(angle, x, y, z)
        self.rotation_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

        # Update the camera position.
        scene_to_camera = map(sub, self.camera_position_perm, self.position)
        scene_to_camera = mult_vector_matrix(scene_to_camera, self.rotation_matrix)
        self.camera_position = map(add, scene_to_camera, self.position)

        # Update the up vector.
        self.up = mult_vector_matrix(self.up_perm, self.rotation_matrix)

    def rotate_end(self):
        """Permanently applies the scene rotation."""
        self.rotation_matrix_perm = self.rotation_matrix
        self.camera_position_perm = self.camera_position
        self.up_perm = self.up

    def scale(self, increment):
        """Zooms temporarily the scene."""
        self.zoom_angle = self.zoom_perm -increment
        if self.zoom_angle < 1:
            self.zoom_angle = 1
        elif self.zoom_angle > 180:
            self.zoom_angle = 180

    def scale_end(self):
        """Permanently applies the scene zoom."""
        self.zoom_perm = self.zoom_angle

    def show_all(self):
        """Repositions the camera so that all figures are visible."""
        if len(self.figures) == 0:
            return

        (minx, minx_figure, maxx, maxx_figure,
            miny, miny_figure, maxy, maxy_figure,
            minz, minz_figure, maxz, maxz_figure) = self. get_extreme_figures()

        # Reposition the scene and the camera.
        self.rotation_matrix_perm = get_identity_matrix()
        self.camera_far = max(100.0, maxz + maxz_figure.size)
        zpos_offset = minz - minz_figure.size
        self.position[0] = (minx + maxx) / 2
        self.position[1] = (miny + maxy) / 2
        self.position[2] = zpos_offset + ((self.camera_near + self.camera_far) / 2)
        self.camera_position[0] = self.position[0]
        self.camera_position[1] = self.position[1]
        self.camera_position[2] = zpos_offset - self.camera_near
        self.camera_position_perm = self.camera_position
        self.position_perm = self.position
        self.up = [0.0, 1.0, 0.0]
        self.up_perm = self.up

        # Find the farthest object from the new center.
        farthest_dist = self.position[0] - minx
        farthest_pos = [minx_figure.position[0] - minx_figure.size, minx_figure.position[1], minx_figure.position[2]]
        if (self.position[1] - miny) > farthest_dist:
            farthest_dist = self.position[1] - miny
            farthest_pos = [miny_figure.position[0], miny_figure.position[1] - minx_figure.size, miny_figure.position[2]]
        if (maxx - self.position[0]) > farthest_dist:
            farthest_dist = maxx - self.position[0]
            farthest_pos = [maxx_figure.position[0] + minx_figure.size, maxx_figure.position[1], maxx_figure.position[2]]
        if (maxy - self.position[1]) > farthest_dist:
            farthest_dist = maxy - self.position[1]
            farthest_pos = [maxy_figure.position[0], maxy_figure.position[1] + miny_figure.size, maxy_figure.position[2]]

        # Calculate the vectors which determine the viewing angle.
        eye_to_scene = map(sub, self.position, self.camera_position)
        eye_to_obj = map(sub, farthest_pos, self.camera_position)

        # Calculate the new angle.
        e2s_module = vector_module(eye_to_scene)
        e2o_module = vector_module(eye_to_obj)
        sp = scalar_product(eye_to_scene, eye_to_obj)
        angle_cosine = sp / (e2s_module * e2o_module)
        self.zoom_angle = 2 * math.degrees(math.acos(angle_cosine % 1))
        self.zoom_perm = self.zoom_angle

    def reset_matrices(self):
        """Resets the projection and modelview matrices."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_camera(self):
        """Positions the camera"""
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(self.camera_position[0], self.camera_position[1], self.camera_position[2],
                  self.position[0], self.position[1], self.position[2],
                  self.up[0], self.up[1], self.up[2])

    def set_perspective(self):
        """Calculates the new perspective according to given width and height"""
        glMatrixMode(GL_PROJECTION)
        gluPerspective(self.zoom_angle, float(self.width) / float(self.height),
                       self.camera_near, self.camera_far)

    def set_height(self, height):
        """Sets the height"""
        self.height = height

    def set_width(self, width):
        """Sets the width"""
        self.width = width

    def get_extreme_figures(self):
        """Finds the figures positioned in the extremes of the scene.
        Returns a 12-element tuple in the following format:
        (minx, minx_figure, maxx, maxx_figure,
        miny, miny_figure, maxy, maxy_figure,
        minz, minz_figure, maxz, maxz_figure)"""
        minx = None
        maxx = None
        miny = None
        maxy = None
        minz = None
        maxz = None
        for figure in self.figures:
            if (figure.position[0] - figure.size < minx) or (minx == None):
                minx = figure.position[0] - figure.size
                minx_figure = figure
            if (figure.position[0] + figure.size > maxx) or (maxx == None):
                maxx = figure.position[0] + figure.size
                maxx_figure = figure
            if (figure.position[1] - figure.size < miny) or (miny == None):
                miny = figure.position[1] - figure.size
                miny_figure = figure
            if (figure.position[1] + figure.size > maxy) or (maxy == None):
                maxy = figure.position[1] + figure.size
                maxy_figure = figure
            if (figure.position[2] - figure.size < minz) or (minz == None):
                minz = figure.position[2] - figure.size
                minz_figure = figure
            if (figure.position[2] + figure.size > maxz) or (maxz == None):
                maxz = figure.position[2] + figure.size
                maxz_figure = figure

        return (minx, minx_figure, maxx, maxx_figure,
                miny, miny_figure, maxy, maxy_figure,
                minz, minz_figure, maxz, maxz_figure)
__author__ = 'salas'
