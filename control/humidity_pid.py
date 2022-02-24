# https://projects.raspberrypi.org/en/projects/robotPID/3

import sys
sys.path.insert(0,'/home/pi/pmcs')


from water2 import get_reading, GPIO, PIN, setup, destroy
from time import sleep
import datetime

#Constants
DUTY_CYCLE = 10 #Max length of time pump can be on
SAMPLETIME = 1
TARGET = 95
KP = 12
KD = 1
KI = 0.025
#PID variables
global e1_prev_error
e1_prev_error = 0
global e1_sum_error
e1_sum_error = 0
global humidity_control_variable #PID output
humidity_control_variable = 0.0 
global humidity_control_variable_previous #PID output of previous cycle
humidity_control_variable_previous = 0.0
global time_on #How long the pump will stay on
time_on = 0
global samples #Sample, taken every second 
samples = 0

global run 
run = False

def setLastWatered():
    now = datetime.datetime.now()
    timeString = str(now.month)+'/'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)
    with open('last_watered.txt', 'w') as f:
        last_watered_time = timeString
        f.write(last_watered_time+'\n')
        f.close()

def get_time_on(humidity_control_variable,humidity_control_variable_previous):
    #error if dividing by zero 
    if humidity_control_variable_previous == 0 or humidity_control_variable == 0:
        return 0 
    percent_diff = (humidity_control_variable - humidity_control_variable_previous )/ abs(humidity_control_variable_previous)
    print("percent_diff 1: {} ".format(percent_diff))
    if percent_diff <= 0 or percent_diff<.01:
        return 0
    percent_diff = max(min(percent_diff, 1),0)
    time_on = max(DUTY_CYCLE * percent_diff,1)#turn on at least minimum 1 second
    print("time on  {} ".format(time_on))
    print("percent_diff 2: {} ".format(percent_diff))

   
    return time_on 

global duty_cycle_counter
duty_cycle_counter = 0
def setRelayStatus(time_on):
    global duty_cycle_counter
    state = GPIO.input(PIN)
    while duty_cycle_counter < time_on:
        if not state:
            GPIO.output(PIN, GPIO.HIGH)
            setLastWatered()
        duty_cycle_counter += .1
        sleep(.1)
    GPIO.output(PIN, GPIO.LOW)
    duty_cycle_counter = 0

    # GPIO.output(PIN, GPIO.LOW)
    # if counter > time_on:
    #     GPIO.output(PIN, GPIO.LOW)
    # if counter < time_on:
    #     GPIO.output(PIN, GPIO.HIGH)
    #     setLastWatered()
       

def start():
    while run:
        global humidity_control_variable
        global humidity_control_variable_previous
        global e1_sum_error
        global e1_prev_error
        global time_on
        global samples
        samples += 1
        raw = get_reading()
        humidity = -.009*raw + 206.4
        humidity_error = TARGET - humidity
        humidity_control_variable_previous = humidity_control_variable
        humidity_control_variable += (humidity_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
        print("humidity  {} ".format(humidity))
        print("target humidity  {} ".format(TARGET))

        print("humidity_control_variable prev{} ".format(humidity_control_variable_previous))
        print("humidity control var {} ".format(humidity_control_variable))
        time_on = get_time_on(humidity_control_variable, humidity_control_variable_previous)
        with open('data.txt', 'a') as f:
            textdata = str(humidity)
            f.write(textdata+'\n')
            f.close()
 
        if samples > 5: # wait to cycle 5 times so we dont get a huge spike at the beginning (turns on 10 seconds if under target humidity)
            setRelayStatus(time_on)
  
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
        start()
        return
    except KeyboardInterrupt:
        destroy()
run_main()