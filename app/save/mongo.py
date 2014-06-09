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

import pymongo
import requests
from mimetypes import MimeTypes
from pymongo import MongoClient
from gridfs import GridFS

client = MongoClient('localhost', 27017)
sph_db = client['sph']
fs = GridFS(sph_db)


def drop_database(name):
    for i in (0, client.database_names().count()):
        if client.database_names().index(i) is name:
            client.database_names().index(i).drop()


def open_collection(name):
    collection = sph_db[name]
    return collection


def insert_document(document, collection):
    collection.insert(document)


def insert_binary_document(binary, collection):
    m = MimeTypes()
    mime_type = m.guess_type(binary)
    doc = fs.put(binary, content_type=mime_type)
    collection.insert(doc)


