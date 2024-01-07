#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    def __init__(self, **kwargs):
        """initialize the child class"""
        BaseModel.__init__(self)
        BaseModel.__init__(self, **kwargs)

    __tablename__ = 'states'
    name = Column(String(128, collation='latin1_swedish_ci'), nullable=False)

    cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def cities(self):
        """defines the relationship between a state and its cities
        in File storage"""
        from models import storage
        related_cities = []
        file_cities = storage.all(City)
        for key, value in file_cities.items():
            if value.state_id == self.id:
                related_cities.append(value)
        return related_cities
