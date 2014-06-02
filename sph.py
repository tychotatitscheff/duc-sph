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
    import app.solver.model.fluid as s_flu
    import app.gui
    import app.save.mongo as mongo
    import app.save.json as d_json

    db = mongo.create_database('SPH')
    # pas encore testé
    # L'utilisateur veut créer un nouveau projet
    nom_project = "jean-claude"  # come from gui
    project = mongo.create_collection(nom_project, db)
    nombre_d_itération = 8  # come from gui
    for i in range(0, nombre_d_itération):
        state = mongo.create_collection('State ' + str(i), project)
        group_fluid = mongo.create_collection('fluid', state)
        number_of_fluid = 1  # come from gui
        for j in range(0, number_of_fluid):
            fluid = [s_flu.Fluid(1, 2, 3, 4, 5, 6, 7)]  # come from gui
            pickled_fluid = d_json.json_encode(fluid[j])
            mongo.create_document(pickled_fluid, group_fluid)
        group_particle = mongo.create_collection('particle', state)
        number_of_particle = 4  # come from gui
        for j in range(0, number_of_particle):
            particle = ["Classe particle", "a", "e", "32"]  # come from gui
            pickled_particle = d_json.json_encode(particle[j])
            mongo.create_document(pickled_particle, group_particle)
        acc_structural = "classe structure"  # come from gui²
        pickled_acc_structural = d_json.json_encode(acc_structural)
        mongo.create_document(pickled_acc_structural, state)
    geometrie = "classe geometrie"  # come from gui
    pickled_geometrie = d_json.json_encode(geometrie)
    mongo.create_document(pickled_geometrie, project)
    meta_data = "classe meta data"  # come from gui²
    pickled_meta_data = d_json.json_encode(meta_data)
    mongo.create_document(pickled_meta_data, project)

