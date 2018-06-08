from setup_environment import EngEnv
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def q_learning_update(gamma, alpha, q_vals, cur_state, action, next_state, reward):
    delta = reward + gamma * np.max(q_vals[next_state, :]) - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta

def get_weather():
    return random.randint(0,2)

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

def print_info(print_flag, itr, env):
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


def multiBarPlot(x, y, colors, ylabel, title, legends):
    N = len(x)
    ind = np.arange(N)
    width = 1.0 / (len(y) + 1)
    fig, ax = plt.subplots()

    rects = []
    for i in range(len(y)):
        rects.append(ax.bar(ind + width * i, y[i], width, color=colors[i]))
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(x)
    ax.legend((rects[0][0], rects[1][0]), legends)
    time = get_timestamp()
    plt.savefig('plots/{}.png'.format(title + time))