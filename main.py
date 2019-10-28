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


def template(title="Advanced Water Control Web App", text=""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title': title,
        'time': timeString,
        'text': text
    }
    return templateDate


@app.route("/")
def home():
    templateData = template()
    return render_template('index.html', **templateData)


@app.route('/plant_configuration')
def plant_configuration():
    plants = session.query(Plant).all()
    return render_template('plantConfiguration.html', plants=plants)


@app.route('/plants/new/', methods=['GET', 'POST'])
def newPlant():
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
        return render_template('new_plant.html')


# This will let us Update our plants and save it in our database
@app.route("/plants/<int:plant_id>/edit/", methods=['GET', 'POST'])
def editPlant(plant_id):
    editedPlant = session.query(Plant).filter_by(id=plant_id).one()
    if request.method == 'POST':
        # if request.form['name']:
            editedPlant.name = request.form['name']
            editedPlant.water_needed = request.form['water_needed']
            editedPlant.last_watered = request.form['last_watered']
            editedPlant.plant_type = request.form['plant_type']
            editedPlant.device_id = request.form['device_id']
            session.add(editedPlant)
            session.commit()
            return redirect(url_for('plant_configuration'))
    else:
        return render_template('edit_plant.html', plant=editedPlant)


# This will let us Delete our plant
@app.route('/plants/<int:plant_id>/delete/', methods=['GET', 'POST'])
def deletePlant(plant_id):
    plantToDelete = session.query(Plant).filter_by(id=plant_id).one()
    if request.method == 'POST':
        session.delete(plantToDelete)
        session.commit()
        return redirect(url_for('plant_configuration', plant_id=plant_id))
    else:
        return render_template('delete_plant.html', plant=plantToDelete)


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
    addedPlant = Plant(name=name, water_needed=water_needed, last_watered=last_watered, plant_type=plant_type, device_id=device_id)
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
    serverStatus = template()
    return render_template('serverStatus.html', **serverStatus)


@app.route('/water_status')
def water_status():
    waterStatus = template()
    return render_template('waterStatus.html', **waterStatus) \


@app.route('/alerts')
def alerts():
    return render_template('alerts.html') \


@app.route('/reports')
def reports():
    return render_template('reports.html') \


@app.route("/last_watered")
def check_last_watered():
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
    app.run(host='0.0.0.0', port=8090, debug=True)
