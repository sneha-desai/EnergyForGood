import numpy as np
import math
import copy
from weather import *
from EnergyProducer.energy_producer import EnergyProducer

class EngEnv:
    def __init__(self):
        self.time_energy_requirement = [
            7.0,
            8.0,
            6.0,
            7.0
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
        self.count = 0

    def reset(self):
        self.solar_cost = 0
        self.solar_energy = 0
        self.grid_cost = 0
        self.grid_energy = 0
        self.reward = 0

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

    def get_next_state(self, action):
        self.state[0] = action[0]
        self.state[1] = action[1]
        self.state[2] = (self.state[2] + 1) % 4
        self.state[3] = get_sunlight()


    def reward_function(self, action, state, energy_req_after_renewable, energy_req):
        time = state[2]
        if action[0] == 1:
            if time ==2:
                self.reward += 1
            else:
                self.reward -= 1

        if action[1] == 1 and energy_req_after_renewable:
            self.reward -= 100

        if energy_req > 0:
            self.reward -= 0

    def reward_function_2(self, solar_energy_called, grid_energy_called, energy_demand):
        negative_reward = (solar_energy_called-self.solar_energy)**2 + \
                          (grid_energy_called-self.grid_energy)**2 + \
                          (energy_demand)**2

        positive_reward = self.solar_energy + self.battery

        return positive_reward - negative_reward

    def step_2(self, action, state):
        self.reset()

        time = state[2]
        energy_demand = self.time_energy_requirement[time]

        solar_energy_called = action[0]
        grid_energy_called = action[1]

        if time == 2:
            self.solar_energy, self.battery = self.solar_producer.output(energy_demand)

        if self.battery > 0:
            # The case if there is more energy stored than required in this step
            if self.battery >= energy_demand:
                self.battery -= energy_demand
                energy_demand = 0.0
            else:
                energy_demand -= self.battery
                self.battery -= self.battery

        self.grid_energy, throwaway = self.grid_producer.output(energy_demand)
        energy_demand -= self.grid_energy


        # get the reward
        self.reward_function_2(solar_energy_called, grid_energy_called, energy_demand)

        # get the next state
        self.get_next_state(action)

        return self.reward, self.state


    def step(self, action, state):
        self.reset()

        #penalizes reward because of initial cost of solar panels
        # self.reward -= self.solar_producer.get_init_price()/30
        # self.solar_producer.set_init_price(0)

        # NOTE: state is in the form of [solar_switch, ff_switch, time, sun_coverage]
        time = state[2]
        energy_req = self.time_energy_requirement[time]

        sun_coverage = (state[3])/2 # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer

        if action[0] == 1:
            if time == 2:
                # self.reward += 1
                self.solar_cost = self.solar_producer.production_cost(energy_req, sun_coverage)
                self.solar_energy, self.battery = self.solar_producer.output(energy_req)
                energy_req -= self.solar_energy

        if self.battery > 0:
            # The case if there is more energy stored than required in this step
            if self.battery >= energy_req:
                self.battery -= energy_req
                energy_req = 0.0
            else:
                energy_req -= self.battery
                self.battery -= self.battery

        energy_req_after_renewable = energy_req

        if action[1] == 1:
            if energy_req <= 0.0:
                # self.reward -= 100
                print("Grid didn't need to be on")
            else:
                self.grid_cost = self.grid_producer.production_cost(energy_req, 0)
                self.grid_energy, throwaway = self.grid_producer.output(energy_req)
                energy_req -= self.grid_energy

        # TODO: implement negative reward if energy requirement is not met
        if energy_req > 0:
            # Give some negative reward
            self.reward -= 100

        #get the reward
        self.reward_function(action, state, energy_req_after_renewable, energy_req)

        #get the next state
        self.get_next_state(action)


        return self.reward, self.state