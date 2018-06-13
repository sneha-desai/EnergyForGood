from EnergyProducer.resources import resource_capacity, resource_price, resource_init_price

class EnergyProducer(object):
    def __init__(self, type):
        self.type = type
        self.unit_price = resource_price[type]
        self.init_price = resource_init_price[type]
        self.capacity = resource_capacity[type]

    def production_cost(self, quantity, sun_coverage):
        if (sun_coverage):
    	    return self.unit_price*quantity*sun_coverage
        else:
            return self.unit_price*quantity

    def output(self, quantity, sun_coverage):
        energy_produced = min(quantity, self.capacity)
        energy_produced = energy_produced*sun_coverage
        if (self.capacity > energy_produced):
            energy_leftover = energy_produced - self.capacity
            return energy_produced, energy_leftover
        else:
            return energy_produced, 0

    def get_init_price(self):
        return self.init_price

    def set_init_price(self, val):
        self.init_price = val
        return self.init_price

    def truncate(self, quantity):
        quantity = max(0, quantity)
        return min(self.capacity, quantity)
