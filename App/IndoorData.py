import board
from busio import I2C
import adafruit_bme680


def getIndoorData():

        # Create library object using our Bus I2C port
    i2c = I2C(board.SCL, board.SDA)
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

    # change this to match the location's pressure (hPa) at sea level
    #bme680.sea_level_pressure = 1013.25

    # You will usually have to add an offset to account for the temperature of
    # the sensor. This is usually around 5 degrees but varies by use. Use a
    # separate temperature sensor to calibrate this one.
    #temperature_offset = -5


    temperature_inside = getTemperatureInside(bme680)
    ground_humidity = 0
    gas = 0
    air_humidity_inside = getAirHumidityInside(bme680)
    air_pressure_inside = getAirPressureInside(bme680)
    light = 0
    water = 0
    water_temperature = 0
    water_level = 0
    dict = {"temperature_inside" : temperature_inside, "ground_humidity": ground_humidity, "gas": gas, "air_humidity_inside": air_humidity_inside, "air_pressure_inside": air_pressure_inside, "light": light, "water": water, "water_temperature": water_temperature, "water_level": water_level}
    return dict

# get info from sensors of the pi and the BME680 Breakout Board
def getTemperatureInside(bme680):
    temperature_offset = 0
    return bme680.temperature + temperature_offset
    
def getGroundHumidity(bme680):
    return bme680.gas

def getAirHumidityInside(bme680):
    return bme680.relative_humidity


def getAirPressureInside(bme680):
    return bme680.pressure

def getAltitudeInside(bme680):
    return bme680.altitude
