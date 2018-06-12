from EnergyProducer.resources import * #resource_capacity, resource_price, resource_init_price


class EnergyProducer(object):
    def __init__(self, type, s_cap):
        self.type = type
        #print(type)
        #print(location)
        self.unit_price = resource_price[type]
        self.init_price = resource_init_price[type]
        self.capacity = resource_capacity(type, s_cap)

    def production_cost(self, quantity):
        return self.unit_price * quantity

    def output(self, energy_required, weather):
        if self.type == "solar":
            # CHANGE!!!!! this should be a formula of amount of energy produced depending on weather
            energy_produced = self.capacity * weather

        elif self.type == "wind":
            # CHANGE!!!!!
            energy_produced = self.capacity * weather

        else:
            # fossil fuels makes exactly the amount needed
            energy_produced = energy_required

        energy_produced = min(energy_required, energy_produced)

        if energy_produced > energy_required:
            energy_leftover = energy_produced - energy_required
            return energy_produced, energy_leftover
        else:
            return energy_produced, 0
