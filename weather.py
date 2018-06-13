## This file is modeled as if the weather information could be grabbed from a dataset with weather data over time
## or such that the weather data is grabbed from a weather API

import numpy as np


def get_sunlight():
    # 20% probability of it being a cloudy day - returns 0.0
    # 20% probability of it being a partially cloudy day - returns 0.5
    # 60% probability of it being a perfectly sunny day - returns 1.0
    return np.random.choice(np.arange(0, 3), p=[0.2, 0.2, 0.6])


def get_wind_power():
    # 20% probability of there being no wind - returns 0.0
    # 50% probability of there being some wind - returns 0.5
    # 30% probability of it being very windy - returns 1
    return np.random.choice(np.arange(0, 3), p=[0.2, 0.5, 0.3])
