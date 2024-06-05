import os
from utils import read_data
from utils import create_model
from utils import add_parameters_to_model
from scegen import create_scenarios_from_default_dataset
from variables import add_decision_variables
from equations import add_equations
from equations import add_objective_function
from solving import solving_model


# define the set of scenarios here;
# note that the scenario names should be used in 'scegen.py'
set_scenarios = ["Scenario1", "Scenario2"]


_cur_dir = os.path.dirname(__file__)
_path_to_input_folder = os.path.join(_cur_dir, "inputs")
constant, timeseries = read_data(path=_path_to_input_folder)
set_years = list(timeseries.keys())

scenario_tree = create_scenarios_from_default_dataset(
    set_scenarios, constant, timeseries
)

set_hours = list(timeseries[list(timeseries.keys())[0]]["hour"])

mdl_name = "FlexEnebler"
sets = {"scenarios": set_scenarios, "years": set_years, "hours": set_hours}

model = create_model(mdl_name, sets)
model.scenario_values = scenario_tree

# COMBINED HEAT AND POWER UNIT (INCLUDING HOT WATER TANK) (CHP)
add_parameters_to_model(model)
add_decision_variables(model)
add_equations(model)

# INDUSTRIAL EXCESS HEAT (IEH)
from utils import add_ieh_parameters
add_ieh_parameters(model)
from variables import add_ieh_variables
add_ieh_variables(model)
from equations import add_ieh_equations
add_ieh_equations(model)

# SOLAR THERMAL (ST)
from utils import add_st_parameters
add_st_parameters(model)
from variables import add_st_variables
add_st_variables(model)
from equations import add_st_equations
add_st_equations(model)

# GEOTHERMAL SOURCES (GS)
from utils import add_gs_parameters
add_gs_parameters(model)
from variables import add_gs_variables
add_gs_variables(model)
from equations import add_gs_equations
add_gs_equations(model)

# WASTE INCINERATION (I.E., MUNICIPAL SOLID WASTE) (WI)
from utils import add_wi_parameters
add_wi_parameters(model)
from variables import add_wi_variables
add_wi_variables(model)
from equations import add_wi_equations
add_wi_equations(model)

# LARGE-SCALE HEAT PUMP (HP)
from utils import add_hp_parameters
add_hp_parameters(model)
from variables import add_hp_variables
add_hp_variables(model)
from equations import add_hp_equations
add_hp_equations(model)

add_objective_function(model)
solving_model(model)
