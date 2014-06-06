import math

from OpenGL.GL import *
from OpenGL.GLU import *


def get_identity_matrix():
    """Returns a 4x4 identity matrix."""
    return [[1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]]

def vector_to_matrix(vector):
    """Returns a 4x4 matrix equivalent to the given 3-element vector."""
    return [[vector[0], vector[1], vector[2], 0.0],
            [0.0,       0.0,       0.0,       0.0],
            [0.0,       0.0,       0.0,       0.0],
            [0.0,       0.0,       0.0,       0.0]]

def matrix_to_vector(matrix):
    """Returns a 3-element vector based on the first elements of the given 4x4 matrix."""
    return [matrix[0][0], matrix[0][1], matrix[0][2]]

def mult_vector_matrix(vector, matrix):
    """Returns the result of a vector-matrix multiplication."""
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadMatrixf(matrix)
    glMultMatrixf(vector_to_matrix(vector))
    result = glGetFloatv(GL_MODELVIEW_MATRIX)
    glPopMatrix()
    return matrix_to_vector(result)

def vector_module(vector):
    """Returns the module (norm) of a vector."""
    sum = 0
    for i in vector:
        sum += (i * i)
    return math.sqrt(sum)

def normalize(vector):
    """Normalizes a vector."""
    module = vector_module(vector)
    result = []
    for i in vector:
        result.append(i / module)
    return result

def scalar_product(vector1, vector2):
    if len(vector1) != len(vector2):
        return 0
    sum = 0
    for i in range(0, len(vector1)):
        sum += (vector1[i] * vector2[i])
    return sum