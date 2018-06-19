import numpy as np
import math
import copy

import data.weather as weather
# import data.resources as capacities
from model.producer import EnergyProducer 

class EnergyEnvironment:
    def __init__(self, house): 
        self.time_energy_requirement = house.get_demand()

        # solar
        self.solar_producer = EnergyProducer(house, "solar")
        self.solar_cost = 0
        self.solar_energy = 0 

        # wind
        self.wind_producer = EnergyProducer(house, "wind") 
        self.wind_cost = 0
        self.wind_energy = 0

        # grid
        self.grid_producer = EnergyProducer(house, "fossil fuel") 
        self.grid_cost = 0
        self.grid_energy = 0 

        self.battery = EnergyProducer(house, "battery") 
        self.battery_energy = 0
        self.battery_used = 0

        # other parameters
        self.reward = 0
        self.state = [0,0,0]
        # self.state = [0,0,0,0] # order = time, sun, wind

        self.solar_index = 0
        self.wind_index = 1
        self.ff_index = 2

        self.time_index = 0
        self.sun_coverage_index = 1
        self.wind_power_index = 2
        # self.month_index = 3

    def reset(self):
        # solar
        self.solar_cost = 0
        self.solar_energy = 0

        # wind
        self.wind_cost = 0
        self.wind_energy = 0

        # grid
        self.grid_cost = 0
        self.grid_energy = 0

        # battery
        self.battery_used = 0

        # reward
        self.reward = 0

    def get_next_state(self):
        self.state[self.time_index] = (self.state[self.time_index] + 1) % 4
        self.state[self.sun_coverage_index] = weather.get_sunlight()
        self.state[self.wind_power_index] = weather.get_wind_power()

    def reward_function(self, solar_energy_called, grid_energy_called, wind_energy_called, energy_demand,
                        grid_energy_produced,solar_energy_produced, wind_energy_produced, battery_used):
        output = grid_energy_produced + solar_energy_produced + wind_energy_produced + battery_used
        negative_reward = abs(solar_energy_called - solar_energy_produced) + \
                          abs(grid_energy_called - grid_energy_produced) + \
                          abs(wind_energy_called - wind_energy_produced) + \
                          abs(energy_demand - output)
        positive_reward = abs(solar_energy_produced) + abs(wind_energy_produced) + abs(battery_used)

        self.reward = positive_reward - negative_reward

    def step(self, action, state):
        self.reset()
        # initial_resource_price = self.solar_producer.get_init_price()
        # print("initial resource price:", initial_resource_price)
        # self.solar_producer.set_init_price(0)

        time = state[self.time_index]

        sun_coverage = float((state[self.sun_coverage_index])) / 2.0  # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer
        wind_power = float(state[self.wind_power_index]) / 2.0

        # no sun during the 1st and last time periods
        if time == 0 or time == 3:
            sun_coverage = 0

        energy_demand = self.time_energy_requirement[time]

        solar_energy_called = action[self.solar_index]
        grid_energy_called = action[self.ff_index]
        wind_energy_called = action[self.wind_index] * 0.1

        solar_energy_produced = self.solar_producer.output(solar_energy_called, sun_coverage)
        self.solar_energy = copy.deepcopy(solar_energy_produced)

        wind_energy_produced = self.wind_producer.output(wind_energy_called, wind_power)
        self.wind_energy = copy.deepcopy(wind_energy_produced)

        old_battery = self.battery_energy

        # if there is excess energy to store in battery
        if (self.solar_energy + self.wind_energy + self.battery_energy) > energy_demand:
            self.battery_energy = (self.solar_energy + self.wind_energy + self.battery_energy) - energy_demand
            if self.battery_energy < old_battery:
                self.battery_used = old_battery - self.battery_energy
            else:
                self.battery_used = 0

        # make sure battery energy isn't greater than amount of energy it can store
        self.battery_energy = self.battery.truncate(self.battery_energy)

        # calculate grid energy produced from grid energy call
        grid_energy_produced = self.grid_producer.output(grid_energy_called, 1)
        self.grid_energy= copy.deepcopy(grid_energy_produced)

        # get the reward
        self.reward_function(solar_energy_called, grid_energy_called, wind_energy_called, energy_demand, grid_energy_produced,
                               solar_energy_produced, wind_energy_produced, self.battery_used)

        self.get_next_state()

        return self.reward, self.state


