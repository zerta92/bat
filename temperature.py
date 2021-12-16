import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import math
GAIN = 1;
PIN = 11;

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.IN)
    time.sleep(0.1)

def get_reading(pin=PIN):
    return 

# def turn_pump_on():
#     GPIO.output(PIN, GPIO.HIGH)

# def turn_pump_off():
#     GPIO.output(PIN, GPIO.LOW)

# This has been replaced by humidity_pid.py
values = [0]*100
def loop():
    while True:
        input_value = GPIO.input(PIN)
        print(str(input_value))
    # while True:
    #     for i in range(100):
    #         values[i] = adc.read_adc(1, gain = GAIN)
    #     humidity = round(-.009*max(values) + 206.4)
    #     print(humidity)
    #     #print(max(values)) prints nonconverted soil humidity
    #     #print(PIN) prints out pin7 which connects to the relay controlling the pump
    #     if (humidity)<10:
    #         GPIO.output(PIN, GPIO.HIGH)
    #         print("ON")
    #         time.sleep(0.1)
    #     else:
    #         GPIO.output(PIN, GPIO.LOW)
    #         print("OFF")
    #         time.sleep(0.1)
            
def destroy():
    # GPIO.output(PIN, GPIO.HIGH)
    GPIO.cleanup()
    
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        
            