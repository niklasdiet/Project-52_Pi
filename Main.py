import requests
from datetime import datetime
from requests.auth import HTTPDigestAuth
import firebase_admin
from firebase_admin import credentials, firestore
import configparser
import threading
import time

MAX_THREADS = 4
config = configparser.ConfigParser()

def initializeApp():
    # Initialize Firebase with the configuration file
    cred = credentials.Certificate("firebaseConfig.json")
    firebase_admin.initialize_app(cred)


def uploadData(collection_name, d1, d2 = {}, d3 = {}):
    data = d1 | d2 | d3
    # Get the Firestore database instance
    db = firestore.client()

    # Get the reference to the collection and upload the data
    collection_ref = db.collection(collection_name)
    collection_ref.add(data)



def get_weather(api_key, lat, lon, exclude='minutely,hourly', units='metric'):
    
    # Base URL for the OpenWeatherMap API
    base_url = "https://api.openweathermap.org/data/3.0/onecall"
    # Building the complete API URL
    url = f"{base_url}?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units={units}"

    try:
        # Making the API request
        response = requests.get(url)
        data = response.json()

        # Extracting relevant information from the response
        current_weather = data['current']
        sunrise_timestamp = current_weather['sunrise']
        sunset_timestamp = current_weather['sunset']
       
        # Calculate the duration of daylight (for PV efficiency)
        daylight_duration = sunset_timestamp - sunrise_timestamp
        daylight_minutes = daylight_duration / 60

        data = {"timestamp": datetime.now().timestamp(), "temperature_outside": current_weather['temp'], "air_humidity_outside": current_weather['humidity'], "air_pressure_air_outside": current_weather['pressure'], "daylight_minutes_outside": daylight_minutes, "weather": current_weather['weather'][0]['main'], "weather_icon": current_weather['weather'][0]['icon']}
        return data

    except Exception as e:
        print(f"Error fetching weather information: {e}")
    return {}


def get_energy_status(serial_number, key_myEnergy):
    url = 'https://director.myenergi.net/cgi-jstatus-H'    
    h = {'User-Agent': 'Wget/1.14 (linux-gnu)'}

    try:
        # Making the API request with additional headers
        response = requests.get(url, headers = h, auth=HTTPDigestAuth(serial_number, key_myEnergy), timeout=10)

        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")


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

def getInfoEverySecondMinute():
    # get energy status from my energy hub
    #get_energy_status(config['WEATHER']['serial_number'], config['WEATHER']['key_myEnergy'])

    # get weather data for better overall data
    weather_dict = get_weather(config['WEATHER']['api_key'], config['WEATHER']['latitude'], config['WEATHER']['longitude'])

    # get indoor data from pods and the room
    greenhouse_dict = getIndoorData()

    print(weather_dict)

    # upload data to firebase
    uploadData("analyticsData", weather_dict, greenhouse_dict)


def worker(thread_number):
    print(f"Thread {thread_number} started")
    getInfoEverySecondMinute()
    time.sleep(5)  # Simulating some work
    print(f"Thread {thread_number} completed")

def timer_thread():
    thread_number = 1
    while True:
        if threading.active_count() - 1 < MAX_THREADS:  # Subtract 1 to exclude the timer thread
            threading.Thread(target=worker, args=(thread_number,)).start()
            thread_number += 1
        time.sleep(120)






if __name__ == "__main__":
    # get keys and firebase access
    config.read('Keys.cfg')
    initializeApp()

    threading.Thread(target=timer_thread).start()
    
