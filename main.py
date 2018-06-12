import numpy as np
import sys
from setup_environment import EngEnv
from utils import *
from plots import *
from maps import *
from weather import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        episodes_num = int(sys.argv[1])
    else:
        episodes_num = 1000

    num_of_days = 30         # number of days per episode

    num_solar_states = 2
    num_fossil_states = 2
    num_time_states = 4
    num_weather_states = 3

    num_solar_actions = 30
    num_fossil_actions = 30

    Q_x = num_solar_states * num_fossil_states * num_time_states * num_weather_states
    Q_y = num_solar_actions * num_solar_actions

    Q = np.zeros([Q_x, Q_y])

    gamma = 0.95
    alpha = 0.8
    epsilon = 0.1
    rList = []
    reList = []
    ffList = []
    battList = []
    energyList = []

    reSubList = []
    ffSubList = []
    battSubList = []

    state_map = init_state_map(num_solar_states, num_fossil_states, num_time_states, num_weather_states)
    action_map = init_action_map(num_solar_actions, num_fossil_states)

    print_flag = False

    for itr in range(episodes_num):

        # Printing results every 50 episodes
        if itr%50 == 0:
            print_flag = True

        # Reset the state at the beginning of each "week" in this case 
        env = EngEnv()

        # Set reward = 0 at the beginning of each episode 
        total_reward = 0

        for day in range(num_of_days):

            cur_state = env.state

            total_solar_energy = 0
            total_grid_energy = 0
            total_battery = 0

            for i in range(num_time_states):
                cur_state_index = get_state_index(cur_state, state_map)

                action_index = eps_greedy(Q, epsilon, cur_state_index)
                action = action_map[action_index]

                #calculate expected next states
                expected_value_next_state = calculate_expected_next_state(action, cur_state, state_map, Q)

                #don't use next_state until next iteration of for loop
                reward, next_state = env.step_2(action, cur_state)

                q_learning_update(gamma, alpha, Q, cur_state_index, action_index, expected_value_next_state, reward)

                cur_state = next_state
                total_reward += reward

                total_solar_energy += env.solar_energy
                total_grid_energy += env.grid_energy
                total_battery = env.battery

        reSubList.append(total_solar_energy)
        ffSubList.append(total_grid_energy)
        battSubList.append(total_battery)

        if print_flag:
            print_info(itr, env)
            reList.append(np.mean(reSubList))
            ffList.append(np.mean(ffSubList))
            battList.append(np.mean(battSubList))
            reSubList = []
            ffSubList = []

        print_flag = False

        #total reward per episode appended for learning curve visualization
        rList.append(total_reward)


    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)

    plot_learning_curve(rList)

    energyList.append(reList)
    energyList.append(ffList)
    energyList.append(battList)
    energyList.append
    multiBarPlot(list(range(len(reList))), energyList, colors=['b', 'g', 'r'], ylabel="Energy (kWh)",
                 title="Evolution of Energy Use", legends=["Renewable Energy", "Fossil Fuel Energy", "Solar Battery"])