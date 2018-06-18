class EnergyProducer(object):
    def __init__(self, type, capacity):
        self.type = type
        self.capacity = capacity

        self.resource_init_price = {
            "solar": 20000, # $
            "wind": 800,
            "fossil fuel": 0, # $
            "battery": 3000
        }

    # To implement months, output will need time as a parameter
    def output(self, quantity, coverage=1):
        if self.type == "solar":
            energy_produced = min(quantity, self.capacity[0]*coverage)
        elif self.type == "wind":
            energy_produced = min(quantity, self.capacity[0] * coverage)
        else: 
            energy_produced = min(quantity, self.capacity*coverage)
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
        self.resource_init_price[self.type] = val
