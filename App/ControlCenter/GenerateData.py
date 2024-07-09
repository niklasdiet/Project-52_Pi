import random
import requests
from datetime import datetime, time

'''Main function to generate data for the tests'''
def testDataMain(latitude, longitude, api_key):
    generatedData = testDataGenerateData(latitude, longitude, api_key)
    return generatedData

'''Add up all the data that is generated'''
def testDataGenerateData(latitude, longitude, api_key):
    current_time = {"date": datetime.now()}
    weatherData = getWeather(latitude, longitude, api_key)
    roomData = testDataRoom(weatherData["humidityOutside"], weatherData["temperatureOutside"], weatherData["pressureOutside"])
    waterData = testDataWaterCycle()
    heatData = testDataHeatpump()
    #pvData = testDataPV(area, weatherData["uvi"])
    productionData = testDataProduction()
    allData = current_time | weatherData | roomData | waterData | heatData | productionData #| pvData
    return allData

'''Generate data for the water cycle'''
def testDataWaterCycle():
    # generate data for the water cycle. In one of 1000 cases the water cycle will fail. So the data is not generated
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"waterBufferTankLevel": 0, "flowrate": 0, "waterTemperature": 0, "powerConsumption": 0}
    else:
        waterLevel = random.uniform(49.0, 54.5)
        flowrate = generate_random_number()
        watertemperature = random.uniform(15.0, 15.9)
        powerConsumption = random.uniform(0.1, 0.2)
        return {"waterBufferTankLevel": waterLevel, "flowrate": flowrate, "waterTemperature": watertemperature, "powerConsumption": powerConsumption}

'''Generate data for the heat pump'''
def testDataHeatpump():
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"temperatureInput": 0, "powerConsumption": 0, "temperatureOutput": 0}
    else:
        temperatureInput = random.uniform(22.0, 24.0)
        temperatureOutput = random.uniform(19.0, 26.0)
        waterFlow = generate_random_number()
        powerConsumption = (50 - (temperatureInput + temperatureOutput) + random.uniform(0.1, 0.5))/30
        return {"temperatureInput": temperatureInput, "powerConsumption": powerConsumption, "temperatureOutput": temperatureOutput, "waterFlow": waterFlow}

'''Generate data for the room'''
def testDataRoom(humidity, temperature, airPressure):
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"airPressure": 0, "humidity": 0, "temperature": 0}
    else:
        airPressureGenerated = airPressure + random.uniform(-0.3, 0.3)
        humidityGenerated = 100 - ((55-(humidity/10)) + random.uniform(0.1, 1.0))
        temperatureGenerated = 15.0 + (((temperature - 15.0)/10.0)  + random.uniform(-0.2, 0.2))
        return {"airPressure": airPressureGenerated, "humidity": humidityGenerated, "temperature": temperatureGenerated}
    
'''Generate data for the light room'''
def testDataLightRoom():
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"lightIntensity": 0}
    else:
        lightIntensity = random.randint(0, 100)
        return {"lightIntensity": lightIntensity}

'''Generate data for the substrate production'''
def testSubstrateProduction():
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"oldSubstrate": 0, "newSubstrate": 0}
    else:
        oldSubstrate = random.randint(0, 100)
        newSubstrate = random.randint(0, 100)
        return {"oldSubstrate": oldSubstrate, "newSubstrate": newSubstrate}

'''Generate data for the mushroom output'''    
def testMushroomOutput():
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"oldMushrooms": 0, "newMushrooms": 0}
    else:
        oldMushrooms = random.randint(0, 100)
        newMushrooms = random.randint(0, 100)
        return {"oldMushrooms": oldMushrooms, "newMushrooms": newMushrooms}
    
'''Generate data for the units in production'''
def testDataProduction():
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"oldUnits": 0, "newUnits": 0}
    else:
        oldUnits = random.randint(0, 100)
        newUnits = random.randint(0, 100)
        return {"oldUnits": oldUnits, "newUnits": newUnits}

'''Generate data for the PV system'''
def testDataPV(area, uvi):
    ghi = uvi + 3
    fail = random.randint(0, 1000)
    if fail == 1000:
        return {"powerProduced": 0}
    else:
        power = 0.2 * ghi * area
        return {"powerProduced": power}

'''Function to add the new units to the old units'''
def unitsInProduction(new_units, date, old_units):
    allUnits = old_units+new_units
    add_units = {"date": date, "units": allUnits}
    return add_units

'''Function to generate a random number with a probability distribution'''
def generate_random_number():
    probabilities = [0.89, 0.1, 0.01]
    return random.choices([100, 98, 0], weights=probabilities)[0]

'''Function to generate the chat data'''
def chatGptGeneratedData():
    return {"chatGpt": "Hello, how can I help you?"}

'''Function to get the weather data from the OpenWeatherMap API'''
def getWeather(lat, lon, api_key, units='metric', exclude='minutely,hourly,daily'):
    
    base_url = "https://api.openweathermap.org/data/3.0/onecall" # Base URL for the OpenWeatherMap API
    url = f"{base_url}?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}&units={units}" # Building the complete API URL

    try:
        response = requests.get(url)
        data = response.json()

        daylight_minutes = (data['current']['sunset'] - data['current']['sunrise']) / 60

        data = {"temperatureOutside": data['current']['temp'],
                "humidityOutside": data['current']['humidity'],
                "pressureOutside": data['current']['pressure'],
                "uvi": data['current']['uvi'],
                "daylightMinutesOutside": daylight_minutes,
                }
        return data

    except Exception as e:
        print(f"Error fetching weather information: {e}")
    return {}