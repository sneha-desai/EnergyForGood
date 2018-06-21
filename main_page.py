import numpy as np
import sys

# import data.resources as capacities
import utils.utils as utils
import utils.plots as plots
# from utils import *
from model.environment import EnergyEnvironment
from model.agent import Agent
from model.house import House

import matplotlib.pyplot as plt


def main_function(location, num_of_panels, num_of_turbines, num_of_batteries):
    # Get arguments
    if len(sys.argv) > 1:
        episodes_num = int(sys.argv[1])
    else:
        episodes_num = 100

    # House dependent parameters
    # location = 'California'
    # num_of_panels = 30   # Number of 250-watts solar panels
    # num_of_turbines = 2  # Number of 400 KW wind turbines
    # num_of_batteries = 2

    house = House(location, num_of_panels, num_of_turbines, num_of_batteries)

    # Main dependent parameters
    num_of_months = 12
    num_of_days = 30        # number of days per episode
    num_time_states = 4
    epsilon = 0.5
    alpha = 0.8

    # Initiate Agent
    agent = Agent()
    Q = agent.initialize_Q()
    avg_Q_old = np.mean(Q)

    # For printing and plots
    print_iteration = 50
    # ARMAN: What is a print_flag?
    print_flag = False

    # ARMAN: Needs comments
    rList = []
    solarList = []
    windList = []
    ffList = []
    battstorageList = []
    battusedList = []
    energyList = []

    solarSubList = []
    windSubList = []
    ffSubList = []
    battstorageSubList = []
    battusedSubList = []

    final_itr = {}

    ## for realtime plotting
    # fig, ax = plt.subplots()
    # ax.set_ylabel("Energy (kWh)")
    # ax.set_title("Evolution of Energy Use")

    for itr in range(episodes_num):
        if itr%print_iteration == 0:
            print_flag = True
 
        # The house stays constant for every episode
        env = EnergyEnvironment(house) 
        cur_state = env.state
        total_reward = 0

        solar_avg = 0
        wind_avg = 0
        ff_avg = 0
        batt_storage_avg = 0
        batt_used_avg = 0

        # for month in range(num_of_months):
        #     env.state[env.month_index] = month

        for day in range(num_of_days):
            total_solar_energy = 0
            total_wind_energy = 0
            total_grid_energy = 0
            total_battery_used = 0

            for i in range(num_time_states):
                action, cur_state_index, action_index = agent.get_action(cur_state, Q, epsilon)
                reward, next_state = env.step(action, cur_state)

                Q = agent.get_Q(action, cur_state, Q, epsilon, cur_state_index, action_index, reward, alpha)

                cur_state = next_state
                total_reward += reward

                # calculate total
                total_solar_energy += env.solar_energy
                total_wind_energy += env.wind_energy
                total_grid_energy += env.grid_energy
                total_battery_used += env.battery_used

                if itr == episodes_num - 1 and day == num_of_days - 1:
                    final_itr[i] = [env.solar_energy, env.wind_energy, env.grid_energy, ]

            # store how much is stored in the battery at the end of each day
            total_battery_stored = env.battery_energy

            # save total daily energy produced from different sources
            solarSubList.append(total_solar_energy)
            windSubList.append(total_wind_energy)
            ffSubList.append(total_grid_energy)
            battstorageSubList.append(total_battery_stored)
            battusedSubList.append(total_battery_used)

            solar_avg = np.mean(solarSubList)
            wind_avg = np.mean(windSubList)
            ff_avg = np.mean(ffSubList)
            batt_storage_avg = np.mean(battstorageSubList)
            batt_used_avg = np.mean(battusedSubList)


        if print_flag:
            avg_Q_new = np.mean(Q)
            avg_Q_change = abs(avg_Q_new-avg_Q_old)
            utils.print_info(itr, env, solar_avg, wind_avg, ff_avg, batt_storage_avg, batt_used_avg, avg_Q_change)
            avg_Q_old = avg_Q_new
            solarList.append(solar_avg)
            windList.append(wind_avg)
            ffList.append(ff_avg)
            battstorageList.append(batt_storage_avg)
            battusedList.append(np.mean(batt_used_avg))

            # plt.ion()
            # plots.real_time_plot([[solar_avg], [wind_avg], [ff_avg],
            #                                [batt_storage_avg], [batt_used_avg]],
            #                     colors=['b', 'g', 'r', 'purple', 'gray'],
            #                     legends=["Solar Energy", "Wind Energy", "Fossil Fuel Energy", "Battery Storage",
            #                              "Battery Usage"], ax=ax)

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
        alpha = max(0, alpha-0.0005)

    # plt.close()
    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)

    plots.plot_learning_curve(rList)

    energyList.append(solarList)
    energyList.append(windList)
    energyList.append(ffList)
    energyList.append(battstorageList)
    energyList.append(battusedList)


    plots.multiBarPlot(list(range(len(solarList))), energyList, colors=['b', 'g', 'r', 'purple', 'gray'], ylabel="Energy (kWh)",
                 title="Evolution of Energy Use", legends=["Solar Energy",  "Wind Energy", "Fossil Fuel Energy", "Battery Storage", "Battery Usage"])

    return list(range(len(solarList))), energyList


# if __name__ == "__main__":
#     main()
