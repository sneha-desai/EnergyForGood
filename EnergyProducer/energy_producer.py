from EnergyProducer.resources import resource_capacity, resource_price

class EnergyProducer(object):
    def __init__(self, type):
        self.type = type
        self.unit_price = resource_price[type]
        self.capacity = resource_capacity[type]

    def production_cost(self, quantity, sun_coverage):
        if (sun_coverage):
    	    return self.unit_price*quantity*sun_coverage
        else:
            return self.unit_price*quantity

    def output(self, quantity):
        return min(quantity, self.capacity)