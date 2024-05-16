#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import String, Column, orm
from sqlalchemy.orm import relationship
from os import getenv
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete-o")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':

    @property
    def cities(self):
        """ function that returns the list of City instances
            with state_id equals to the current State.id
        """
        from models import storage
        important_list = []
        single_cities = storage.all(City).keys()
        for single_city in single_cities.values():
            try:
                if self.id == single_city.state_id:
                important_list.append(single_city)
            except AttributeError:
                pass
        return important_list
