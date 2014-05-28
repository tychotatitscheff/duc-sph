#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Clément Eberhardt," \
             "Clément Léost," \
             "Benoit Picq," \
             "Théo Subtil" \
             "and Tycho Tatitscheff"
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


if __name__ == "__main__":
    import app.solver
    import app.gui
    import app.save.mongo as mongo
    import app.save.json as json

    db = mongo.create_database('SPH')
    # pas encore testé
    # L'utilisateur veut créer un nouveau projet
    nom_project = ""  # come from gui
    project = mongo.create_collection(nom_project, db)
    nombre_d_itération = ""  # come from gui
    for i in range(0, nombre_d_itération):
        state = mongo.create_collection('State ' + str(i), project)
        group_fluid = mongo.create_collection('fluid', state)
        number_of_fluid = ""  # come from gui
        for j in range(1, number_of_fluid):
            fluid = ""  # come from gui
            pickled_fluid = json.encode(fluid[j])
            mongo.create_document(pickled_fluid, group_fluid)
        group_particle = mongo.create_collection('particle', state)
        number_of_particle = ""  # come from gui
        for j in range(1, number_of_particle):
            particle = ""  # come from gui
            pickled_particle = json.encode(particle[j])
            mongo.create_document(pickled_particle, group_particle)
        acc_structural = ""  # come from gui²
        pickled_acc_structural = json.encode(acc_structural)
        mongo.create_document(pickled_acc_structural, state)
    geometrie = ""  # come from gui
    pickled_geometrie = json.json_encode(geometrie)
    mongo.create_document(pickled_geometrie, project)
    meta_data = ""  # come from gui²
    pickled_meta_data = json.json_encode(meta_data)
    mongo.create_document(pickled_meta_data, project)
            # en cours de production