import numpy as np
import random

import utils.maps as maps
import utils.utils as utils

class Agent: 
    def __init__(self):
        self.num_states = {
            "time": 4,
            "sun": 3,
            "wind": 3
        }
        self.num_actions = {
            "solar": 20,
            "fossil": 20,
            "wind": 5
        }

        self.state_map = maps.init_state_map(list(self.num_states.values()))
        self.action_map = maps.init_action_map(list(self.num_actions.values()))

        #Learning paramenters
        self.gamma = 0.95 
        self.alpha = 0.8

    def initialize_Q(self):
        Q_x = np.product(list(self.num_states.values()))
        Q_y = np.product(list(self.num_actions.values()))
        Q = np.zeros([Q_x, Q_y])
        return Q

    def get_action(self, cur_state, Q, epsilon):
        cur_state_index = maps.get_state_index(cur_state, self.state_map)
        action_index = utils.eps_greedy(Q, epsilon, cur_state_index)
        action = self.action_map[action_index]
        return action, cur_state_index, action_index

    def get_Q(self, action, cur_state, Q, epsilon, cur_state_index, action_index, reward):
        expected_value_next_state = utils.calculate_expected_next_state(action, cur_state, self.state_map, Q)
        Q = utils.q_learning_update(self.gamma, self.alpha, Q, cur_state_index, action_index, expected_value_next_state, reward)
        return Q
