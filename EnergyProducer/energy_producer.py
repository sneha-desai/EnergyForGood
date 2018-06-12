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

    def output(self, quantity):
        energy_produced = min(quantity, self.capacity)
        if (self.capacity > quantity):
            energy_leftover = self.capacity - quantity
            return energy_produced, energy_leftover
        else:
            return energy_produced, 0