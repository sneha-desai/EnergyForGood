import requests
import json

def solar_api_call(location):
    #input a US state for location and gives average (right now taking annual average but can be changed to monthly)
    #solar energy in kWh/m2/day area 
    solar_response = requests.get("https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=owCXDO0Dkwp5tddJBWWCfSEVKxR3NpSHbtxYOuGu&address={}" .format(location))
    solar_list = json.loads(solar_response.content)
    solar_obj = solar_list['outputs']['avg_lat_tilt']['monthly']
    # print(solar_obj)
    solar_dict = []
    for value in solar_obj.values():
        solar_dict.append(value)
    return solar_dict

def wind_api_call(location):
    if(location == 'California'):
        return [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4]
    else:
        return [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4]

# print(api_call("Delaware"))