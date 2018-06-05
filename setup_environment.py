import numpy as np

# flag
##  0: OFF
##  1: ON

""" 
action = [
    [on, off], # solar
    [on, off], # oil
    [on, off], # another
    [on, off]  # another 
]
"""    

# def init():

def step(action, state, time):
    # get weather
    renew_cost, renew_energy = 0
    ff_cost, ff_energy = 0
    if (action[0] === 1):
        renew_cost += 5
        if (time > 11 or time < 13):
            renew_energy += 10
    if (action[1] === 1):
        ff_cost += 10
        ff_energy += 15
    return renew_cost, renew_energy, ff_cost, ff_energy

def reward(solar_percentage, reward):
    if (solar_percentage > 0.5):
        reward += 1
    return reward


# def step(action):
