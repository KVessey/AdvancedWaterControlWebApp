# db_setup.py
 
import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship, backref

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# We will add classes here
class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(250), nullable=False)
    restart_time = Column(String(250))
    last_watered = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'restart_time': self.restart_time,
            'last_watered': self.restart_time,
            'id': self.id,
        }


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(250), nullable=False)
    water_needed = Column(String(250), nullable=False)
    last_watered = Column(String(250))
    plant_type = Column(String(250), nullable=False)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", backref=backref(
        "plants", order_by=id), lazy=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'water_needed': self.water_needed,
            'last_watered': self.last_watered,
            'plant_type': self.plant_type,
            'id': self.id,
        }


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
