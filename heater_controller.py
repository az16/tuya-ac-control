from tuya_iot import TuyaOpenAPI, AuthType
from requests import get
from keys import keys_heater
import os
import time

PUBLIC_IP = get('https://api.ipify.org').text
keys = keys_heater
ACCESS_ID = keys[0]
ACCESS_KEY = keys[1]

# Endpoint as defined at https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
ENDPOINT = "https://openapi.tuyaeu.com"

USERNAME = keys[2]
PASSWORD = keys[3]

HEATER_ID = keys[4] # device ID


openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY, AuthType.CUSTOM)
reponse = openapi.connect(USERNAME, PASSWORD)

def get_params():
    """
    This function executes an input prompt, asking the user to specify the
    time in minutes that this script is supposed to be ran.

    Returns:
        result (string): The answer given to the input prompt.
    """
    total_time = input("How long should this script control your HA device? (in minutes)\r\n")
    print("Set timer to {0} min.".format(total_time))
    return total_time

def start_heating_phase(debug=False):
    """
    Sets the max temperature as the target temperature.

    Args:
        debug (bool, optional): Prints the TuyaCloud reponse if True. Defaults to False.

    Returns:
        result (json object): The Tuya Cloud reponse as a json object.
    """
    commands = {'commands': [{'code': 'temp_set', 'value': 35}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{HEATER_ID}/commands", commands)
    if debug:
        print(result)
    return result 

# def start_cooling_phase(debug=False):
#     """
#     Sets the min temperature as the target temperature.

#     Args:
#         debug (bool, optional): Prints the TuyaCloud reponse if True. Defaults to False.

#     Returns:
#         result (json object): The Tuya Cloud reponse as a json object.
#     """
#     commands = {'commands': [{'code': 'temp_set', 'value': 16}]}
#     result = openapi.post(f"/v1.0/iot-03/devices/{MONZANA_ID}/commands", commands)
#     if debug:
#         print(result)
#     return result 

def switch_on(debug=False):
    """
    Switches the device on if it is online but turned off.

    Args:
        debug (bool, optional): Prints the TuyaCloud reponse if True. Defaults to False.

    Returns:
        result (json object): The Tuya Cloud reponse as a json object.
    """
    commands = {'commands': [{'code': 'switch', 'value': True}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{HEATER_ID}/commands", commands)
    if debug:
        print(result)
    return result 

def switch_off(debug=False):
    """
    Switches the device off if it is online and turned on.

    Args:
        debug (bool, optional): Prints the TuyaCloud reponse if True. Defaults to False.

    Returns:
        result (json object): The Tuya Cloud reponse as a json object.
    """
    commands = {'commands': [{'code': 'switch', 'value': False}]}
    result = openapi.post(f"/v1.0/iot-03/devices/{HEATER_ID}/commands", commands)
    if debug:
        print(result)
    return result 

def current_temp(debug=False):
    """
    Fetches the current status and extracts the current temperature value from Tuya Cloud
    
    Args:
        debug (bool, optional): Prints the TuyaCloud reponse if True. Defaults to False.

    Returns:
        result (string): The current temperature found in the json response body.
    """
    result = openapi.get(f"/v1.0/iot-03/devices/{HEATER_ID}/status")["result"][2]["value"]
    if debug:
        print(result)
    return result 

def temp_status():
    """
    Meant for debugging. Only function is to format a easy to read string that 
    entails the current temperature

    Returns:
        (string): The formatted string that entails the current temperature
    """
    return print("Current temperature: {0}".format(current_temp()))

def main_loop():
    """
    This function defines the main structure and timing of heating and cooling 
    phases. All structural code goes here.
    """
    
    if reponse['success'] == True:
        print("Successfully connected to Tuya Open API.")
    else: 
        print("Connection to Tuya API failed. Shutting down..")
        os._exit(-1)

    total_time = 40.0

    start_time = time.time()
    
    switch_on(True)
    time.sleep(3) #wait for signal to be given
    
    #This loop assumes that the experiment starts with the lowest temperature (min) and 
    #first heats the room up to 32°C (max) and then reverses with a cooling phase back to
    #16 °C
    
    start_heating_phase(True)
    #temp_status()
    # heating = True
    # while (((time.time() - start_time)/60) <= total_time):
    #     time.sleep(30)
    #     temp_status()
    #     if heating:
    #         if current_temp(True) == max: #Finished heating phase? --> switch to cooling
    #             start_cooling_phase()
    #             heating = False
    #     if not heating:
    #         if current_temp(True) == min: #Finished cooling phase? --> switch off
    #             switch_off() 
    #             break 


if __name__ == "__main__":
    main_loop()