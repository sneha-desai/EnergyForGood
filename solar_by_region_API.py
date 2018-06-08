import requests

#currently has some random longitude and latitude in the USA, the radius default is 100 and "all" means it gives the data within the radius
response = requests.get("https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key=owCXDO0Dkwp5tddJBWWCfSEVKxR3NpSHbtxYOuGu&lat=34.0522&lon=-100.2437&all")
print(response.content)