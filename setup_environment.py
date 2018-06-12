import numpy as np
import math
import copy
from weather import get_sunlight, get_wind_power

from EnergyProducer.energy_producer import EnergyProducer
class EngEnv:
    def __init__(self):
        self.time_energy_requirement = [
            7,
            8,
            6,
            7
        ]
        # solar
        self.solar_producer = EnergyProducer('solar')
        self.solar_cost = 0
        self.solar_energy = 0 

        # wind
        self.wind_producer = EnergyProducer('wind')
        self.wind_cost = 0
        self.wind_energy = 0

        # grid
        self.grid_producer = EnergyProducer('fossil fuel')
        self.grid_cost = 0
        self.grid_energy = 0 # how much energy has been produced from fossil fuel 

        # other parameters
        self.reward = 0
        self.state = [0, 0, 0, 0, 0, 0] # order = solar, wind, fossil fuel, time, sun, wind
        self.battery = 0

        self.solar_index = 0
        self.wind_index = 1
        self.ff_index = 2
        self.time_index = 3
        self.sun_coverage_index = 4
        self.wind_power_index = 5

    def reset(self):
        self.solar_cost = 0
        self.solar_energy = 0

        self.wind_cost = 0
        self.wind_energy = 0

        self.grid_cost = 0
        self.grid_energy = 0

    # def reward_base(self, renew_energy, ff_energy, battery, time_energy_requirement, time, renew_cost, ff_cost):
    #     if self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time]:
    #         reward = 1 
    #     else:
    #         reward = -1
        
    #     reward += 0.1*(self.reward_min_cost(renew_cost, ff_cost))
    #     return reward

    def reward_min_cost(self, solar_cost, wind_cost, ff_cost):
        cost = solar_cost + wind_cost + ff_cost
        if (cost > 0 and cost <= 10):
            reward = cost - ff_cost
        else:
            reward = -cost
        return reward

    def step(self, action, state):
        self.reset()

        # NOTE: state is in the form of [solar_switch, wind_switch, ff_switch, time, sun_coverage, wind_power]
        time = state[self.time_index]
        energy_req = self.time_energy_requirement[time]

        sun_coverage = (state[self.sun_coverage_index])/2 # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer
        wind_power = state[self.wind_power_index]/2

        if (action[self.solar_index] == 1):
            if (time == 2):
                self.solar_energy, self.battery = self.solar_producer.output(energy_req, sun_coverage)
                self.solar_cost = self.solar_producer.production_cost(self.solar_energy)
                energy_req -= self.solar_energy

        if (action[self.wind_index] == 1):
            self.wind_energy, self.battery = self.wind_producer.output(energy_req, wind_power)
            self.wind_cost = self.wind_producer.production_cost(self.wind_energy)

        if (self.battery > 0):
            # The case if there is more energy stored than required in this step
            self.batter -= energy_req

            if (self.battery >= energy_req):
                self.battery -= energy_req
                energy_req = 0
            else:
                energy_req -= self.battery
                self.battery -= self.battery

        if (action[self.ff_index] == 1):
            if (energy_req == 0):
                # Give some negative reward 
                print("Grid didn't need to be on")
            else:
                self.grid_energy, throwaway = self.grid_producer.output(energy_req, 0)
                self.grid_cost = self.grid_producer.production_cost(self.grid_energy)


        # TODO: implement negative reward if energy requirement is not met
        # if (energy_req > 0):
            # Give some negative reward 

        # reward = self.reward_base(self.renew_energy, self.ff_energy, self.battery, self.time_energy_requirement, time)
        reward = self.reward_min_cost(self.solar_cost, self.wind_cost, self.grid_cost)

        self.state[self.solar_index] = action[self.solar_index]
        self.state[self.wind_index] = action[self.wind_index]
        self.state[self.ff_index] = action[self.ff_index]
        self.state[self.time_index] = (self.state[self.time_index] + 1) % 4
        self.state[self.sun_coverage_index] = get_sunlight()
        self.state[self.wind_power_index] = get_wind_power()

        return reward, self.state
