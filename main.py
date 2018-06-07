from setup_environment import EngEnv
import random
import numpy as np
import math
import copy
import matplotlib.pyplot as plt
from datetime import datetime


def q_learning_update(gamma, alpha, q_vals, cur_state, action, next_state, reward):
    delta = reward + gamma * np.max(q_vals[next_state, :]) - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta

def get_weather():
    return np.random.randint(3, size=1)

def init_action_map(a, b):
    count = 0
    mapping = {}
    for i in range(a):
        for j in range(b):
            mapping[count] = [i, j]
            count += 1
    return mapping

def init_state_map(a, b, c, d):
    count = 0
    mapping = {}
    for i in range(a):
        for j in range(b):
            for k in range(c):
                for l in range(d):
                    mapping[count] = [i, j, k, l]
                    count += 1
    return mapping

def get_state_index(state, state_map):
    for k, v in state_map.items():
        if v == state:
            return k

def get_action_index(action, action_map):
    for k, v in action_map.items():
        if v == action:
            return k

def eps_greedy(q_vals, eps, state):
    if random.random() <= eps:
        action = random.randint(0,3)
        return action # sample an action randomly # sample an action randomly
    else:
        action = np.argmax(q_vals[state,:])
    return action

def smooth_list(x):
    smoothing_window = 50
    avg_x = []
    for i in range(len(x)):
        avg_x.append(np.mean(x[max(0, i - smoothing_window):i]))
    return avg_x

def plot_learning_curve(rList):
    x = list(range(len(rList)))
    y = rList

    plt.plot(x, smooth_list(y))
    plt.ylabel("Total Reward")
    plt.xlabel("Episodes")
    plt.grid(True)
    plt.title("Q-Learning Curve")

    time = get_timestamp()
    plt.savefig('plots/{}.png'.format("Q-Learning Curve - " + time))
    plt.close()

def get_timestamp():
    return str(datetime.now())


if __name__ == "__main__":

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

    state_map = init_state_map(num_solar_states, num_fossil_states, num_time_states, num_weather_states)
    action_map = init_action_map(num_solar_actions, num_fossil_states)

    for itr in range(episodes_num):

        print("******************")
        print("Episode: ", itr)

        env = EngEnv()
        cur_state = env.state
        total_reward = 0

        #Static weather in each episode
        weather = get_weather()

        for i in range(4):
            cur_state_index = get_state_index(cur_state, state_map)

            action_index = eps_greedy(Q, epsilon, cur_state_index)
            action = action_map[action_index]

            print("Action: ", action)

            reward, next_state = env.step(action, i, weather)


            next_state_index = get_state_index(next_state, state_map)

            q_learning_update(gamma, alpha, Q, cur_state_index, action_index, next_state_index, reward)

            cur_state = next_state
            total_reward += reward

        # print("Total reward: ", total_reward)
        rList.append(total_reward)

    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)
    plot_learning_curve(rList)







    # for j in range(5):
    #     print("###############################################")
    #     total_reward = 0
    #     reward = 0
    #     env = EngEnv()
    #     for i in range(24):
    #         reward, state = env.step(np.random.randint(2, size=2), i, np.random.randint(2, size=1))
    #         total_reward = total_reward + reward
    #         print("Iteration: ", i, " Total Reward: ", total_reward)



    # action_index = np.argmax(Q[cur_state_index, :])
    # action = action_map[action_index]