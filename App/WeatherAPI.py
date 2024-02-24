import requests
import time

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
       
        # Calculate the duration of daylight (for PV efficiency)
        daylight_minutes = (current_weather['sunset'] - current_weather['sunrise']) / 60

        data = {"timestamp": int(time.time() * 1000),
                "temperature": current_weather['temp'],
                "humidity": current_weather['humidity'],
                "pressure": current_weather['pressure'],
                "daylight_minutes_outside": daylight_minutes,
                "weather": current_weather['weather'][0]['main'],
                "weather_icon": current_weather['weather'][0]['icon'],
                }
        return data

    except Exception as e:
        print(f"Error fetching weather information: {e}")
    return {}