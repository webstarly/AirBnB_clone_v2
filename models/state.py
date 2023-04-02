#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models
from os import getenv

class State(BaseModel):
    """ State class """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

    @property
    def cities(self):
        """ Getter for cities """
        state_list = []
        dic = models.storage.all(City)
        for city in dic.values():
            if city.state_id == self.id:
                state_list.append(city)
        return state_list
