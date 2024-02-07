
import board
import busio
import smbus
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#import RPi.GPIO as GPIO


    
sensor1_ads = initialize_sensor()






def initialize_sensor(scl=board.SCL, sda=board.SDA):
    i2c = busio.I2C(scl, sda)
    device = I2CDevice(i2c, sensor_i2c_address)
    print(device)
    # access sparkfun isl29125 sensor