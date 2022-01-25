from tuya_iot import TuyaOpenAPI
from requests import get

PUBLIC_IP = get('https://api.ipify.org').text

ACCESS_ID = ''
ACCESS_KEY = ''

# For more info: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
ENDPOINT = "https://openapi.tuyaeu.com"

USERNAME = '4mykvqs8baeuryqcnuwa'
PASSWORD = 'e674d8a2317a4d8195a60d2e1d3407d0'

MONZANA_ID = '9be82f24b2effa137ctmgx'


openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.login(USERNAME, PASSWORD)


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