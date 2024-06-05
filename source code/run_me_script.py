"""
    IMPORTING REQUIRED MODULES AND PACKAGES
"""

import os
from scegen import create_scenarios_from_default_dataset
import utils
from utils import read_data
import utils_var
import utils_par
import equations
import time
import datetime
import pandas as pd
from utils_par import add_power_prices

# | MEASURE RUNNING TIME OF THE SCRIPT |
_start_time = time.time()
_current_time = datetime.datetime.now()
_formatted_time = _current_time.strftime("%H:%M")
print("Start of the script at:", _formatted_time)


"""
    READING INPUT DATA
"""

_cur_dir = os.path.dirname(__file__)
_path_to_input_folder = os.path.join(_cur_dir, "data")
_constant, _timeseries = read_data(path=_path_to_input_folder)
_balancing = pd.read_csv('data/balancing_market.csv', sep=';')

"""
    DEFINING THE SETS OF THE MODEL
    e.g., year, time step, scenario
"""

_name_of_the_model = "FLXenabler"

# s_inv_years ... 2025, 2030, 2035, 2040, 2045
_s_inv_years = list(_constant.keys())

# s_oper_years ... 2025 to 2050
_s_oper_years = list(range(min(_s_inv_years), max(_s_inv_years) + 6, 1))

# | DEFINE SCENARIO SET
# | Note that the scenario names should be used then in 'scegen.py'
_s_scenarios = ["Scenario1", "Scenario2"]

# hourly temporal resolution within a year
_s_hours = list(_timeseries[list(_timeseries.keys())[0]]["hour"])

_sets = {
    "investment years": _s_inv_years,
    "operation years": _s_oper_years,
    "scenarios": _s_scenarios,
    "timesteps": _s_hours,
}

scenario_tree = create_scenarios_from_default_dataset(
    _s_scenarios, _constant, _timeseries, _balancing
)

model = utils.create_model(_name_of_the_model, _sets)
model.scenario_values = scenario_tree

###############################################################################
# |
# |     - Add power balancing market parameters
# |         - intra-day power prices per year, hour, and scenario.
# |         - binary decision whether or not offered bid has been cleared per year, hour, and scenario.
# |         - power/energy retrieved from the balancing power market per year, hour, and scenario.
# |         - balacing power prices per year, hour, and scenario.
# |

add_power_prices(model)



###############################################################################
# |
# | TECHNOLOGIES
# |     - add technology's paramaters
# |     - add technology's decision variables
# |     - add technology's equation


for _func in [
        # utils_par.add_waste_inc_parameters, # | WASTE INCINERATION 
        # utils_var.add_waste_inc_variables, 
        # equations.add_waste_formula,
        # utils_par.add_industrial_parameters, # | INDUSTRIAL EXCESS HEAT
        # utils_var.add_industrial_variables,
        # equations.add_industrial_formula,
        # utils_par.add_solar_thermal_parameters, # | SOLAR THERMAL
        # utils_var.add_solarthermal_variables, 
        # equations.add_solarthermal_formula,
        # utils_par.add_geothermal_parameters, # | GEOTHERMAL
        # utils_var.add_geothermal_variables,
        # equations.add_geothermal_formula,
        utils_par.add_electric_boiler_parameters, # | ELECTRIC BOILER
        utils_var.add_electric_boiler_variables,
        equations.add_electric_boiler_formula
              ]:
    _func(model)



# # ELECTRIC BOILER (UP (+) & DOWN (-))
# from utils import add_electric_boiler_parameters
# add_electric_boiler_parameters(m)
# # add_electric_boiler_up


# """
#     COMBINED HEAT AND POWER (CHP)
#     - check whether or not hot water tank is included 
# """
# utils_var.add_chp_variables(model)
# utils_par.add_chp_parameters(model)
# equations.add_chp_formula(model)


# # LARGE-SCALE HEAT PUMP (HP)
# from utils import add_hp_parameters
# add_hp_parameters(model)
# from variables import add_hp_variables
# add_hp_variables(model)
# from equations import add_hp_equations
# add_hp_equations(model)


# COOLING TECHNOLOGIES


# STORAGES !!











_end_time = time.time()
_elapsed_time = _end_time - _start_time
_hours = _elapsed_time // 3600
_minutes = (_elapsed_time % 3600) // 60
_seconds = _elapsed_time % 60


print("Script execution time: {:.0f} h ; {:.0f} min ; {:.0f} sec".format(_hours, _minutes, _seconds))