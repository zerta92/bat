# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import adafruit_am2320

# create the I2C shared bus
i2c = board.I2C()  # uses board.SCL and board.SDA
am = adafruit_am2320.AM2320(i2c)

def get_temp_reading():
    temperature = am.temperature*(9/5)+32
    return temperature

def get_humi_reading():
    humidity = am.relative_humidity
    return humidity

# Uncomment this to run temp2.py
# while True:
#     print("Temperature: ", am.temperature*(9/5)+32)
#     print("Humidity: ", am.relative_humidity)
#     time.sleep(2)
