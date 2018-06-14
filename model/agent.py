import numpy as np
import random

import utils.maps as maps
import utils.utils as utils

class Agent: 
    def __init__(self):
        self.num_time_states = 4
        self.num_sun_states = 3
        self.num_wind_states = 3

        self.num_solar_actions = 20 
        self.num_fossil_actions = 20
        self.num_wind_actions = 5

        self.state_map = maps.init_state_map(self.num_time_states, self.num_sun_states, self.num_wind_states)
        self.action_map = maps.init_action_map(self.num_solar_actions, self.num_wind_actions, self.num_fossil_actions)

        #Learning paramenters
        self.gamma = 0.95 
        self.alpha = 0.8

    def initialize_Q(self):
        Q_x = self.num_time_states * self.num_sun_states * self.num_wind_states
        Q_y = self.num_solar_actions * self.num_wind_actions * self.num_fossil_actions
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

