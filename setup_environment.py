import numpy as np
import math
import copy
# flag
##  0: OFF
##  1: ON

# """ 
# action = [
#     [on, off], # solar
#     [on, off], # oil
#     [on, off], # another
#     [on, off]  # another 
# ]
# """    

energy_requirement = {
    "morn" :  7.594591898,
    "aft" : 8.240421074,
    "eve" : 6.522350828,
    "night" : 7.6426362
}

class EngEnv:

    def __init__(self):
        self.time_energy_requirement = [
            7.594591898,
            8.240421074,
            6.522350828,
            7.6426362
        ]
        self.renew_price = 0.10 # $/kWh
        self.ff_price = 0.05 # $/kWh

        self.reward = 0
        self.renew_cost = 0
        self.renew_energy = 0 # how much energy has been produced from renewable
        self.ff_cost = 0
        self.ff_energy = 0 # how much energy has been produced from fossil fuel 
        self.state = [0,0,0,0] # order = solar, fossil fuel, time, sun
        self.battery = 0


    def reward_base(self, renew_energy, ff_energy, battery, time_energy_requirement, time, renew_cost, ff_cost):
        # if self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time] + self.time_energy_requirement[time + 1]:
        #     reward = 1
        if self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time]:
            reward = 1 # possibly make into small positive reward 
        else:
            reward = -1
        
        reward += 0.1*(self.reward_min_cost(renew_cost, ff_cost))
        return reward

    def reward_min_cost(self, renew_cost, ff_cost):
        cost = 0
        cost = renew_cost + ff_cost
        if (cost > 0 and cost <= 1.0):
            reward = cost
        else:
            reward = -cost
        return reward

    def step(self, action, state):
        self.renew_energy = 0
        self.ff_energy = 0
        self.renew_cost = 0
        self.ff_cost = 0
        if (action[0] == 1):
            self.renew_energy = 10*action[0] 
            self.renew_cost = self.renew_price*self.renew_energy
            # if (time == 2):
            #     self.renew_energy = 10
            # self.renew_cost += self.renew_price*self.renew_energy # doesn't charge $ when there is no sun out
            # self.battery = self.renew_energy + self.time_energy_requirement[time]
        # print(self.renew_cost)

        # fossil fuel dial
        if (action[1] == 1):
            self.ff_energy = 10*action[1] # need to tune because 15 is arbitrary
            self.ff_cost = self.ff_price*self.ff_energy

        # print(self.ff_cost)

        # reward = self.reward_base(self.renew_energy, self.ff_energy, self.battery, self.time_energy_requirement, time)
        reward = self.reward_min_cost(self.renew_cost, self.ff_cost)        
        self.state[0] = action[0]
        self.state[1] = action[1]

        # return reward, self.state, self.renew_energy, self.ff_energy
        return reward, self.state

