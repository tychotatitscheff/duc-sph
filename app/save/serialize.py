__author__ = 'salas'

import jsonpickle
import app.solver.model.fluid as s_fl

A = s_fl.Fluid(1, 1, 1, 1, 1, 1, 1)
print(A)

json = jsonpickle.encode(A)
print(json)

B = jsonpickle.decode(json)
print(B)