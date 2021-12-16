# https://projects.raspberrypi.org/en/projects/robotPID/3

import sys
sys.path.insert(0,'/home/pi/pmcs')


from water2 import get_reading, GPIO, PIN, setup, destroy
from time import sleep
import datetime

DUTY_CYCLE = 2
SAMPLETIME = 1

TARGET = 50
KP = 1
KD =0#0.002
KI = 0#0.0003
e1_prev_error = 0
e1_sum_error = 0

counter = 0
humidity_new = 1.0
time_on = 0

global run 
run = False

def setLastWatered():
    now = datetime.datetime.now()
    timeString = str(now.hour)+':'+str(now.minute)
    with open('last_watered.txt', 'w') as f:
        last_watered_time = timeString
        f.write(last_watered_time+'\n')
        f.close()

def get_time_on(humidity_new, counter):
    percentage = max(min(humidity_new, 100),0)/100
    time_on = DUTY_CYCLE * percentage
    print("time on  {} ".format(time_on))
    print("counter  {} ".format(counter))
   
    return time_on 

def setRelayStatus(time_on, counter):
    if counter > time_on:
        GPIO.output(PIN, GPIO.LOW)
    if counter < time_on:
        GPIO.output(PIN, GPIO.HIGH)
        setLastWatered()
       

   
    

def start(humidity_new, e1_sum_error, e1_prev_error, counter, time_on):
    while run:
        raw = get_reading()
        humidity = -.009*raw + 206.4
        humidity_error = TARGET - humidity

        # print("humidity error {} ".format(humidity_error))
        # print("humidity e1_prev_error {} ".format(e1_sum_error))
        # print("humidity sum error {} ".format(e1_sum_error))

        humidity_new += (humidity_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
        if(counter >= DUTY_CYCLE or counter==0):
            print("humidity  {} ".format(humidity))
            print("humidity process var {} ".format(humidity_new))
            counter = 0
            time_on = get_time_on(humidity_new, counter)
            with open('data.txt', 'a') as f:
                textdata = str(humidity)
                f.write(textdata+'\n')
                f.close()

        print('----------- {}'.format(counter))
        setRelayStatus(time_on, counter)
        counter +=1
        sleep(SAMPLETIME)
        e1_prev_error = humidity_error
        e1_sum_error += humidity_error

def stop():
    global run 
    run= False
    destroy()

# if __name__ == '__main__':
def run_main():
    setup()
    try:
        global run
        run = True
        start(humidity_new, e1_sum_error, e1_prev_error, counter, time_on)
        return
    except KeyboardInterrupt:
        destroy()
run_main()