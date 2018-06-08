from setup_environment import EngEnv
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

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