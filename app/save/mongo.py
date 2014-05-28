#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Clément Eberhardt," \
             "Clément Léost," \
             "Benoit Picq," \
             "Théo Subtil" \
             " and Tycho Tatitscheff"
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

from pymongo import MongoClient
client = MongoClient()


def create_database(nom):
    db = client[nom]
    return db


def check_database(name):
    print(name in client.database_names())


def drop_database(name):
    for i in (0, client.database_names().count()):
        if client.database_names().index(i) is name:
            client.database_names().index(i).drop()


def create_collection(name, database):
    collection = database[name]
    return collection


def create_document(document, collection):
    post_id = collection.insert(document)
    print(post_id)


