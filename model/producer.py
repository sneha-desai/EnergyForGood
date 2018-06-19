class EnergyProducer(object):
    def __init__(self, house, resource_type):
        self.resource_type = resource_type
        self.capacity = house.get_caps(resource_type)
        self.number = house.get_nums(resource_type)

        self.resource_init_price = {
            "solar": 20000, # $
            "wind": 800,
            "fossil fuel": 0, # $
            "battery": 3000
        }

    # To implement months, output will need time as a parameter
    def output(self, quantity, prob=1):
        if self.resource_type == "solar" or self.resource_type == "wind":
            energy_produced = min(quantity, self.capacity[0]*prob)*self.number
        else: 
            energy_produced = min(quantity, self.capacity*prob)*self.number
        return energy_produced

    def truncate(self, quantity):
        quantity = max(0, quantity)
        return min(self.capacity, quantity)

    ## Functions for calculating cost
    # def production_cost(self, quantity):
    #     return self.unit_price * quantity

    def get_init_price(self):
        return self.resource_init_price

    def set_init_price(self, val):
        self.resource_init_price[self.resource_type] = val
