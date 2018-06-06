from setup_environment import EngEnv
import numpy as np
import math
import copy


def q_learning_update(gamma, alpha, q_vals, cur_state, action, next_state, reward):
    delta = reward + gamma * np.max(q_vals[next_state, :]) - q_vals[cur_state, action]
    q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta


if __name__ == "__main__":
    for j in range(5):
        print("###############################################")
        total_reward = 0
        reward = 0
        env = EngEnv()
        for i in range(24):
            reward, state = env.step(np.random.randint(2, size=2), i, np.random.randint(2, size=1))
            total_reward = total_reward + reward
            print("Iteration: ", i, " Total Reward: ", total_reward)
