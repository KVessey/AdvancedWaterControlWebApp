from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Plant, Device
import psutil
import datetime
import water
import os

app = Flask(__name__, static_url_path='/static')

# Connect to Database and create database session
engine = create_engine('sqlite:///database.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# TEMPLATES
def template(title="Advanced Water Control Web App", text=""):
    now = datetime.datetime.now()
    timeString = now
    templateData = {
        'title': title,
        'time': timeString,
        'text': text
    }
    return templateData


def serverStatusTemplate(title="Advanced Water Control Web App", text=""):
    now = datetime.datetime.now()
    timeString = now
    restartTime = restart_time
    templateData = {
        'title': title,
        'time': timeString,
        'restart_time': restartTime,
        'text': text
    }
    return templateData
# END TEMPLATES


# Landing Page Route
@app.route("/")
def home():
    templateData = template()
    plants = session.query(Plant).all()
    devices = session.query(Device).all()
    return render_template('index.html', **templateData, plants=plants, devices=devices)


# API Documentation Page 
@app.route('/api_documentation')
def api_documentation():
    devices = session.query(Device).all()
    return render_template('/apiDocumentation.html', devices=devices)


# Device Configuration
@app.route('/device_configuration')
def device_configuration():
    devices = session.query(Device).all()
    return render_template('devices/deviceConfiguration.html', devices=devices)


@app.route('/devices/new/', methods=['GET', 'POST'])
def newDevice():
    if request.method == 'POST':
        newDevice = Device(name=request.form['name'],
                         ip_address=request.form['ip_address'],
                         restart_time=request.form['restart_time'],
                         last_watered=request.form['last_watered'])
        session.add(newDevice)
        session.commit()
        return redirect(url_for('device_configuration'))
    else:
        return render_template('devices/new_device.html')


@app.route("/devices/<int:device_id>/edit/", methods=['GET', 'POST'])
def editDevice(device_id):
    editedDevice = session.query(Device).filter_by(id=device_id).one()
    if request.method == 'POST':
        editedDevice.name = request.form['name']
        editedDevice.ip_address=request.form['ip_address'],
        editedDevice.restart_time = request.form['restart_time']
        editedDevice.last_watered = request.form['last_watered']
        session.add(editedDevice)
        session.commit()
        return redirect(url_for('device_configuration'))
    else:
        return render_template('devices/edit_device.html', device=editedDevice)


@app.route('/devices/<int:device_id>/delete/', methods=['GET', 'POST'])
def deleteDevice(device_id):
    deviceToDelete = session.query(Device).filter_by(id=device_id).one()
    if request.method == 'POST':
        session.delete(deviceToDelete)
        session.commit()
        return redirect(url_for('device_configuration', device_id = device_id))
    else:
        return render_template('devices/delete_device.html', device = deviceToDelete)



# Plant Configuration
@app.route('/plant_configuration')
def plant_configuration():
    plants = session.query(Plant).all()
    devices = session.query(Device).all()
    return render_template('plants/plantConfiguration.html', plants=plants, devices=devices)


@app.route('/plants/new/', methods=['GET', 'POST'])
def newPlant():
    devices = session.query(Device).all()
    if request.method == 'POST':
        newPlant = Plant(name=request.form['name'],
                         water_needed=request.form['water_needed'],
                         last_watered=request.form['last_watered'],
                         plant_type=request.form['plant_type'],
                         device_id=request.form['device_id'])
        session.add(newPlant)
        session.commit()
        return redirect(url_for('plant_configuration'))
    else:
        return render_template('plants/new_plant.html', devices=devices)


@app.route("/plants/<int:plant_id>/edit/", methods=['GET', 'POST'])
def editPlant(plant_id):
    devices = session.query(Device).all()
    editedPlant = session.query(Plant).filter_by(id=plant_id).one()
    if request.method == 'POST':
        editedPlant.name = request.form['name']
        editedPlant.water_needed = request.form['water_needed']
        editedPlant.last_watered = request.form['last_watered']
        editedPlant.plant_type = request.form['plant_type']
        editedPlant.device_id = request.form['device_id']        
        session.add(editedPlant)
        session.commit()
        return redirect(url_for('plant_configuration'))
    else:
        return render_template('plants/edit_plant.html', plant=editedPlant, devices=devices)


@app.route('/plants/<int:plant_id>/delete/', methods=['GET', 'POST'])
def deletePlant(plant_id):
    devices = session.query(Device).all()
    plantToDelete = session.query(Plant).filter_by(id=plant_id).one()
    if request.method == 'POST':
        session.delete(plantToDelete)
        session.commit()
        return redirect(url_for('plant_configuration', plant_id=plant_id))
    else:
        return render_template('plants/delete_plant.html', plant=plantToDelete, devices=devices)


"""
BEGIN api functions for plant database
"""


def get_plants():
    plants = session.query(Plant).all()
    return jsonify(plants=[p.serialize for p in plants])


def get_plant(plant_id):
    plants = session.query(Plant).filter_by(id=plant_id).one()
    return jsonify(plants=plants.serialize)


def makeANewPlant(name, water_needed, last_watered, plant_type, device_id):
    addedPlant = Plant(name=name, water_needed=water_needed, last_watered=last_watered, plant_type=plant_type,
                       device_id=device_id)
    session.add(addedPlant)
    session.commit()
    return jsonify(Plant=addedPlant.serialize)


def updatePlant(id, name, water_needed, last_watered, plant_type, device_id):
    updatedPlant = session.query(Plant).filter_by(id=id).one()
    if not name:
        updatedPlant.name = name
    if not water_needed:
        updatedPlant.water_needed = water_needed
    if not last_watered:
        updatedPlant.last_watered = last_watered
    if not plant_type:
        updatedPlant.plant_type = plant_type
    if not device_id:
        updatedPlant.device_id = device_id
    session.add(updatedPlant)
    session.commit()
    return 'Updated a Plant with id %s' % id


def deleteAPlant(id):
    plantToDelete = session.query(Plant).filter_by(id=id).one()
    session.delete(plantToDelete)
    session.commit()
    return 'Removed Plant with id %s' % id


@app.route('/plantsApi', methods=['GET', 'POST'])
def plantsFunction():
    if request.method == 'GET':
        return get_plants()
    elif request.method == 'POST':
        name = request.args.get('name', '')
        water_needed = request.args.get('water_needed', '')
        last_watered = request.args.get('last_watered', '')
        plant_type = request.args.get('plant_type', '')
        device_id = request.args.get('device_id', '')
        return makeANewPlant(name, water_needed, last_watered, plant_type, device_id)


@app.route('/plantsApi/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def plantsFunctionId(id):
    if request.method == 'GET':
        return get_plant(id)

    elif request.method == 'PUT':
        name = request.args.get('name', '')
        water_needed = request.args.get('water_needed', '')
        last_watered = request.args.get('last_watered', '')
        plant_type = request.args.get('plant_type', '')
        device_id = request.args.get('device_id', '')
        return updatePlant(name, water_needed, last_watered, plant_type, device_id)

    elif request.method == 'DELETE':
        return deleteAPlant(id)


"""
END api functions for plant database
"""


@app.route('/server_status')
def server_status():
    serverStatus = serverStatusTemplate()
    devices = session.query(Device).all()
    return render_template('serverStatus.html', **serverStatus, devices=devices)


@app.route('/water_status')
def water_status():
    waterStatus = template()
    devices = session.query(Device).all()
    return render_template('waterStatus.html', **waterStatus, devices=devices)


@app.route('/alerts')
def alerts():
    devices = session.query(Device).all()
    return render_template('alerts.html', devices=devices)


@app.route('/reports')
def reports():
    devices = session.query(Device).all()
    return render_template('reports.html', devices=devices)


@app.route("/last_watered")
def check_last_watered():
    devices = session.query(Device).all()
    templateData = template(text="water.get_last_watered()")
    return render_template('waterStatus.html', **templateData)


@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text=message)
    return render_template('waterStatus.html', **templateData)


@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text="Watered Once")
    return render_template('waterStatus.html', **templateData)


@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text="Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text="Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python auto_water.py&")
    else:
        templateData = template(text="Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('waterStatus.html', **templateData)


if __name__ == "__main__":
    restart_time = datetime.datetime.now()
    # FOR HOME COMPUTER REMOTE CONNECTION
    #app.run(host='192.168.1.85', port=8090, debug=True, threaded=True)
    app.run(host='0.0.0.0',port=8090, debug=True)
