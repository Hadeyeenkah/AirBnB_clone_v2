#!/usr/bin/python3
"""New engine storage"""
from sqlalchemy import (create_engine, orm)
from models.base_model import Base, BaseModel
import os
from models.city import City
from models.state import State


class DBStorage:
    """engine storage class"""
    __engine = None
    __session = None
    cities = orm.relationship("City", cascade="all, delete", backref='state')

    def __init__(self):
        """class initialization method"""
        string = 'mysql+mysqldb://{}:{}@{}/{}'
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        database = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(string.format(user, password, host, database, pool_pre_ping=True))
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        dictionary = {}
        if cls:
            objects = self.__session.query(cls).all()
            key = f"{obj.__class__.__name__}.{obj.id}"
            dictionary[key] = obj
        elif not cls:
            determinant = [Place, Review, User, State, City, Amenity]
            for classing in determinant:
                dict_session = self.__session.query(classing).all()
                for values in dict_session:
                    new_key = f"{values.__class__.__name__}, {values.id}"
                    dictionary[new_key] = values
        return dictionary

        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            dictionary[key] = obj
        return dictionary

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = orm.scoped_session(orm.sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()