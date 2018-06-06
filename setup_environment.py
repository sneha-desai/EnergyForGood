import numpy as np
import math
import copy
# flag
##  0: OFF
##  1: ON

# """ 
# action = [
#     [on, off], # solar
#     [on, off], # oil
#     [on, off], # another
#     [on, off]  # another 
# ]
# """    

class EngEnv:

    def __init__(self):
        self.reward = 0
        self.renew_cost = 0
        self.renew_energy = 0
        self.ff_cost = 0
        self.ff_energy = 0
        self.state = [0,0,0,0]

    def step(self, action, time, sun):
        # get weather
        # renew_cost = 0
        # renew_energy = 0
        # ff_cost = 0
        # ff_energy = 0
        if (action[0] == 1):
            self.renew_cost += 10
            if (time > 11 or time < 13):
                self.renew_energy += 10
        if (action[1] == 1):
            self.ff_cost += 5
            self.ff_energy += 15

        # reward(self)

        if self.ff_energy + self.renew_energy >= 30:
            reward = 30
        else:
            reward = 0

        self.state = action + [time] + [sun]
        return reward, self.state

        # return self.renew_cost, self.renew_energy, \
        #        self.ff_cost, self.ff_energy

    # def reward(self):
    #     if self.ff_energy + self.renew_energy >= 30:
    #         reward = 30
    #     else:
    #         reward = 0
    #     return reward

#     def q_learning_update(gamma, alpha, q_vals, cur_state, action, next_state, reward):
#         delta = reward + gamma * np.max(q_vals[next_state, :]) - q_vals[cur_state, action]
#         q_vals[cur_state, action] = q_vals[cur_state, action] + alpha * delta
#
#
# if __name__ == "__main__":
#     for j in range(5):
#         print("###############################################")
#         total_reward = 0
#         reward = 0
#         env = EngEnv()
#         for i in range(24):
#             reward, state = env.step(np.random.randint(2, size=2), i, np.random.randint(2, size=1))
#             total_reward = total_reward + reward
#             print("Iteration: ", i, " Total Reward: ", total_reward)

