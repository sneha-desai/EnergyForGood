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
            -7.594591898,
            -8.240421074,
            -6.522350828,
            -7.6426362
        ]
        self.renew_price = 0.10 # $/kWh
        self.ff_price = 0.05 # $/kWh

        self.reward = 0
        self.renew_cost = 0
        self.renew_energy = 0 # how much energy has been produced from renewable
        self.ff_cost = 0
        self.ff_energy = 0 # how much energy has been produced from fossil fuel 
        self.state = [0,0,0,0]
        self.battery = 0


    def reward_base(self, renew_energy, ff_energy, battery, time_energy_requirement, time):
        # TODO: going from time 3 to 0 is not time+1 anymore
        # reward(self)
        if self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time] + self.time_energy_requirement[time + 1]:
            reward = 1
        elif self.renew_energy + self.ff_energy + battery >= self.time_energy_requirement[time]:
            reward = 0 # possibly make into small positive reward 
        else:
            reward = -1
        
        return reward

    def reward_min_cost(self, renew_price, ff_price):
        # print("renew_price", renew_price)
        # print("ff_price", ff_price)
        cost = 0
        cost = renew_price + ff_price
        print("cost", cost)
        if (cost > 0 and cost <= 0.5):
            reward = 1
        else:
            reward = -1
        return reward

    def step(self, action, time, sun):
        self.renew_energy = 0
        self.ff_energy = 0
        self.renew_cost = 0
        self.ff_cost = 0
        if (action[0] == 1):
            self.renew_energy = 10*action[0] # need to tune because 15 is arbitrary
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
        self.state = action + [time] + [sun]
        # return reward, self.state, self.renew_energy, self.ff_energy
        # print("State: ", self.state)
        return reward, self.state

