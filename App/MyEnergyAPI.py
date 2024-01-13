import requests
from requests.auth import HTTPDigestAuth

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