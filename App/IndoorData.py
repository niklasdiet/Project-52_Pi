import board
import adafruit_bme680
import busio
import smbus
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#import RPi.GPIO as GPIO


def getIndoorData():

    SENSOR1_I2C_ADDRESS = 0x77

    SENSOR2_I2C_ADDRESS = 0x48
    
    sensor1_ads = initialize_sensor(SENSOR1_I2C_ADDRESS, "bme680")
    temperature_inside = getTemperatureInside(sensor1_ads)
    air_humidity_inside = getAirHumidityInside(sensor1_ads)
    air_pressure_inside = getAirPressureInside(sensor1_ads)


    sensor2_ads = initialize_sensor(SENSOR2_I2C_ADDRESS, "ads1115",board.SCL_1, board.SDA_1)
    moisture = getMoisture(sensor2_ads)

    gas = 0
    light = 0
    water = 0
    water_temperature = 0
    water_level = 0

    dict = {"temperature_inside": temperature_inside, "moisture": moisture, "gas": gas, "air_humidity_inside": air_humidity_inside, "air_pressure_inside": air_pressure_inside, "light": light, "water": water, "water_temperature": water_temperature, "water_level": water_level}
    print("Data: ", dict)
    return dict


# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
#temperature_offset = -5
def getTemperatureInside(bme680, temperature_offset = -15):
    return bme680.temperature + temperature_offset

def getAirHumidityInside(bme680):
    return bme680.relative_humidity

def getAirPressureInside(bme680):
    return bme680.pressure


def processMoistureData(data):
    zero_saturation = 0
    full_saturation = 32767

    moisture_level = abs((data-zero_saturation)/(full_saturation-zero_saturation))*100
    return moisture_level

def getMoisture(ads):
    channel = AnalogIn(ads, ADS.P0)

    # Read the analog input value
    raw_data = channel.value

    # Perform any necessary processing on the data
    moisture_level = processMoistureData(raw_data)
    print(f"Moisture: {moisture_level}%")

    return moisture_level



def initialize_sensor(sensor_i2c_address, sensor_type, scl=board.SCL, sda=board.SDA):
    i2c = busio.I2C(scl, sda)
    device = I2CDevice(i2c, sensor_i2c_address)
    print(device)
    if sensor_type == "bme680":
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=sensor_i2c_address)
        return bme680
    elif sensor_type == "ads1115":
        ads = ADS.ADS1115(i2c, address=sensor_i2c_address)
        ads.gain = 1
        return ads
    else:
        return None



