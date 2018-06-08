from setup_environment import EngEnv
import numpy as np
from utils import q_learning_update, get_weather, init_action_map, init_state_map, \
    get_state_index, get_action_index, eps_greedy, smooth_list, plot_learning_curve, \
    get_timestamp, print_info, multiBarPlot

if __name__ == "__main__":

    num_of_days = 7         # number of days per episode

    num_solar_states = 2
    num_fossil_states = 2
    num_time_states = 4
    num_weather_states = 3

    num_solar_actions = 2
    num_fossil_actions = 2

    Q_x = num_solar_states * num_fossil_states * num_time_states * num_weather_states
    Q_y = num_solar_actions * num_solar_actions

    Q = np.zeros([Q_x, Q_y])

    gamma = 0.
    alpha = 0.8
    epsilon = 0.1
    episodes_num = 100
    rList = []
    reList = []
    ffList = []
    energyList = []

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
            print(cur_state)
            weather = get_weather()     # Static weather in each day

            for i in range(num_time_states):
                cur_state_index = get_state_index(cur_state, state_map)
                cur_state[2] = i
                cur_state[3] = weather

                action_index = eps_greedy(Q, epsilon, cur_state_index)
                action = action_map[action_index]

                reward, next_state = env.step(action, cur_state)

                next_state_index = get_state_index(next_state, state_map)

                q_learning_update(gamma, alpha, Q, cur_state_index, action_index, next_state_index, reward)

                cur_state = next_state
                total_reward += reward

        if print_flag:
            print_info(print_flag, itr, env)
            reList.append(env.renew_energy)
            ffList.append(env.ff_energy)

        print_flag = False

        #total reward per episode appended for learning curve visualization
        rList.append(total_reward)


    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)

    plot_learning_curve(rList)

    energyList.append(reList)
    energyList.append(ffList)
    print(reList)
    print(ffList)
    multiBarPlot(list(range(len(reList))), energyList, colors=['b', 'g'], ylabel="Energy (kWh)", title="Evolution of Energy Use", legends=["Renewable Energy", "Fossil Fuel Energy"])