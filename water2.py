import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import math
adc =Adafruit_ADS1x15.ADS1115(address = 0x48, busnum=1)
GAIN = 1;
PIN = 7;

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(0.1)

def get_reading(pin=PIN):
    return adc.read_adc(0, gain = GAIN)

values = [0]*100
def loop():
    while True:
        for i in range(100):
            values[i] = adc.read_adc(0, gain = GAIN)
        humidity = round(-.009*max(values) + 206.4)
        print(humidity)
        #print(max(values)) prints nonconverted soil humidity
        #print(PIN) prints out pin7 which connects to the relay controlling the pump
        if (humidity)<10:
            GPIO.output(PIN, GPIO.HIGH)
            print("ON")
            time.sleep(0.1)
        else:
            GPIO.output(PIN, GPIO.LOW)
            print("OFF")
            time.sleep(0.1)
            
def destroy():
    GPIO.output(PIN, GPIO.HIGH)
    GPIO.cleanup()
    
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        
            