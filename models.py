# models.py
 
from app import db

class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)
    restart_time = db.Column(db.String)

    def __init__(self, name, restart_time):
        """"""
        self.name = name
        self.restart_time = restart_time

class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)
    water_needed = db.Column(db.String)
    last_watered = db.Column(db.String)

    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    device = db.relationship("Device", backref=db.backref(
        "plants", order_by=id), lazy=True)

    def __init__(self, name, water_needed, last_watered):
        """"""
        self.name = name
        self.water_needed = water_needed
        self.last_watered = last_watered
