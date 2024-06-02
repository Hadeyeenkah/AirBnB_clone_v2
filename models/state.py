#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import String, Column, orm
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    arg1 = "state"
    arg2 = "all, delete-orphan"
    name = Column(String(128), nullable=False)
    cities = orm.relationship("City", backref=arg1, cascade=arg2)

    import models
    if models.engine_storage == "fs":
        def __init__(self, *args, **kwargs):
            """ State class initialization """
            self.name = kwargs['name']
            kwargs = {}
            super().__init__()

    if models.engine_storage != "db":
        @property
        def cities(self):
            """ function that returns the list of City instances
                with state_id equals to the current State.id
            """
            from models import storage
            important_list = []
            single_cities = storage.all(City).values()
            for single_city in single_cities:
                if self.id == city.state_id:
                    important_list.append(city)
            return important_list
