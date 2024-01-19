from board import SCL, SDA
from busio import I2C
import adafruit_bme680
import RPi.GPIO as GPIO


def getIndoorData():

    bme680 = createLibrary()

    temperature_inside = getTemperatureInside(bme680)
    moisture = getMoisture(17)
    gas = 0
    air_humidity_inside = getAirHumidityInside(bme680)
    air_pressure_inside = getAirPressureInside(bme680)
    light = 0
    water = 0
    water_temperature = 0
    water_level = 0
    altitude = getAltitudeInside(bme680)
    
    dict = {"altitude": altitude, "temperature_inside": temperature_inside, "moisture": moisture, "gas": gas, "air_humidity_inside": air_humidity_inside, "air_pressure_inside": air_pressure_inside, "light": light, "water": water, "water_temperature": water_temperature, "water_level": water_level}
    print("Data: ", dict)
    return dict

def createLibrary():
    # Create library object using our Bus I2C port
    i2c = I2C(SCL, SDA, frequency=100000)
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

    return bme680

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
#temperature_offset = -5
def getTemperatureInside(bme680, temperature_offset = 0):
    return bme680.temperature + temperature_offset
    
def getGroundHumidity(bme680):
    return bme680.gas

def getAirHumidityInside(bme680):
    return bme680.relative_humidity

def getAirPressureInside(bme680):
    return bme680.pressure

def getAltitudeInside(bme680):
    return bme680.altitude

def getMoisture(MOISTURE_SENSOR_PIN):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)
    moisture_level = GPIO.input(MOISTURE_SENSOR_PIN)
    GPIO.cleanup()  # Clean up GPIO configuration

    return moisture_level