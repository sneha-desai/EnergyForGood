## The U.S. Energy Information Administration (EIA) refers to capacity as
## the maximum output of electricity that a generator can produce under ideal conditions.

## This file is modeled such that the energy capacity from a resource could be taken from an API

## For example the daily output for the solar capacity per month in kWh/m^2/day is shown below: 
#   "outputs": {
#     "avg_dni": {
#       "annual": 6.06,
#       "monthly": {
#         "jan": 5,
#         "feb": 5.34,
#         "mar": 5.94,
#         "apr": 6.11,
#         "may": 6.36,
#         "jun": 7.43,
#         "jul": 7.48,
#         "aug": 6.65,
#         "sep": 6.81,
#         "oct": 5.82,
#         "nov": 5.11,
#         "dec": 4.67
#       }
#     }

resource_capacity = {
    "solar": 10, # Daily capacity for a household solar farm in kWh
    "fossil fuel": 100000 
}

resource_price = {
    "solar": 0.10, # $/kWh,
    "fossil fuel": 0.05 # $/kWh
}


## This file is modeled as if the weather information could be grabbed from a dataset with weather data over time
## or such that the weather data is grabbed from a weather API