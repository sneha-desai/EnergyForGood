from setup_environment import EngEnv
import random
import numpy as np
from datetime import datetime
from maps import *


def q_learning_update(gamma, alpha, q_vals, cur_state, action, expected_value_next_state, reward):
    delta = reward + gamma * expected_value_next_state - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta


def eps_greedy(q_vals, eps, state):
    if random.random() <= eps:
        action = random.randint(0,3)
        return action # sample an action randomly # sample an action randomly
    else:
        action = np.argmax(q_vals[state,:])
    return action


def calculate_expected_next_state(action, cur_state, state_map, q_vals):
    expected_next_state = [[],[],[]]
    expected_next_state_array_indices = []
    max_q_values = []
    expected_next_state[0] = [action[0], action[1], (cur_state[2]+1)%4, 0] #cloudy (20% chance)
    expected_next_state[1] = [action[0], action[1], (cur_state[2]+1)%4, 1] #partially cloudy (20% chance)
    expected_next_state[2] = [action[0], action[1], (cur_state[2]+1)%4, 2] #sunny (60% chance)
    for i in range(len(expected_next_state)):
        expected_next_state_array_indices.append(get_state_index(expected_next_state[i], state_map))
    for j in  range(len(expected_next_state_array_indices)):
        max_q_values.append(np.max(q_vals[expected_next_state_array_indices[i], :]))
    expected_value_next_state = 0.2*max_q_values[0] + 0.2*max_q_values[1] + 0.6*max_q_values[2]
    return expected_value_next_state


def smooth_list(x):
    smoothing_window = 50
    avg_x = []
    for i in range(len(x)):
        avg_x.append(np.mean(x[max(0, i - smoothing_window):i]))
    return avg_x


def print_info(itr, env):
    print("*************************")
    print("Iteration : " + str(itr))
    print("Renewable Energy:" + str(env.renew_energy))
    print("Fossil Fuel Energy: " + str(env.ff_energy))
    print("Renewable Energy Cost: " + str(env.renew_cost))
    print("Fossil Fuel Cost: " + str(env.ff_cost))
    print("Time Energy Requirement: " + str(env.time_energy_requirement[3]))
    if (env.renew_energy + env.ff_energy) > 0:
        print("Percentage of Renewable : " + str(
            (float(env.renew_energy) / (env.renew_energy + env.ff_energy)) * 100))
    else:
        print("NO ENERGY PRODUCED")
    if (env.time_energy_requirement[3] <= (env.renew_energy + env.ff_energy)):
        print("Energy Requirement Met: YES")
    else:
        print(("Energy Requirement Met: NO"))
    print("*************************")


def get_timestamp():
    return str(datetime.now())
