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
        episodes_num = 2000


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

    final_itr = []
    final_list = []

    final_solar = []
    solar_dict = {0: [], 1: [], 2: [], 3: []}

    final_wind = []
    wind_dict = {0: [], 1: [], 2: [], 3: []}

    final_ff = []
    ff_dict = {0: [], 1: [], 2: [], 3: []}

    final_battery = []
    battery_dict = {0: [], 1: [], 2: [], 3: []}

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

                if itr == (episodes_num - 1):
                    solar_dict[i].append(env.solar_energy)
                    wind_dict[i].append(env.wind_energy)
                    ff_dict[i].append(env.grid_energy)
                    battery_dict[i].append(env.battery_used)

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


    for i in range(num_time_states):
        final_solar.append(np.mean(solar_dict[i]))
        final_wind.append(np.mean(wind_dict[i]))
        final_ff.append(np.mean(ff_dict[i]))
        final_battery.append(np.mean(battery_dict[i]))

    energyList.append(solarList)
    energyList.append(windList)
    energyList.append(ffList)
    # energyList.append(battstorageList)
    energyList.append(battusedList)

    final_itr.append(final_solar)
    final_itr.append(final_wind)
    final_itr.append(final_ff)
    final_itr.append(final_battery)


    # plots.multiBarPlot_final(list(range(4)), final_itr, colors=['b', 'g', 'r', 'purple', 'gray'], ylabel="Energy (kWh)",
    #              title="Final Iteration of Energy Use", legends=["Solar Energy",  "Wind Energy", "Fossil Fuel Energy", "Battery Storage", "Battery Usage"])
    #
    # plots.multiBarPlot(list(range(len(solarList))), energyList, colors=['b', 'g', 'r', 'purple', 'gray'], ylabel="Energy (kWh)",
    #              title="Evolution of Energy Use", legends=["Solar Energy",  "Wind Energy", "Fossil Fuel Energy", "Battery Storage", "Battery Usage"])

    return list(range(len(solarList))), energyList, list(range(len(final_solar))), final_itr, list(range(len(rList))), rList


if __name__ == "__main__":
     x_list, y_list, x_list_final, y_list_final, x_list_learning_curve, y_list_learning_curve = main_function('California', 25, 3, 2)

     y_1 = y_list[0]
     y_2 = y_list[1]
     y_3 = y_list[2]
     y_4 = y_list[3]

     y_1_final = y_list_final[0]
     y_2_final = y_list_final[1]
     y_3_final = y_list_final[2]
     y_4_final = y_list_final[3]

     # print(x_list)
     # print()
     # print(y_1)
     # print(y_2)
     # print(y_3)
     # print(y_4)
     # print()
     # print(y_1_final)
     # print(y_2_final)
     # print(y_3_final)
     # print(y_4_final)
     # print()
     # print(x_list_learning_curve)
     # print(y_list_learning_curve)

     # print(x_list_final)


