# https://projects.raspberrypi.org/en/projects/robotPID/3

import sys
sys.path.insert(0,'/home/pi/pmcs')


from water2 import get_reading, GPIO, PIN, setup, destroy
from time import sleep

DUTY_CYCLE = 10
SAMPLETIME = 1

TARGET = 50
KP = 1#0.0002
KD =0#0.0019
KI = 0#0.005
e1_prev_error = 0
e1_sum_error = 0

counter = 0
humidity_new = 1.0
time_on = 0


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
   
    

def start(humidity_new, e1_sum_error, e1_prev_error, counter, time_on):
    while True:
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

        print('----------- {}'.format(counter))
        setRelayStatus(time_on, counter)
        counter +=1
        sleep(SAMPLETIME)
        e1_prev_error = humidity_error
        e1_sum_error += humidity_error


if __name__ == '__main__':
    setup()
    try:
        start(humidity_new, e1_sum_error, e1_prev_error, counter, time_on)
    except KeyboardInterrupt:
        destroy()