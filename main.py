from setup_environment import EngEnv
import random
import numpy as np
import math
import copy


def q_learning_update(gamma, alpha, q_vals, cur_state, action, next_state, reward):
    print(reward)
    print(cur_state)
    print(next_state)
    print(action)
    delta = reward + gamma * np.max(q_vals[next_state, :]) - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta

def get_sun():
    return np.random.randint(2, size=1)

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


if __name__ == "__main__":
    Q = np.zeros([32, 4])
    gamma = 0.95
    alpha = 0.8
    epsilon = 0.5
    episodes_num = 5000
    rList = []
    state_map = init_state_map(2,2,4,2)
    action_map = init_action_map(2,2)


    for itr in range(episodes_num):
        print("Episode: ", itr)
        env = EngEnv()
        cur_state = env.state
        total_reward = 0
        done = False
        for i in range(4):
            cur_state_index = get_state_index(cur_state, state_map)

            action_index = eps_greedy(Q, epsilon, cur_state_index)
            action = action_map[action_index]

            print("Action: ", action)

            sun = get_sun()

            reward, next_state = env.step(action, i, sun)

            next_state_index = get_state_index(next_state, state_map)

            q_learning_update(gamma, alpha, Q, cur_state_index, action_index, next_state_index, reward)

            cur_state = next_state
            total_reward += reward
        rList.append(total_reward)

    print("Score over time: " + str(sum(rList) / episodes_num))
    print("Q-values:", Q)







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