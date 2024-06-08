from flask import Flask, render_template, redirect, url_for, jsonify, Response
import psutil
import datetime
import os
# from templates.camstream import takePic
import water2
import temp2
import lcd



app = Flask(__name__)

def template(title = "PMCS", text=""):
    go_to_pmcs()
    now = datetime.datetime.now()
    timeString = str(now.hour)+':'+str(now.minute)
    with open('control/last_watered.txt') as f:
        last_watered = f.read()
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : last_watered
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

# @app.route("/temp2")
# def displayTemp():
#     temperature = temp2.get_temp_reading
#     templateData = {'text' : temperature}
#     return jsonify(templateData), 200

# def displayHumi():
#     humidity = temp2.get_humi_reading
#     templateData = {'text' : humidity}
#     return jsonify(templateData), 200

@app.route("/camera")
def cameraPage():
    templateData = template()
    return render_template('camera.html', **templateData)

@app.route("/lcd")
def turn_on_LCD():
    templateData = template(text = lcd.displayTempHumi())
    return render_template('main.html', **templateData)


@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water2.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def action():
    status = water.get_status() 
    message = ""
    if (status == 1):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/humidity_sensor_reading")
def get_reading():
    reading = water2.get_reading()
    humidity = -.009*reading + 206.4
    return jsonify({'soil_hum' : humidity}), 200

# @app.route("/get_humidity_target_reading")
# def get_humidity_target_reading():
#     target_humidity = water2.get_target_humidity_reading()
#     return jsonify({'target_soil_hum' : target_humidity}), 200


@app.route("/get_temperature")
def get_temp_reading():
    reading = temp2.get_temp_reading()
    temperature = reading
 #temp var is to cross communicate using jsonifi
    return jsonify({'temp' : temperature}), 200

@app.route("/get_humidity")
def get_humi_reading():
    reading = temp2.get_humi_reading()
    humidity = reading
    return jsonify({'hum' : humidity}), 200

@app.route("/water")
def action2():
    water2.pump_on()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)

def go_to_control():
    current_path = os.getcwd()
    if current_path == "/home/pi/pmcs":
        os.chdir('control')

def go_to_pmcs():
    current_path = os.getcwd()
    if current_path != "/home/pi/pmcs":
        os.chdir('..')

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    go_to_control()
    running = False
    message = ''
    if toggle == "ON":
        go_to_control()
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'humidity_pid.py':
                    running = True
                    message = "Already running"
            except:
                pass
        if not running:
            go_to_control()
            os.system("python3 humidity_pid.py&")
            message='ON'
            running = True
    else:
        go_to_control()
        message = 'OFF'
        os.system("sudo pkill -f humidity_pid.py")

    return jsonify({'auto_water_status':running, 'message':message})

# def gen(): 
#    """Video streaming generator function.""" 
#    while True: 
#         takePic()
#         yield (b'--frame\r\n' 
#               b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpeg', 'rb').read() + b'\r\n') 

# @app.route('/video_feed') 
# def video_feed(): 
#    """Video streaming route. Put this in the src attribute of an img tag.""" 
#    return Response(gen(), 
#                    mimetype='multipart/x-mixed-replace; boundary=frame') 

if __name__ == "__main__":
    # os.system("python3 lcd.py&") #load lcd program
    app.run(host='0.0.0.0', port=80, debug=True)