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
    import sys

    ################## Create Main Application ###################
    import qdarkstyle
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    sph_app = QApplication(sys.argv)
    sph_app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

    ############ Initialize connection to database ###############
    import app.save.mongo as d_mongo
    sph_db = d_mongo.db
    list_projects = sph_db.collection_names(include_system_collections=False)

    #################### Project windows #########################
    import app.gui.windows_list_projects as w_list_projects
    project_name = w_list_projects.ProjectWindows.get_project(list_projects)

    ################# Open project collection ###################
    project_col = sph_db[project_name]

    ################## Create or open solver ####################
    import app.solver.model.solver as s_sol
    import jaraco.modb as d_jaraco
    if project_col.count() == 0:
        import app.gui.windows_create_project as g_create_project
        properties = g_create_project.CreateProjectWindows().get_properties()
        import app.solver.model.hash_table as s_hash
        hashing = s_hash.Hash(properties[2], properties[3])
        solve = s_sol.SphSolver(properties[0], properties[1], hashing)
        post = {'initial_state': d_jaraco.encode(solve)}
        project_col.insert(post)
        del solve, post
    for doc in project_col.find({'initial_state': {'$exists': True}}):
        solve = d_jaraco.decode(doc['initial_state'])
        print(solve)




