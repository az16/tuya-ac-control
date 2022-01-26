from tuya_iot import TuyaOpenAPI, AuthType
from requests import get
from keys import keys
import os
import time

PUBLIC_IP = get('https://api.ipify.org').text

ACCESS_ID = keys[0]
ACCESS_KEY = keys[1]

# For more info: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
ENDPOINT = "https://openapi.tuyaeu.com"

USERNAME = keys[2]
PASSWORD = keys[3]

MONZANA_ID = keys[4]


openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, AuthType.CUSTOM)
reponse = openapi.connect(USERNAME, PASSWORD)


# def get_weather():
# 	location_url = f'/v1.0/iot-03/locations/ip?ip={PUBLIC_IP}'
# 	location = openapi.get(location_url)['result']
# 	lat, lon = location['latitude'], location['longitude']

# 	weather_url = f"/v2.0/iot-03/weather/current?lat={lat}&lon={lon}"
# 	weather = openapi.get(weather_url)['result']['current_weather']['temp']
# 	return weather


# commands = {'commands': [{'code': 'colour_data', 'value': color}]}
# result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
# print(result)


# x = input('Press enter to brew')
# commands = {'commands': [{'code': 'switch', 'value': True}]}
# result = openapi.post(f"/v1.0/iot-03/devices/{FINGERBOT_DEVICE_ID}/commands", commands)
# print(result)

def get_params():
    total_time = input("How long should this script control your HA device? (in minutes)\r\n")
    print("Set timer to {0} min.".format(total_time))
    return total_time

def start_heating_phase(debug=False):
    commands = {'commands': [{'code': 'temp_set', 'value': 32}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    if debug:
        print(result)
    return result 

def start_cooling_phase(debug=False):
    commands = {'commands': [{'code': 'temp_set', 'value': 16}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    if debug:
        print(result)
    return result 

def switch_on(debug=False):
    commands = {'commands': [{'code': 'switch', 'value': True}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    if debug:
        print(result)
    return result 

def switch_off(debug=False):
    commands = {'commands': [{'code': 'switch', 'value': False}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    if debug:
        print(result)
    return result 

def current_temp(debug=False):
    result = openapi.get(f"/v1.0/iot-03/devices/{MONZANA_ID}/status")["result"][2]["value"]
    if debug:
        print(result)
    return result 

def temp_status():
    return print("Current temperature: {0}".format(current_temp()))

def main_loop():
    if reponse['success'] == True:
        print("Successfully connected to Tuya Open API.")
    else: 
        print("Connection to Tuya API failed. Shutting down..")
        os._exit(-1)

    total_time = 40.0
    #total_time = float(get_params())
    #print(total_time)
    max = 32 
    min = 16
    start_time = time.time()
    #switch_on(True)
    time.sleep(3)
    start_heating_phase(True)
    temp_status()
    heating = True
    while (((time.time() - start_time)/60) <= total_time):
        time.sleep(30)
        temp_status()
        if heating:
            if current_temp(True) == max:
                start_cooling_phase()
                heating = False
        if not heating:
            if current_temp(True) == min:
                switch_off() 
                break 


if __name__ == "__main__":
    main_loop()