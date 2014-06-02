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
    import app.solver.model.fluid
    import app.gui
    import app.save.mongo as d_mongo
    import app.save.json as d_json

    ############ Initialize connection to database ###############
    db = d_mongo.create_database('SPH')

    #################### Project windows #########################
    # TODO : show project windows

    ################ User create a new project ###################
    project_name = "test1"  # TODO : integrate with GUI
    project = d_mongo.create_collection(project_name, db)
    # TODO : add metadata (name, date)

    #################### Store initial data #####################

    iteration_number = 4  # TODO : integrate with GUI
    for i in range(0, iteration_number):
        state = d_mongo.create_collection('State ' + str(i), project)
        group_fluid = d_mongo.create_collection('fluid', state)

        fluid_number = 2  # TODO : integrate with solver
        for j in range(1, fluid_number):
            fluid = ""  # come from gui
            pickled_fluid = d_json.json_encode(fluid[j])
            d_mongo.create_document(pickled_fluid, group_fluid)
        group_particle = d_mongo.create_collection('particle', state)

        number_of_particle = 4  # TODO : integrate with solver
        for j in range(1, number_of_particle):
            particle = ""  # come from gui
            pickled_particle = d_json.json_encode(particle[j])
            d_mongo.create_document(pickled_particle, group_particle)
        acc_structural = ""  # come from gui²
        pickled_acc_structural = d_json.json_encode(acc_structural)
        d_mongo.create_document(pickled_acc_structural, state)

    geometrie = ""  # come from gui
    pickled_geometrie = json.json_encode(geometrie)
    mongo.create_document(pickled_geometrie, project)
    meta_data = ""  # come from gui²
    pickled_meta_data = json.json_encode(meta_data)
    mongo.create_document(pickled_meta_data, project)
            # en cours de production
