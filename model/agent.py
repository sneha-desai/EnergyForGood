import numpy as np
import random

import utils.maps as maps
import utils.utils as utils

class Agent: 
    def __init__(self):
        # self.num_month_states = 12
        self.num_time_states = 4
        self.num_sun_states = 3
        self.num_wind_states = 3

        self.num_solar_actions = 20 
        self.num_fossil_actions = 20
        self.num_wind_actions = 6

        # self.Q_x = self.num_time_states * self.num_sun_states * self.num_wind_states * self.num_month_states
        self.Q_x = self.num_time_states * self.num_sun_states * self.num_wind_states
        self.Q_y = self.num_solar_actions * self.num_wind_actions * self.num_fossil_actions

        # self.state_map = maps.init_state_map(self.num_time_states, self.num_sun_states, self.num_wind_states, self.num_month_states)
        self.state_map = maps.init_state_map(self.num_time_states, self.num_sun_states, self.num_wind_states)
        self.action_map = maps.init_action_map(self.num_solar_actions, self.num_wind_actions, self.num_fossil_actions)


        #Learning paramenters
        self.gamma = 0.95 
        # self.alpha = 0.8

    def initialize_Q(self):
        return np.zeros([self.Q_x, self.Q_y])

    def get_action(self, cur_state, Q, epsilon):
        cur_state_index = maps.get_state_index(cur_state, self.state_map)
        action_index = utils.eps_greedy(Q, epsilon, cur_state_index, self.Q_y - 1)
        action = self.action_map[action_index]
        return action, cur_state_index, action_index

    def get_Q(self, action, cur_state, Q, epsilon, cur_state_index, action_index, reward, alpha):
        expected_value_next_state = utils.calculate_expected_next_state(action, cur_state, self.state_map, Q)
        Q = utils.q_learning_update(self.gamma, alpha, Q, cur_state_index, action_index, expected_value_next_state, reward)
        return Q

