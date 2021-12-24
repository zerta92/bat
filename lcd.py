# from decimal import Decimal
# import RPi.GPIO as GPIO
# import PCF8591 as ADC
import math
import time
import LCD1602 as LCD
from temp2 import get_temp_reading , get_humi_reading


def setup():
    LCD.init(0x27, 1)  # init(slave address, background light)


def loop():
    while True:
        temp = get_temp_reading()  # read temperature sensor value
        temp = round(temp, 1)
        humidity = get_humi_reading()  # read temperature sensor value
        LCD.write(0, 0, 'Temp: {} F'.format(temp))  # write to top row and farthest left column of LCD
        LCD.write(0, 1, 'Humidity: {} %'.format(humidity))  # write to top row and farthest left column of LCD
        time.sleep(1)  # update every second

# if __name__ == '__main__':
try:
    setup()
    loop()
except KeyboardInterrupt:
    pass