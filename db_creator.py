from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    restart_time = Column(String)

    def __init__(self, name, restart_time):
        """"""
        self.name = name
        self.restart_time = restart_time


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    water_needed = Column(String)
    last_watered = Column(String)
    plant_type = Column(String)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", backref=backref(
        "plants", order_by=id), lazy=True)

    def __init__(self, name, water_needed, last_watered, plant_type):
        """"""
        self.name = name
        self.water_needed = water_needed
        self.last_watered = last_watered
        self.plant_type = plant_type


# create tables
Base.metadata.create_all(engine)