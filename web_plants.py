from flask import Flask, render_template, redirect, url_for, jsonify, Response
import psutil
import datetime
import water
import water2
import os
import cv2
import picamera
import time
from templates.camstream import takePic

# vc = cv2.VideoCapture(0) 


app = Flask(__name__)

def template(title = "PMSC", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/camera")
def cameraPage():
    templateData = template()
    return render_template('camera.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
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
    #templateData = template(text = reading)
    #return render_template('main.html', **templateData)
    humidity = -.009*reading + 206.4
    templateData = {'text' : humidity}
    return jsonify(templateData), 200

@app.route("/water")
def action2():
    water.pump_on()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)

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
            os.system("python3.4 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

def gen(): 
   """Video streaming generator function.""" 
   while True: 
        takePic()
    #    rval, frame = vc.read() 
    #    cv2.imwrite('pic.jpg', frame) 
        yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpeg', 'rb').read() + b'\r\n') 

@app.route('/video_feed') 
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)