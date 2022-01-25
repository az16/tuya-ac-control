from tuya_iot import TuyaOpenAPI, AuthType
from requests import get
from info import keys
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
print(openapi.connect(USERNAME, PASSWORD))


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
    total_time = input("How long should this script control your HA device? (in minutes)")
    return total_time

def start_heating_phase():
    commands = {'commands': [{'code': 'switch', 'value': True}, {'code': 'mode', 'value': 'heat'}, {'code': 'set_temperature_c', 'value': '32'}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    return result 

def start_cooling_phase():
    commands = {'commands': [{'code': 'mode', 'value': 'cooling'}, {'code': 'set_temperature_c', 'value': '16'}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    return result 

def switch_on():
    commands = {'commands': [{'code': 'switch', 'value': True}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    return result 

def switch_off():
    commands = {'commands': [{'code': 'switch', 'value': False}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
    return result 

def current_temp():
    result = openapi.get(f"/v1.0/iot-03/devices/{MONZANA_ID}/status")
    return result 

def main_loop():

    total_time = get_params()
    max = 32 
    min = 16
    start_time = time.time()
    start_heating_phase()
    heating = True
    while (((time.time() - start_time)*60) <= total_time):
        time.sleep(60)
        if heating:
            if current_temp == max:
                start_cooling_phase()
                heating = False
        if not heating:
            if current_temp == min:
                switch_off() 
                break 