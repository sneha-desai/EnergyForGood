import numpy as np
import math
import copy

from EnergyProducer.energy_producer import EnergyProducer
class EngEnv:
    def __init__(self):
        self.time_energy_requirement = [
            7.594591898,
            8.240421074,
            6.522350828,
            7.6426362
        ]
        self.ff_producer = EnergyProducer('fossil fuel')
        self.solar_producer = EnergyProducer('solar')

        self.reward = 0
        self.renew_cost = 0
        self.renew_energy = 0 # how much energy has been produced from renewable
        self.ff_cost = 0
        self.ff_energy = 0 # how much energy has been produced from fossil fuel 
        self.state = [0,0,0,0] # order = solar, fossil fuel, time, sun
        self.battery = 0

    def reset(self):
        self.renew_energy = 0
        self.ff_energy = 0
        self.renew_cost = 0
        self.ff_cost = 0

    def reward_base(self, renew_energy, ff_energy, battery, time_energy_requirement, time, renew_cost, ff_cost):
        if self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time]:
            reward = 1 
        else:
            reward = -1
        
        reward += 0.1*(self.reward_min_cost(renew_cost, ff_cost))
        return reward

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
        time = state[2]
        # NOTE: state is in the form of [solar_switch, ff_switch, time, sun_coverage]

        sun_coverage = (state[3])/2 # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer

        if (action[0] == 1):
            self.renew_cost = self.solar_producer.production_cost(self.time_energy_requirement[time], sun_coverage)
            # if (time == 2):
            #     self.renew_energy = 10
            # self.renew_cost += self.renew_price*self.renew_energy # doesn't charge $ when there is no sun out
            # self.battery = self.renew_energy + self.time_energy_requirement[time]

        if (action[1] == 1):
            self.ff_cost = self.ff_producer.production_cost(self.time_energy_requirement[time], 0)

        # reward = self.reward_base(self.renew_energy, self.ff_energy, self.battery, self.time_energy_requirement, time)
        reward = self.reward_min_cost(self.renew_cost, self.ff_cost)        
        self.state[0] = action[0]
        self.state[1] = action[1]

        return reward, self.state