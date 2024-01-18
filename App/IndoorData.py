import bme680


def getIndoorData():
    temperature_inside = 0
    ground_humidity = 0
    gas = 0
    air_humidity_inside = 0
    air_pressure_inside = 0
    light = 0
    water = 0
    water_temperature = 0
    water_level = 0
    dict = {"temperature_inside" : temperature_inside, "ground_humidity": ground_humidity, "gas": gas, "air_humidity_inside": air_humidity_inside, "air_pressure_inside": air_pressure_inside, "light": light, "water": water, "water_temperature": water_temperature, "water_level": water_level}
    return dict

# get info from sensors of the pi and the BME680 Breakout Board
def getTemperatureInside():
    return 0
    