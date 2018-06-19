from data.regional_resources import solar_api_call, wind_api_call

class House: 
    def __init__(self, location, num_of_panels, num_of_turbines, num_of_batteries):

        self.num_resource = {
            "solar": num_of_panels,
            "wind": num_of_turbines,
            "fossil fuel": 1,
            "battery": num_of_batteries
        }

        self.single_resource_capacity = {
            "solar": self.solar_multiplier(solar_api_call(location)),  # Note this is an array
            "wind": wind_api_call(location),
            "fossil fuel": 100000, 
            "battery": 10
        }

        self.energy_demand = [7.0, 8.0, 6.0, 7.0]

    def solar_multiplier(self, array):
        array = [float(x * 0.15 * 1.6) for x in array]
        return array

    def get_caps(self, resource_type):
        return self.single_resource_capacity[resource_type]

    def get_nums(self, resource_type):
        return self.num_resource[resource_type]

    def get_demand(self):
        return self.energy_demand

    # def get_resource_price(self):
    #     return self.resource_price

    # def get_init_price(self):
    #     return self.resource_init_price
    #
    # def set_init_price(self):
    #     self.resource_init_price[self.]

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


        # self.resource_price = {
        #     "solar": 0.10, # $/kWh,
        #     "wind": 0.16, # $/kWh,
        #     "fossil fuel": 0.05, # $/kWh
        #     "battery": 0.00
        # }
        #
        # self.resource_init_price = {
        #     "solar": 20000, # $
        #     "wind": 800,
        #     "fossil fuel": 0, # $
        #     "battery": 3000
        # }



