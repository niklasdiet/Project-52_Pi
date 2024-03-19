from MongoDBFunctions import *
from WeatherAPI import *
from Humidifier import *
import configparser


def getInfoEveryFiveMinutes():
    
    # get energy status from my energy hub
    #get_energy_status(cfgP['serial_number'], cfgP['key_myEnergy'])

    # get weather data for better overall data
    #weather_dict = get_weather(cfgW['api_key'], cfgW['latitude'], cfgW['longitude'])

    #client = connectToDB(cfgM['username'], cfgM['password'])

    # upload data to mongodb
    #uploadData(client, cfgM['database_name'], "sensorData", weather_dict)
    humidify()



def timer_thread():
    print("Starting Threads...")
    while True:
        getInfoEveryFiveMinutes()


if __name__ == "__main__":
    print("Starting App...")
    # get keys
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgW = config['WEATHER']
    cfgM = config['MONGODB']
    cfgP = config['PV']

    threading.Thread(target=timer_thread).start()
    