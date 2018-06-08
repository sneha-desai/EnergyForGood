## This file is modeled as if the weather information could be grabbed from a dataset with weather data over time
## or such that the weather data is grabbed from a weather API

import numpy as np

def get_weather():
    # 60% probability of it being a perfectly sunny day
    # 20% probability of it being a partially cloudy day
    # 20% probability of it being a cloudy day
    return np.random.choice(np.arange(0, 3), p=[0.6, 0.2, 0.2])