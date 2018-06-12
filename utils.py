from setup_environment import EngEnv
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def q_learning_update(gamma, alpha, q_vals, cur_state, action, next_state, reward):
    delta = reward + gamma * np.max(q_vals[next_state, :]) - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta

def eps_greedy(q_vals, eps, state):
    if random.random() <= eps:
        action = random.randint(0,3)
        return action # sample an action randomly # sample an action randomly
    else:
        action = np.argmax(q_vals[state,:])
    return action

# def print_info(itr, env):
#     print("*************************")
#     print("Iteration : " + str(itr))
#     print("Renewable Energy:" + str(env.solar_energy))
#     print("Fossil Fuel Energy: " + str(env.grid_energy))
#     print("Renewable Energy Cost: " + str(env.solar_cost))
#     print("Fossil Fuel Cost: " + str(env.grid_cost))
#     print("Time Energy Requirement: " + str(env.time_energy_requirement[3]))
#     if (env.solar_energy + env.grid_energy) > 0:
#         print("Percentage of Renewable : " + str(
#             (float(env.solar_energy) / (env.solar_energy + env.grid_energy)) * 100))
#     else:
#         print("NO ENERGY PRODUCED")
#     if (env.time_energy_requirement[3] <= (env.solar_energy + env.grid_energy)):
#         print("Energy Requirement Met: YES")
#     else:
#         print(("Energy Requirement Met: NO"))
#     print("*************************")

def get_timestamp():
    return str(datetime.now())
