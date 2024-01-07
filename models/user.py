#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if (kwargs):
            pwd = kwargs.get("password")
            kwargs["password"] = hashlib.md5(bytes(pwd, 'utf-8')).hexdigest()
        if (args):
            l_args = list(args)
            l_args[1] = hashlib.md5(bytes(args[1], 'utf-8')).hexdigest()
            args = tuple(l_args)
        super().__init__(*args, **kwargs)
