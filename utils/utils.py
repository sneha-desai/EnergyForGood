import random
import numpy as np
from datetime import datetime

import utils.maps as maps

prob_windy = 0.5
prob_part_windy = 0.4
prob_not_windy = 0.1

def q_learning_update(gamma, alpha, q_vals, cur_state, action, expected_value_next_state, reward):
    delta = reward + gamma * expected_value_next_state - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta
    return q_vals

def eps_greedy(q_vals, eps, state, num_actions):
    if random.random() <= eps:
        action = random.randint(0,num_actions)
        return action # sample an action randomly # sample an action randomly
    else:
        action = np.argmax(q_vals[state,:])
    return action

# def calculate_expected_next_state(action, cur_state, state_map, q_vals):
#     expected_next_state = [[],[],[]]
#     expected_next_state_array_indices = []
#     max_q_values = []
#     expected_next_state[0] = [action[0], action[1], (cur_state[2]+1)%4, 0] #cloudy (20% chance)
#     expected_next_state[1] = [action[0], action[1], (cur_state[2]+1)%4, 1] #partially cloudy (20% chance)
#     expected_next_state[2] = [action[0], action[1], (cur_state[2]+1)%4, 2] #sunny (60% chance)
#     for i in range(len(expected_next_state)):
#         expected_next_state_array_indices.append(get_state_index(expected_next_state[i], state_map))
#     for j in  range(len(expected_next_state_array_indices)):
#         max_q_values.append(np.max(q_vals[expected_next_state_array_indices[i], :]))
#     expected_value_next_state = 0.2*max_q_values[0] + 0.2*max_q_values[1] + 0.6*max_q_values[2]
#     return expected_value_next_state

def calculate_expected_next_state(action, cur_state, state_map, q_vals):
    expected_next_state = [[], [], [], [], [], [], [], [], []]
    expected_next_state_array_indices = []
    max_q_values = []
# <<<<<<< sneha_2
#     expected_next_state[0] = [(cur_state[0]+1)%4, 0] #cloudy (20% chance)
#     expected_next_state[1] = [(cur_state[0]+1)%4, 1] #partially cloudy (20% chance)
#     expected_next_state[2] = [(cur_state[0]+1)%4, 2] #sunny (60% chance)
#     for i in range(len(expected_next_state)):
#         expected_next_state_array_indices.append(get_state_index(expected_next_state[i], state_map))
#     for j in  range(len(expected_next_state_array_indices)):
#         max_q_values.append(np.max(q_vals[expected_next_state_array_indices[j], :]))
#     expected_value_next_state = 0.2*max_q_values[0] + 0.2*max_q_values[1] + 0.6*max_q_values[2]
# =======



    # not windy (20%)
    expected_next_state[0] = [(cur_state[0]+1)%4, 0, 0] #cloudy (20% chance)
    expected_next_state[1] = [(cur_state[0]+1)%4, 1, 0] #partially cloudy (20% chance)
    expected_next_state[2] = [(cur_state[0]+1)%4, 2, 0] #sunny (60% chance)

    # partially windy (50%)
    expected_next_state[3] = [(cur_state[0]+1)%4, 0, 1] #cloudy (20% chance)
    expected_next_state[4] = [(cur_state[0]+1)%4, 1, 1] #partially cloudy (20% chance)
    expected_next_state[5] = [(cur_state[0]+1)%4, 2, 1] #sunny (60% chance)

    # windy (30%)
    expected_next_state[6] = [(cur_state[0]+1)%4, 0, 2] #cloudy (20% chance)
    expected_next_state[7] = [(cur_state[0]+1)%4, 1, 2] #partially cloudy (20% chance)
    expected_next_state[8] = [(cur_state[0]+1)%4, 2, 2] #sunny (60% chance)

    for i in range(len(expected_next_state)):
        expected_next_state_array_indices.append(maps.get_state_index(expected_next_state[i], state_map))

    for j in range(len(expected_next_state_array_indices)):
        # this was originally 'i' but shouldn't it be j???
        max_q_values.append(np.max(q_vals[expected_next_state_array_indices[j], :]))

    expected_value_next_state = 0.2 * prob_not_windy * max_q_values[0] + 0.2 * prob_not_windy * max_q_values[1] + 0.6 * prob_not_windy * max_q_values[2] + \
                                0.2 * prob_part_windy * max_q_values[3] + 0.2 * prob_part_windy * max_q_values[4] + 0.6 * prob_part_windy * max_q_values[5] + \
                                0.2 * prob_windy * max_q_values[6] + 0.2 * prob_windy * max_q_values[7] + 0.6 * prob_windy * max_q_values[8]
    return expected_value_next_state


def smooth_list(x):
    smoothing_window = 50
    avg_x = []
    for i in range(len(x)):
        avg_x.append(np.mean(x[max(0, i - smoothing_window):i]))
    return avg_x


def print_info(itr, env, solar_avg, wind_avg, ff_avg, batt_storage_avg, batt_used_avg, avg_Q_change):
    print("*************************")
    print("Iteration : " + str(itr))
    print( "Q change: %0.2f"%avg_Q_change)
    print("Average Daily Energy Demand: " + str(round(np.mean(env.time_energy_requirement),2)))
    print("Average Daily Solar Energy Produced:" + str(round(solar_avg, 2)))
    print("Average Daily Wind Energy Produced: " + str(round(wind_avg, 2)))
    print("Average Daily Fossil Fuel Energy Produced: " + str(round(ff_avg, 2)))
    print("Average Daily Battery Used Produced: " + str(round(batt_used_avg, 2)))
    print("Daily Energy Stored in Battery Produced: " + str(round(batt_storage_avg, 2)))
    if (solar_avg + wind_avg + batt_used_avg + ff_avg) > 0:
        print("Percentage of Renewable Energy Produced Produced: " + str(
            round(((float(solar_avg + wind_avg + batt_used_avg) / (solar_avg + wind_avg + batt_used_avg + ff_avg)) * 100),2)))
    else:
        print("NO ENERGY PRODUCED")
    if (np.mean(env.time_energy_requirement) <= (solar_avg + wind_avg + batt_used_avg + ff_avg)):
        print("Energy Requirement Met: YES")
    else:
        print(("Energy Requirement Met: NO"))
    print("*************************")


def get_timestamp():
    return str(datetime.now())

