import numpy as np
import sys
from setup_environment import EnergyEnvironment
import utils 
from plots import *
from EnergyProducer.solar_by_region_API import *
from agent import Agent 

#for now let's say location is california always (but maybe eventually will be an argument passed)
location = 'California'
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

    #Learning paramenters
    epsilon = 0.5

    # List parameters
    rList = []
    solarList = []
    windList = []
    ffList = []
    battList = []
    energyList = []

    # SubList paramenters
    solarSubList = []
    windSubList = []
    ffSubList = []
    battSubList = [] 

    print_flag = False

    s_cap = api_call(location) #solar energy from api

    for itr in range(episodes_num):

        # Printing results every 50 episodes
        if itr%print_iteration == 0:
            print_flag = True

        # Reset the state at the beginning of each "week" in this case 
        env = EnergyEnvironment(s_cap)
        cur_state = env.state

        # Set reward = 0 at the beginning of each episode 
        total_reward = 0

        for day in range(num_of_days):

            total_solar_energy = 0
            total_grid_energy = 0
            total_battery = 0

            for i in range(num_time_states):
                action, cur_state_index, action_index = agent.get_action(cur_state, Q, epsilon)
                reward, next_state = env.step(action, cur_state)
                Q = agent.get_Q(action, cur_state, Q, epsilon,
                    cur_state_index, action_index, reward)
 
                cur_state = next_state
                total_reward += reward

                total_solar_energy += env.solar_energy
                total_grid_energy += env.grid_energy
                total_battery = env.battery_energy
                total_wind_energy = env.wind_energy

            solarSubList.append(total_solar_energy)
            ffSubList.append(total_grid_energy)
            battSubList.append(total_battery)
            windSubList.append(total_wind_energy)

        if print_flag:
            # print_info(itr, env)
            solarList.append(np.mean(solarSubList))
            windList.append(np.mean(windSubList))
            ffList.append(np.mean(ffSubList))
            battList.append(np.mean(battSubList))
            solarSubList = []
            windSubList = []
            ffSubList = []

        print_flag = False

        #total reward per episode appended for learning curve visualization
        rList.append(total_reward)

        epsilon = max(0, epsilon-0.0005)
        
    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)

    plot_learning_curve(rList)

    energyList.append(solarList)
    energyList.append(windList)
    energyList.append(ffList)
    energyList.append(battList)
    multiBarPlot(list(range(len(solarList))), energyList, colors=['b', 'g', 'r', 'purple'], ylabel="Energy (kWh)",
                 title="Evolution of Energy Use", legends=["Solar Energy",  "Wind Energy", "Fossil Fuel Energy", "Battery Storage"])
