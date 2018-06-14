from data.resources import *

class EnergyProducer(object):
    def __init__(self, type, s_cap):
        self.type = type
        self.unit_price = resource_price[type]
        self.init_price = resource_init_price[type]
        self.capacity = resource_capacity_func(type, s_cap)

    def production_cost(self, quantity):
        return self.unit_price * quantity

    def output(self, energy_required, weather):
        if self.type == "solar":
            energy_produced = self.capacity * weather

        elif self.type == "wind":
            energy_produced = self.capacity * weather

        else:
            # fossil fuels makes exactly the amount needed
            energy_produced = energy_required

        energy_produced = min(energy_required, energy_produced)

#     def output(self, quantity):
#         energy_produced = min(quantity, self.capacity)
#         if (self.capacity > energy_produced):
#             energy_leftover = energy_produced - self.capacity
#             return energy_produced, energy_leftover
#         else:
#             return energy_produced, 0

    def output_2(self, quantity, coverage=1):
        energy_produced = min(quantity, self.capacity*coverage)
        return energy_produced

    def get_init_price(self):
        return self.init_price

    def set_init_price(self, val):
        self.init_price = val
        return self.init_price

    def truncate(self, quantity):
        quantity = max(0, quantity)
        return min(self.capacity, quantity)
