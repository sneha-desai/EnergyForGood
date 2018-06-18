class EnergyProducer(object):
    def __init__(self, type, capacity):
        self.type = type
        self.capacity = capacity
        # self.unit_price = resource_price[type]
        # self.init_price = resource_init_price[type]

    # OLD output function
    # def output(self, energy_required, weather):
    #     if self.type == "solar":
    #         energy_produced = self.capacity[0] * weather

    #     elif self.type == "wind":
    #         energy_produced = self.capacity[0] * weather

    #     else:
    #         # fossil fuels makes exactly the amount needed
    #         energy_produced = energy_required

    #     energy_produced = min(energy_required, energy_produced)

    # To implement months, output will need time as a parameter
    #TODO: check if weather is getting passed like OLD output function
    def output(self, quantity, coverage=1):
        # Only need an if for solar because it is the only month dependent right now
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

    # def get_init_price(self):
    #     return self.init_price

    # def set_init_price(self, val):
    #     self.init_price = val
    #     return self.init_price
