import requests
import json

def api_call(location):

    #input a US state for location and gives average (right now taking annual average but can be changed to monthly)
    #solar energy in kWh/m2/day area 
    solar_response = requests.get("https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=owCXDO0Dkwp5tddJBWWCfSEVKxR3NpSHbtxYOuGu&address={}" .format(location))
    solar_list = json.loads(solar_response.content)
    return int(solar_list['outputs']['avg_dni']['annual']), solar_list['outputs']['avg_dni']['monthly']

#print(api_call("Delaware"))