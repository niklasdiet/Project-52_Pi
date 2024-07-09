from MongoDBFunctions import *
#from WeatherAPI import *
#from Humidifier import *
import configparser


#def getInfoEveryFiveMinutes():
    
    # get energy status from my energy hub
    #get_energy_status(cfgP['serial_number'], cfgP['key_myEnergy'])

    # get weather data for better overall data
    #weather_dict = get_weather(cfgW['api_key'], cfgW['latitude'], cfgW['longitude'])

    #

    # upload data to mongodb
    #uploadData(client, cfgM['database_name'], "sensorData", weather_dict)
    #humidify()


if __name__ == "__main__":
    print("Starting App...")
    # get keys
    config = configparser.ConfigParser()
    config.read('Keys.cfg')
    cfgW = config['WEATHER']
    cfgM = config['MONGODB']
    cfgP = config['PV']
    #while True:
    #    getInfoEveryFiveMinutes()
    #    time.sleep(300)
    
    client = connectToDB(cfgM['username'], cfgM['password'])
    downloadAllImages(client, "Project52", "imageData")
    #download_image_from_mongodb(client, "661820f2b7110fc1fea3f453", "Project52", "Image14.jpg")
    client.close()
