import numpy as np
import math
import copy

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

        # grid
        self.grid_producer = EnergyProducer('fossil fuel')
        self.grid_cost = 0
        self.grid_energy = 0 # how much energy has been produced from fossil fuel 

        # other parameters
        self.reward = 0
        self.state = [0,0,0,0] # order = solar, fossil fuel, time, sun
        self.battery = 0

    def reset(self):
        self.solar_cost = 0
        self.solar_energy = 0
        self.grid_cost = 0
        self.grid_energy = 0

    # def reward_base(self, renew_energy, ff_energy, battery, time_energy_requirement, time, renew_cost, ff_cost):
    #     if self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time]:
    #         reward = 1 
    #     else:
    #         reward = -1
        
    #     reward += 0.1*(self.reward_min_cost(renew_cost, ff_cost))
    #     return reward

    def reward_min_cost(self, renew_cost, ff_cost):
        cost = 0
        cost = renew_cost + ff_cost
        if (cost > 0 and cost <= 0.5):
            reward = cost
        else:
            reward = -cost
        return reward

    def step(self, action, state):
        self.reset()

        # NOTE: state is in the form of [solar_switch, ff_switch, time, sun_coverage]
        time = state[2]
        energy_req = self.time_energy_requirement[time]

        sun_coverage = (state[3])/2 # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer

        if (action[0] == 1):
            self.solar_cost = self.solar_producer.production_cost(energy_req, sun_coverage)
            if (time == 2):
                self.solar_energy, self.battery = self.solar_producer.output(energy_req)
                energy_req -= self.solar_energy

        if (self.battery > 0):
            # The case if there is more energy stored than required in this step
            if (self.battery >= energy_req):
                self.battery -= energy_req
                energy_req = 0
            else:
                energy_req -= self.battery
                self.battery -= self.battery

        if (action[1] == 1):
            if (energy_req == 0):
                # Give some negative reward 
                print("Grid didn't need to be on")
            else:
                self.grid_cost = self.grid_producer.production_cost(energy_req, 0)
                self.grid_energy, throwaway = self.grid_producer.output(energy_req)

        # TODO: implement negative reward if energy requirement is not met
        # if (energy_req > 0):
            # Give some negative reward 

        # reward = self.reward_base(self.renew_energy, self.ff_energy, self.battery, self.time_energy_requirement, time)
        reward = self.reward_min_cost(self.solar_cost, self.grid_cost)        
        self.state[0] = action[0]
        self.state[1] = action[1]

        return reward, self.state