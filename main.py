import numpy as np
import sys

import utils.utils as utils
import utils.plots as plots 
import utils.maps as maps
from model.environment import EnergyEnvironment
from data.solar_by_region_API import api_call
from model.agent import Agent
import matplotlib.pyplot as plt



if __name__ == "__main__":
    if len(sys.argv) > 1:
        episodes_num = int(sys.argv[1])
    else:
        episodes_num = 1000
    agent = Agent()

    num_of_days = 30        # number of days per episode
    num_time_states = 4

    Q = agent.initialize_Q()

    print_iteration = 50

    # Learning paramenters
    epsilon = 0.5

    # List parameters
    rList = []
    solarList = []
    windList = []
    ffList = []
    battstorageList = []
    battusedList = []
    energyList = []

    # SubList paramenters
    solarSubList = []
    windSubList = []
    ffSubList = []
    battstorageSubList = []
    battusedSubList = []

    print_flag = False

    #solar information
    location = 'California' #for now let's say location is california always (but maybe eventually will be an argument passed)
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    s_cap, solar_dict = api_call(location) #solar energy from api
    panels = 30 # so this number is set for now but can be made modular later
                # it's the number of 250-watts panels -- will determine multiplier

    # for realtime plotting
    fig, ax = plt.subplots()
    ax.set_ylabel("Energy (kWh)")
    ax.set_title("Evolution of Energy Use")

    for itr in range(episodes_num):

        # Printing results every 50 episodes
        if itr%print_iteration == 0:
            print_flag = True
 
        s_cap = int(solar_dict[months[itr%12]]*0.15*(panels*1.6))
        #print(s_cap)

        env = EnergyEnvironment(s_cap)
        cur_state = env.state
        total_reward = 0


        for day in range(num_of_days):

            total_solar_energy = 0
            total_wind_energy = 0
            total_grid_energy = 0
            total_battery_stored = 0
            total_battery_used = 0

            for i in range(num_time_states):
                action, cur_state_index, action_index = agent.get_action(cur_state, Q, epsilon)
                reward, next_state = env.step(action, cur_state)
                Q = agent.get_Q(action, cur_state, Q, epsilon, cur_state_index, action_index, reward)
 
                cur_state = next_state
                total_reward += reward

                # calculate total
                total_solar_energy += env.solar_energy
                total_wind_energy += env.wind_energy
                total_grid_energy += env.grid_energy
                total_battery_stored += env.battery_energy
                total_battery_used += env.battery_used

            # save daily energy use from different sources
            solarSubList.append(total_solar_energy)
            windSubList.append(total_wind_energy)
            ffSubList.append(total_grid_energy)
            battstorageSubList.append(total_battery_stored)
            battusedSubList.append(total_battery_used)


        if print_flag:
            # print_info(itr, env)
            solarList.append(np.mean(solarSubList))
            windList.append(np.mean(windSubList))
            ffList.append(np.mean(ffSubList))
            battstorageList.append(np.mean(battstorageSubList))
            battusedList.append(np.mean(battusedSubList))

            plt.ion()
            plots.real_time_plot([[np.mean(solarSubList)], [np.mean(windSubList)], [np.mean(ffSubList)],
                                            [np.mean(battstorageSubList)], [np.mean(battusedSubList)]],
                                 colors=['b', 'g', 'r', 'purple', 'pink'],
                                 legends=["Solar Energy", "Wind Energy", "Fossil Fuel Energy", "Battery Storage",
                                          "Battery Usage"], ax=ax)

            solarSubList = []
            windSubList = []
            ffSubList = []
            battstorageSubList = []
            battusedSubList = []

        print_flag = False

        #total reward per episode appended for learning curve visualization
        rList.append(total_reward)

        #decrease exploration factor by a little bit every episode
        epsilon = max(0, epsilon-0.0005)

    plt.close()
    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)

    plots.plot_learning_curve(rList)

    energyList.append(solarList)
    energyList.append(windList)
    energyList.append(ffList)
    energyList.append(battstorageList)
    energyList.append(battusedList)


    plots.multiBarPlot(list(range(len(solarList))), energyList, colors=['b', 'g', 'r', 'purple', 'pink'], ylabel="Energy (kWh)",
                 title="Evolution of Energy Use", legends=["Solar Energy",  "Wind Energy", "Fossil Fuel Energy", "Battery Storage", "Battery Usage"])
