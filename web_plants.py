from flask import Flask, render_template, redirect, url_for, jsonify, Response
import psutil
import datetime
import water
import water2
import os
import cv2
import picamera
import time
import sys
# sys.path.insert(0,'/home/pi/pmcs/control')
# import humidity_pid

from templates.camstream import takePic

# vc = cv2.VideoCapture(0) 


app = Flask(__name__)

def template(title = "PMCS", auto_watering_status = "", text=""):
    go_to_pmcs()
    now = datetime.datetime.now()
    timeString = str(now.hour)+':'+str(now.minute)
    with open('control/last_watered.txt') as f:
        last_watered = f.read()
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : last_watered,
        'auto_watering_status': auto_watering_status
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
    humidity = -.009*reading + 206.4
    templateData = {'text' : humidity}
    return jsonify(templateData), 200

@app.route("/water")
def action2():
    water.pump_on()
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
    if toggle == "ON":
        templateData = template(auto_watering_status = "ON")
        go_to_control()
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'humidity_pid.py':
                    templateData = template(auto_watering_status = "Already running")
                    running = True
            except:
                pass
        if not running:
            go_to_control()
            os.system("python3 humidity_pid.py&")
    else:
        templateData = template(auto_watering_status = "OFF")
        go_to_control()
        os.system("sudo pkill -f humidity_pid.py")

    return render_template('main.html', **templateData)

# @app.route("/auto/water/<toggle>")
# def auto_water(toggle):
#     if toggle == "ON":
#         templateData = template(auto_watering_status = "Auto Watering On")
#         # try:
#         humidity_pid.run_main()

#         # except:
#         #     pass   

#     else:
#         templateData = template(auto_watering_status = "Auto Watering Off")
#         humidity_pid.stop()

#     print("deez nutz")
#     return render_template('main.html', **templateData)

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