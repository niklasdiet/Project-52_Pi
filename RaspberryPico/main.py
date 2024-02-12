import network
import time
from machine import Pin, I2C, ADC
from bme680 import *
from umqtt.simple import MQTTClient
import ubinascii
import ujson


def check_internet_connection():
    wlan = network.WLAN(network.STA_IF)
    
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.active(True)
        wlan.connect(wifi_name, wifi_pw)

        timeout = 10  # Adjust the timeout as needed (in seconds)
        start_time = time.time()

        while not wlan.isconnected() and (time.time() - start_time) < timeout:
            time.sleep(1)

    if wlan.isconnected():
        print("Connected to WiFi")
        led_blinks(3)
        return True
    else:
        print("Failed to connect to WiFi")
        return False


def convert_to_percentage(value, min_value, max_value):
    if min_value == max_value:
        raise ValueError("min_value and max_value cannot be equal")

    if value < min_value:
        value = min_value
    elif value > max_value:
        value = max_value

    percentage = abs(100-((value - min_value) / (max_value - min_value)) * 100)
    return percentage

def led_blinks(cycles):
    led_onboard = Pin("LED", Pin.OUT)
    for _ in range(cycles):
        time.sleep(0.5)
        led_onboard.toggle()  # Turn on the LED
        time.sleep(0.5)
        led_onboard.toggle()  # Turn off the LED
 

def connect_MQTT():
     # Connect to MQTT broker
    mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_BROKER)
    mqtt_client.connect()
    print("Connected to MQTT broker")
    return mqtt_client

def load_config():
    try:
        with open('config.json', 'r') as file:
            config_data = ujson.load(file)
        return config_data
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

config = load_config()

MQTT_TOPIC = config.get("mqtt_topic")
MQTT_BROKER = config.get("mqtt_broker")
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())

#Calibraton values
dry = config.get("dry")
wet = config.get("wet")
temp_offset = config.get("temp_offset")
pressure = config.get("pressure")
pico_id = config.get("device_id")
wifi_name = config.get("wifi_name")
wifi_pw = config.get("wifi_pw")

if __name__ == "__main__":

    # Check the internet connection
    if check_internet_connection():
        print("Internet connection is active.")
    
    try:
    
        mqtt_client = connect_MQTT()
        
        # Access Sensors
        bme = BME680_I2C(I2C(1, sda=Pin(2), scl=Pin(3))) # BME680 Sensor reference
        soil = ADC(Pin(26)) # Soil moisture PIN reference

        counter = 0.0
        temp = 0.0
        tempRaw = 0.0
        pres = 0.0
        hum = 0.0
        gas = 0.0
        moist = 0.0
        moistRaw = 0.0
        
        while True:
            moisture = convert_to_percentage(soil.read_u16(), wet, dry)
            
            temp += bme.temperature + temp_offset
            tempRaw += bme.temperature
            pres += bme.pressure
            hum += bme.humidity
            gas += bme.gas
            moist += moisture
            moistRaw += soil.read_u16()

            if counter == 4:
                # Construct payload in the desired format
                sensor_data = {
                    "device_id": pico_id,
                    "temperature": temp/5,
                    "pressure": pres/5,
                    "humidity": hum/5,
                    "gas": gas/5,  # Add your gas reading logic here
                    "moisture": moist/5  # Add your moisture reading logic here
                }
                
                json_payload = ujson.dumps(sensor_data)
                
                # Publish sensor data to MQTT Broker
                mqtt_client.publish(MQTT_TOPIC, json_payload)
                
                counter = 0.0
                temp = 0.0
                tempRaw = 0.0
                pres = 0.0
                hum = 0.0
                gas = 0.0
                moist = 0.0
                moistRaw = 0.0
                
                led_blinks(1)
            else:
                counter += 1
                
            time.sleep(5)  # Adjust sleep time as needed
    except Exception as e:
        print(f"Failed: {e}")
