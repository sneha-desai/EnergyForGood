import numpy as np
import math
import copy
from weather import *
from EnergyProducer.energy_producer import EnergyProducer
from weather import get_sunlight, get_wind_power

import pdb

class EnergyEnvironment:
    def __init__(self):
        self.time_energy_requirement = [
            7.0,
            8.0,
            6.0,
            7.0
        ]
        # solar
        self.solar_producer = EnergyProducer('solar', s_cap)
        self.solar_cost = 0
        self.solar_energy = 0 

        # wind
        self.wind_producer = EnergyProducer('wind', s_cap)
        self.wind_cost = 0
        self.wind_energy = 0

        # grid
        self.grid_producer = EnergyProducer('fossil fuel', s_cap)
        self.grid_cost = 0
        self.grid_energy = 0 # how much energy has been produced from fossil fuel

        self.battery = EnergyProducer('battery')
        self.battery_energy = 0
        self.battery_used = 0

        # other parameters
        self.reward = 0
        self.state = [0,0,0] # order = time, sun, wind

        self.solar_index = 0
        self.wind_index = 1
        self.ff_index = 2
        self.time_index = 0
        self.sun_coverage_index = 1
        self.wind_power_index = 2

    def reset(self):
        self.solar_cost = 0
        self.solar_energy = 0

        self.wind_cost = 0
        self.wind_energy = 0

        self.grid_cost = 0
        self.grid_energy = 0
        self.reward = 0
        self.battery_used = 0

#     def reward_min_cost(self, solar_cost, wind_cost, ff_cost):
#         cost = solar_cost + wind_cost + ff_cost
#         if (cost > 0 and cost <= 10):
#             reward = cost - ff_cost
#         else:
#             reward = -cost
#         return reward

    def get_next_state(self, action):
        self.state[0] = (self.state[0] + 1) % 4
        self.state[1] = get_sunlight()

#     def reward_function(self, action, state, energy_req_after_renewable, energy_req):
#         time = state[2]
#         if action[0] == 1:
#             if time ==2:
#                 self.reward += 1
#             else:
#                 self.reward -= 1

#         if action[1] == 1 and energy_req_after_renewable:
#             self.reward -= 100

#         if energy_req > 0:
#             self.reward -= 0

#     def step(self, action, state):
#         self.reset()

#         # NOTE: state is in the form of [solar_switch, wind_switch, ff_switch, time, sun_coverage, wind_power]
#         time = state[self.time_index]
#         energy_req = self.time_energy_requirement[time]

#         sun_coverage = (state[self.sun_coverage_index])/2 # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer
#         wind_power = state[self.wind_power_index]/2

# <<<<<<< sneha_2
#         if action[0] == 1:
#             if time == 2:
#                 # self.reward += 1
#                 self.solar_cost = self.solar_producer.production_cost(energy_req, sun_coverage)
#                 self.solar_energy, self.battery = self.solar_producer.output(energy_req)
#                 energy_req -= self.solar_energy

#         if self.battery > 0:
#             # The case if there is more energy stored than required in this step
#             if self.battery >= energy_req:
# =======
#         if (action[self.solar_index] == 1):
#             if (time == 2):
#                 self.solar_energy, self.battery = self.solar_producer.output(energy_req, sun_coverage)
#                 self.solar_cost = self.solar_producer.production_cost(self.solar_energy)
#                 energy_req -= self.solar_energy

#         if (action[self.wind_index] == 1):
#             self.wind_energy, self.battery = self.wind_producer.output(energy_req, wind_power)
#             self.wind_cost = self.wind_producer.production_cost(self.wind_energy)

#         if (self.battery > 0):
#             # The case if there is more energy stored than required in this step
#             self.batter -= energy_req

#             if (self.battery >= energy_req):
# >>>>>>> master
#                 self.battery -= energy_req
#                 energy_req = 0.0
#             else:
#                 energy_req -= self.battery
#                 self.battery -= self.battery

# <<<<<<< sneha_2
#         energy_req_after_renewable = energy_req

#         if action[1] == 1:
#             if energy_req <= 0.0:
#                 # self.reward -= 100
#                 print("Grid didn't need to be on")
#             else:
#                 self.grid_cost = self.grid_producer.production_cost(energy_req, 0)
#                 self.grid_energy, throwaway = self.grid_producer.output(energy_req)
#                 energy_req -= self.grid_energy
# =======
#         if (action[self.ff_index] == 1):
#             if (energy_req == 0):
#                 # Give some negative reward 
#                 print("Grid didn't need to be on")
#             else:
#                 self.grid_energy, throwaway = self.grid_producer.output(energy_req, 0)
#                 self.grid_cost = self.grid_producer.production_cost(self.grid_energy)

# >>>>>>> master

#         # TODO: implement negative reward if energy requirement is not met
#         if energy_req > 0:
#             # Give some negative reward
#             self.reward -= 100

#         #get the reward
#         self.reward_function(action, state, energy_req_after_renewable, energy_req)

#         #get the next state
#         self.get_next_state(action)


#         return self.reward, self.state


    def reward_function_2(self, solar_energy_called, grid_energy_called, energy_demand, grid_energy_produced, solar_energy_produced, battery_used):
        output = grid_energy_produced + solar_energy_produced + battery_used
        negative_reward = abs(solar_energy_called-solar_energy_produced) + \
                          abs(grid_energy_called-grid_energy_produced) + \
                          abs(energy_demand - output)
        positive_reward = abs(solar_energy_produced)+ abs(battery_used)

        self.reward = positive_reward - negative_reward

    def step_2(self, action, state):
        self.reset()

        #penalizes reward because of initial cost of solar panels
        # self.reward -= self.solar_producer.get_init_price()/30
        # self.solar_producer.set_init_price(0)

        time = state[self.time_index]

        sun_coverage = float((state[self.sun_coverage_index]) )/ 2.0  # the 2 divisor makes the sun_coverage an actual sun proportion instead of an integer

        # no sun during the 1st and last time periods
        if time == 0 or time == 3:
            sun_coverage = 0

        energy_demand = self.time_energy_requirement[time]
        # energy_req = self.time_energy_requirement[time]

        solar_energy_called = action[self.solar_index]
        grid_energy_called = action[self.ff_index]

        solar_energy_produced = self.solar_producer.output_2(solar_energy_called, sun_coverage)
        self.solar_energy = copy.deepcopy(solar_energy_produced)

        old_battery = self.battery_energy

        # if there is excess energy to store in battery
        if (self.solar_energy + self.battery_energy) > energy_demand:
            self.battery_energy += (self.solar_energy + self.battery_energy) - energy_demand
            if (self.battery_energy < old_battery):
                self.battery_used = old_battery - self.battery_energy
            else:
                self.battery_used = 0

        #make sure battery energy isn't greater than amount of energy it can store
        self.battery_energy = self.battery.truncate(self.battery_energy)

        #calculate grid energy produced from gril energy call
        grid_energy_produced = self.grid_producer.output_2(grid_energy_called, 1)
        self.grid_energy= copy.deepcopy(grid_energy_produced)

        # get the reward
        self.reward_function_2(solar_energy_called, grid_energy_called, energy_demand, grid_energy_produced,
                               solar_energy_produced, self.battery_used)
        self.get_next_state(action)

        return self.reward, self.state

#         # reward = self.reward_base(self.renew_energy, self.ff_energy, self.battery, self.time_energy_requirement, time)
#         reward = self.reward_min_cost(self.solar_cost, self.wind_cost, self.grid_cost)

#         self.state[self.solar_index] = action[self.solar_index]
#         self.state[self.wind_index] = action[self.wind_index]
#         self.state[self.ff_index] = action[self.ff_index]
#         self.state[self.time_index] = (self.state[self.time_index] + 1) % 4
#         self.state[self.sun_coverage_index] = get_sunlight()
#         self.state[self.wind_power_index] = get_wind_power()

#         return reward, self.state
# >>>>>>> master
