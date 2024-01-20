import board
import adafruit_bme680
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO


def getIndoorData():

    SENSOR1_I2C_ADDRESS = 0x77
    SENSOR2_I2C_ADDRESS = 0x48 
    SENSOR2_SDA_PIN = board.D27
    SENSOR2_SCL_PIN = board.D17

    bme680 = getBus()

    temperature_inside = getTemperatureInside(bme680)
    moisture = getMoisture(SENSOR2_I2C_ADDRESS, SENSOR2_SDA_PIN, SENSOR2_SCL_PIN)
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

def getBus():
    # Create library object using our Bus I2C port
    i2c = board.I2C()   # uses board.SCL and board.SDA
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

    return bme680

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
#temperature_offset = -5
def getTemperatureInside(bme680, temperature_offset = -5):
    return bme680.temperature + temperature_offset

def getAirHumidityInside(bme680):
    return bme680.relative_humidity

def getAirPressureInside(bme680):
    return bme680.pressure

def getAltitudeInside(bme680):
    return bme680.altitude

def processMoistureData(data):
    moisture_level = data * 100 / 32767
    return moisture_level

def getMoisture(sensor_i2c_address, sda_pin=None, scl_pin=None):
    try:
        # Create the I2C bus
        if sda_pin is None or scl_pin is None:
            i2c = busio.I2C(board.SCL, board.SDA)
        else:
            i2c = busio.I2C(scl_pin, sda_pin)

        ads = ADS.ADS1115(i2c, address=sensor_i2c_address)

        # Create an analog input channel on channel 0
        channel = AnalogIn(ads, ADS.P0)

        # Read the analog input value
        raw_data = channel.value

        # Perform any necessary processing on the data
        moisture_level = processMoistureData(raw_data)

        return moisture_level

    except Exception as e:
        print(f"Error: {e}")
        return None