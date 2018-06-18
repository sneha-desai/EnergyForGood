from data.solar_by_region_API import api_call

class House: 
    def __init__(self, location, num_of_panels, num_of_batteries):
        self.num_of_panels = num_of_panels
        self.constant_caps = {
            "solar": api_call(location), # Note this is an array
            "wind": 0.5,
            "fossil fuel": 100000, 
            "battery": 10 
        }

        self.house_resource_capacity = {
            "solar": self.solar_multiplier(self.constant_caps["solar"]),
            "wind": self.constant_caps["wind"],
            "fossil fuel": self.constant_caps["fossil fuel"],
            "battery": self.constant_caps["battery"]*num_of_batteries
        }

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

        self.energy_demand = [7.0, 8.0, 6.0, 7.0]

    def solar_multiplier(self, array):
        # array = []
        # for key in d:
        #     array.append(int(d[key]*0.15*(self.num_of_panels*1.6)))
        array = [int(x * 0.15*(self.num_of_panels*1.6)) for x in array]
        return array

    def get_caps(self):
        return self.house_resource_capacity

    # def get_resource_price(self):
    #     return self.resource_price

    # def get_init_price(self):
    #     return self.resource_init_price
    #
    # def set_init_price(self):
    #     self.resource_init_price[self.]

    def get_demand(self):
        return self.energy_demand

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



