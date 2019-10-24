from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import water
import os
from app import app
from db_setup import init_db

init_db()


def template(title = "Advanced Water Control Web App", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def home():
    templateData = template()
    return render_template('index.html', **templateData)

@app.route('/plant_configuration')
def plant_configuration():
    return render_template('plantConfiguration.html')

@app.route('/server_status')
def server_status():
    serverStatus = template()
    return render_template('serverStatus.html', **serverStatus)

@app.route('/water_status')
def water_status():
    waterStatus = template()
    return render_template('waterStatus.html', **waterStatus)\

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')\

@app.route('/reports')
def reports():
    return render_template('reports.html')\





@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = "water.get_last_watered()")
    return render_template('waterStatus.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status()
    message = ""
    if (status == 1):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('waterStatus.html', **templateData)

@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Watered Once")
    return render_template('waterStatus.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('waterStatus.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)
