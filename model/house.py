from data.regional_resources import solar_api_call, wind_api_call

class House: 
    def __init__(self, location, num_of_panels, num_of_turbines, num_of_batteries):
        self.num_of_panels = num_of_panels
        self.num_of_turbines = num_of_turbines

        self.constant_caps = {
            "solar": solar_api_call(location),  # Note this is an array
            "wind": wind_api_call(location),
            "fossil fuel": 100000, 
            "battery": 10 
        }

        self.house_resource_capacity = {
            "solar": self.solar_multiplier(self.constant_caps["solar"]),
            "wind": self.wind_multiplier(self.constant_caps["wind"]),
            "fossil fuel": self.constant_caps["fossil fuel"],
            "battery": self.constant_caps["battery"]*num_of_batteries
        }

        self.resource_price = {
            "solar": 0.10,  # $/kWh,
            "wind": 0.16,  # $/kWh,
            "fossil fuel": 0.05,  # $/kWh
            "battery": 0.00 
        }

        self.resource_init_price = {
            "solar": 20000,  # $
            "wind": 800,
            "fossil fuel": 0,  # $
            "battery": 3000
        }

    def solar_multiplier(self, array):
        array = [int(x * 0.15*(self.num_of_panels*1.6)) for x in array]
        return array

    def wind_multiplier(self, array):
        array = [(self.num_of_turbines * avg_wind_speed) for avg_wind_speed in array]
        return array

    def get_caps(self):
        return self.house_resource_capacity

    # def get_data_monthly(self, location, panels, batteries):
    #     solar_dict = api_call(location) #solar energy from api
    #     print(solar_dict)
    #     for key, value in solar_dict.items():
    #         solar_dict[key] = value*0.15*(panels*1.6)
    #         return solar_dict

    # def get_data(self, location, panels, batteries):
    #     solar_dict = api_call(location) #solar energy from api
    #     june_solar_cap = list(solar_dict.values())[5]
    #     battery_cap = resource_capacity["battery"]*batteries
    #     return june_solar_cap, battery_cap

# house = House('California', 30, 2)
# house.get_caps()

# def resource_capacity_func(thetype, s_cap):
#     if thetype == "solar": return s_cap # return api_call(location)
#     elif thetype == "wind": return s_cap
#     elif thetype == "fossil fuel": return 100000

# resource_capacity = {
#     "solar": api_call(location), # Daily capacity for a household solar farm in kWh
#     "fossil fuel": 100000,
#     "battery": 20 
# }