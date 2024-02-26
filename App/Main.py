from MongoDBFunctions import *
from WeatherAPI import *
#from MyEnergyAPI import *
#from IndoorData import *
import configparser
import threading
import time

MAX_THREADS = 4

def getInfoEveryFiveMinutes():
    
    # get energy status from my energy hub
    #get_energy_status(cfgP['serial_number'], cfgP['key_myEnergy'])

    # get weather data for better overall data
    weather_dict = get_weather(cfgW['api_key'], cfgW['latitude'], cfgW['longitude'])


    client = connectToDB(cfgM['username'], cfgM['password'])
    upload_image_to_mongodb(client, "App/images/image.png", "Project52", "analyticsImages", "hub0001")
    # upload data to mongodb
    uploadData(client, cfgM['database_name'], "sensorData", weather_dict)


def timer_thread():
    print("Starting Threads...")
    thread_number = 1
    while True:
        if threading.active_count() - 1 < MAX_THREADS:  # Subtract 1 to exclude the timer thread
            current_time = time.localtime()
            current_minutes = current_time.tm_min

            # Check if the current minutes is at the end of 5 or 0
            if current_minutes % 5 == 0:
                threading.Thread(target=getInfoEveryFiveMinutes).start()
                thread_number += 1

        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    print("Starting App...")
    # get keys
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgW = config['WEATHER']
    cfgM = config['MONGODB']
    cfgP = config['PV']

    threading.Thread(target=timer_thread).start()
    