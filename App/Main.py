from MongoDBFunctions import *
from WeatherAPI import *
from MyEnergyAPI import *
from IndoorData import *
import configparser
import threading
import time

MAX_THREADS = 4

def getInfoEveryFiveMinutes():
    
    # get energy status from my energy hub
    #get_energy_status(cfgP['serial_number'], cfgP['key_myEnergy'])

    # get weather data for better overall data
    weather_dict = get_weather(cfgW['api_key'], cfgW['latitude'], cfgW['longitude'])

    # get indoor data from pods and the room
    greenhouse_dict = getIndoorData()

    # upload data to mongodb
    uploadData(cfgR['name'], cfgM['username'], cfgM['password'], cfgM['database_name'], "analyticsData", weather_dict, greenhouse_dict)


def timer_thread():
    thread_number = 1
    while True:
        if threading.active_count() - 1 < MAX_THREADS:  # Subtract 1 to exclude the timer thread
            threading.Thread(target=getInfoEveryFiveMinutes).start()
            thread_number += 1
        time.sleep(300)


if __name__ == "__main__":
    print("Starting App...")
    # get keys and firebase access
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    print(config.sections())
    cfgW = config['WEATHER']
    cfgM = config['MONGODB']
    cfgP = config['PV']
    cfgR = config['RASPI']

    threading.Thread(target=timer_thread).start()
    
