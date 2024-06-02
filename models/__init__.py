#!/usr/bin/python3
import os
"""This module instantiates an object of class FileStorage"""

from models.state import State
from os import getenv
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.place import Place
from models.engine.db_storage import DBStorage
from models.engine.file_storage important FileStorage

storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
