import numpy as np
import sys
from setup_environment import EngEnv
from utils import *
from plots import *
from maps import *
from weather import *
from EnergyProducer.solar_by_region_API import *

#for now let's say location is california always (but maybe eventually will be an argument passed)
location = 'California'
if __name__ == "__main__":
    if len(sys.argv) > 1:
        episodes_num = int(sys.argv[1])
    else:
        episodes_num = 1000

    num_of_days = 7         # number of days per episode

    num_solar_states = 2
    num_wind_states = 2
    num_fossil_states = 2
    num_time_states = 4
    num_sun_states = 3
    num_wind_states = 3

    num_solar_actions = 2
    num_wind_actions = 2
    num_fossil_actions = 2

    Q_x = num_solar_states * num_wind_states * num_fossil_states * num_time_states * num_sun_states * num_wind_states
    Q_y = num_solar_actions * num_wind_actions * num_fossil_actions

    Q = np.zeros([Q_x, Q_y])

    gamma = 0.
    alpha = 0.8
    epsilon = 0.1
    rList = []
    solarList = []
    windList = []
    ffList = []
    energyList = []

    solarSubList = []
    windSubList = []
    ffSubList = []

    state_map = init_state_map(num_solar_states, num_wind_states, num_fossil_states, num_time_states, num_sun_states, num_wind_states)
    action_map = init_action_map(num_solar_actions, num_wind_actions, num_fossil_actions)

    print_flag = False

    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    s_cap, solar_dict = api_call(location) #solar energy from api

    for itr in range(episodes_num):

        # Printing results every 50 episodes
        if itr % 50 == 0:
            print_flag = True
 
        s_cap = int(solar_dict[months[itr%12]])

        # Reset the state at the beginning of each "week" in this case 
        env = EngEnv(s_cap)

        # Set reward = 0 at the beginning of each episode 
        total_reward = 0

        for day in range(num_of_days):

            cur_state = env.state

            for i in range(num_time_states):
                cur_state_index = get_state_index(cur_state, state_map)

                action_index = eps_greedy(Q, epsilon, cur_state_index)

                action = action_map[action_index]

                # calculate expected next states
                expected_value_next_state = calculate_expected_next_state(action, cur_state, state_map, Q)

                # don't use next_state until next iteration of for loop
                reward, next_state = env.step(action, cur_state)

                q_learning_update(gamma, alpha, Q, cur_state_index, action_index, expected_value_next_state, reward)

                cur_state = next_state
                total_reward += reward

        solarSubList.append(env.solar_energy)
        windSubList.append(env.wind_energy)
        ffSubList.append(env.grid_energy)

        if print_flag:
            # print_info(itr, env)
            solarList.append(np.mean(solarSubList))
            windList.append(np.mean(windSubList))
            ffList.append(np.mean(ffSubList))

            solarSubList = []
            windSubList = []
            ffSubList = []

        print_flag = False

        #total reward per episode appended for learning curve visualization
        rList.append(total_reward)


    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)

    plot_learning_curve(rList)

    energyList.append(solarList)
    energyList.append(windList)
    energyList.append(ffList)
    multiBarPlot(list(range(len(solarList))), energyList, colors=['b', 'r', 'g'], ylabel="Energy (kWh)",
                 title="Evolution of Energy Use", legends=["Solar Energy", "Wind Energy", "Fossil Fuel Energy"])
