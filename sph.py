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
    sph_db = d_mongo.open_database('sph')
    list_projects = sph_db.collection_names()

    #################### Project windows #########################
    import app.gui.windows_list_projects as w_project
    project_name = w_project.ProjectWindows.get_project(list_projects)

    ################# Open project collection ###################
    project_col = sph_db[project_name]
    import app.solver.model.solver as s_sol
    if project_col.count() == 0:
        solve = s_sol.SphSolver()

