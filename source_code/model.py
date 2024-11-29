import time
import datetime
import pyomo.environ as py

# SERVER !!!
# import gurobipy

#-----------------------------------------------------------------------------#
#                                                                             #
# setting start point for runtime measurement                                 #
#                                                                             #
#-----------------------------------------------------------------------------#

start_time = time.time()
current_time = datetime.datetime.now()
formatted_time = current_time.strftime('%H:%M')
print('Start of the script at:', formatted_time)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting the variables for the basic data structure                          #
#                                                                             #
#-----------------------------------------------------------------------------#

# SERVER !!!
# scenarios = ['1_reference', '2_high_electricity_prices', '3_low_electricity_prices', '4_flexible_energy_market', '5_energy_congestion', '6_green_friendly', '7_low_gas_demand', '8_natural_gas_friendly', '9_cold_winters', '10_hot_summers', '11_warm_summers', '12_moderate_climate', '13_zero_co2_price', '14_delayed_co2_pricing', '15_ambitious_co2_pricing', '16_expiring_support_res']
# scenarios_weighting = {'1_reference': 0.15, '2_high_electricity_prices': 0.03, '3_low_electricity_prices': 0.03, '4_flexible_energy_market': 0.1, '5_energy_congestion': 0.06, '6_green_friendly': 0.06, '7_low_gas_demand': 0.06, '8_natural_gas_friendly': 0.03, '9_cold_winters': 0.09, '10_hot_summers': 0.09, '11_warm_summers': 0.03, '12_moderate_climate': 0.03, '13_zero_co2_price': 0.03, '14_delayed_co2_pricing': 0.09, '15_ambitious_co2_pricing': 0.06, '16_expiring_support_res': 0.06}
scenarios = ['1_reference', '2_high_electricity_prices']
scenarios_weighting = {'1_reference': 1, '2_high_electricity_prices': 1}
years = [2025, 2030, 2035, 2040, 2045, 2050]
year_expansion_range = {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1}
hours = list(range(8760))

#-----------------------------------------------------------------------------#
#                                                                             #
# reading the input data                                                      #
#                                                                             #
#-----------------------------------------------------------------------------#

from initialize import initialize_parameters
heating_demand, cooling_demand, electricity_price, electricity_mean_price, gas_price, co2_price, data_eb, data_gb, data_hp, data_st, data_wi, data_ieh, data_chp, data_ac, data_ab, data_cp, data_ttes, data_btes, data_ites = initialize_parameters(years)

#-----------------------------------------------------------------------------#
#                                                                             #
# creating the basic data structure of the scenarios                          #
#                                                                             #
#-----------------------------------------------------------------------------#

# SERVER !!!
from scenarios import define_scenarios
data = define_scenarios(year_expansion_range, heating_demand, cooling_demand, electricity_price, electricity_mean_price, gas_price, co2_price, data_eb, data_gb, data_hp, data_st, data_wi, data_ieh, data_chp, data_ac, data_ab, data_cp, data_ttes, data_btes, data_ites)

#-----------------------------------------------------------------------------#
#                                                                             #
# definition of the model                                                     #
#                                                                             #
#-----------------------------------------------------------------------------#

model_name = 'FLXenabler'
model = py.ConcreteModel()
model.name = model_name
data_structure = {'s': scenarios, 'y': years, 'h': hours}
model.set_scenarios = py.Set(initialize=data_structure['s'])
model.set_years = py.Set(initialize=data_structure['y'])
model.set_hours = py.Set(initialize=data_structure['h'])
model.data_values = data

#-----------------------------------------------------------------------------#
#                                                                             #
# abding the general parameters for the model                                 #
#                                                                             #
#-----------------------------------------------------------------------------#

from general import add_general_parameters
add_general_parameters(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the parameters, variables and equations of the heating technologies  #
#                                                                             #
#-----------------------------------------------------------------------------#

from eb import add_eb_parameters, add_eb_variables, add_eb_equations
add_eb_parameters(model)
add_eb_variables(model)
add_eb_equations(model)

from gb import add_gb_parameters, add_gb_variables, add_gb_equations
add_gb_parameters(model)
add_gb_variables(model)
add_gb_equations(model)

from hp import add_hp_parameters, add_hp_variables, add_hp_equations
add_hp_parameters(model)
add_hp_variables(model)
add_hp_equations(model)

from st import add_st_parameters, add_st_variables, add_st_equations
add_st_parameters(model)
add_st_variables(model)
add_st_equations(model)

from wi import add_wi_parameters, add_wi_variables, add_wi_equations
add_wi_parameters(model)
add_wi_variables(model)
add_wi_equations(model)

from ieh import add_ieh_parameters, add_ieh_variables, add_ieh_equations
add_ieh_parameters(model)
add_ieh_variables(model)
add_ieh_equations(model)

from chp import add_chp_parameters, add_chp_variables, add_chp_equations
add_chp_parameters(model)
add_chp_variables(model)
add_chp_equations(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the parameters, variables and equations of the cooling technologies  #
#                                                                             #
#-----------------------------------------------------------------------------#

from ac import add_ac_parameters, add_ac_variables, add_ac_equations
add_ac_parameters(model)
add_ac_variables(model)
add_ac_equations(model)

from ab import add_ab_parameters, add_ab_variables, add_ab_equations
add_ab_parameters(model)
add_ab_variables(model)
add_ab_equations(model)

from cp import add_cp_parameters, add_cp_variables, add_cp_equations
add_cp_parameters(model)
add_cp_variables(model)
add_cp_equations(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the parameters, variables and equations of the storage technologies  #
#                                                                             #
#-----------------------------------------------------------------------------#

from ttes import add_ttes_parameters, add_ttes_variables, add_ttes_equations
add_ttes_parameters(model)
add_ttes_variables(model)
add_ttes_equations(model)

from btes import add_btes_parameters, add_btes_variables, add_btes_equations
add_btes_parameters(model)
add_btes_variables(model)
add_btes_equations(model)

from ites import add_ites_parameters, add_ites_variables, add_ites_equations
add_ites_parameters(model)
add_ites_variables(model)
add_ites_equations(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting the demand balance equations                                        #
#                                                                             #
#-----------------------------------------------------------------------------#

def demand_balance_heating(m, s, y, h):
    return m.v_eb_q_heat_in[s, y, h] + m.v_gb_q_heat_in[s, y, h] + m.v_hp_q_heat_in[s, y, h] + m.v_st_q_heat_in[s, y, h] + m.v_wi_q_heat_in[s, y, h] + m.v_ieh_q_heat_in[s, y, h] + m.v_chp_q_heat_in[s, y, h] - m.v_ab_ct_q_heat_out[s, y, h] + m.v_ab_hp_q_heat_in[s, y, h] - m.v_ab_hp_q_heat_out[s, y, h] + m.v_cp_hp_q_heat_in[s, y, h] + m.v_ttes_q_heat_in[s, y, h] - m.v_ttes_q_heat_out[s, y, h] + m.v_btes_q_heat_in[s, y, h] == model.data_values[s]['heating'][y][h]

def demand_balance_cooling(m, s, y, h):
    return m.v_ac_q_cool_in[s, y, h] + m.v_ab_ct_q_cool_in[s, y, h] + m.v_ab_hp_q_cool_in[s, y, h] + m.v_cp_ct_q_cool_in[s, y, h] + m.v_cp_hp_q_cool_in[s, y, h] + m.v_ites_q_cool_in[s, y, h] - m.v_ites_q_cool_out[s, y, h] == model.data_values[s]['cooling'][y][h]

model.con_demand_balance_heating = py.Constraint(model.set_scenarios, model.set_years, model.set_hours, rule=demand_balance_heating)
model.con_demand_balance_cooling = py.Constraint(model.set_scenarios, model.set_years, model.set_hours, rule=demand_balance_cooling)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting objective function                                                  #
#                                                                             #
#-----------------------------------------------------------------------------#

def objective_function(m):
    return sum(scenarios_weighting[s] * m.v_eb_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_eb_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_eb_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_hp_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_hp_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_hp_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_st_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_st_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_st_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_wi_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_wi_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_wi_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_ieh_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ieh_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ieh_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_chp_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_chp_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_chp_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_ac_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ac_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ac_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_ab_ct_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ab_ct_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ab_ct_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_ab_hp_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ab_hp_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ab_hp_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_cp_ct_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_cp_ct_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_cp_ct_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_cp_hp_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_cp_hp_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_cp_hp_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_ttes_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ttes_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ttes_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours) + \
           sum(scenarios_weighting[s] * m.v_ites_c_inv[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ites_c_fix[s, y] for s in m.set_scenarios for y in m.set_years) + sum(scenarios_weighting[s] * m.v_ites_c_var[s, y, h] for s in m.set_scenarios for y in m.set_years for h in m.set_hours)

model.obj = py.Objective(expr=objective_function, sense=py.minimize)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting intermediate point for runtime measurement                          #
#                                                                             #
#-----------------------------------------------------------------------------#

intermediate_time = time.time()
elapsed_time_1 = intermediate_time - start_time
start_time = intermediate_time
hours_1 = elapsed_time_1 // 3600
minutes_1 = (elapsed_time_1 % 3600) // 60
seconds_1 = elapsed_time_1 % 60

print('Script initializing time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_1, minutes_1, seconds_1))

#-----------------------------------------------------------------------------#
#                                                                             #
# setting the solver Gurobi                                                   #
#                                                                             #
#-----------------------------------------------------------------------------#

solver = py.SolverFactory('gurobi')
# SERVER !!!
# solver.options['threads'] = 40
#solver.options['NonConvex'] = 2
solution = solver.solve(model)
print(solution)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting intermediate point for runtime measurement                          #
#                                                                             #
#-----------------------------------------------------------------------------#

intermediate_time_2 = time.time()
elapsed_time_2 = intermediate_time_2 - start_time
start_time = intermediate_time_2
hours_2 = elapsed_time_2 // 3600
minutes_2 = (elapsed_time_2 % 3600) // 60
seconds_2 = elapsed_time_2 % 60

print('Script solving time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_2, minutes_2, seconds_2))

#-----------------------------------------------------------------------------#
#                                                                             #
# saving the output in output_x.txt                                           #
#                                                                             #
#-----------------------------------------------------------------------------#

from save import save_output
save_output(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# exporting relevant results in the folder results                            #
#                                                                             #
#-----------------------------------------------------------------------------#

from export import export_result
export_result(model, data, scenarios, scenarios_weighting, years, hours)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting end point for runtime measurement                                   #
#                                                                             #
#-----------------------------------------------------------------------------#

end_time = time.time()
elapsed_time_3 = end_time - start_time
hours_3 = elapsed_time_3 // 3600
minutes_3 = (elapsed_time_3 % 3600) // 60
seconds_3 = elapsed_time_3 % 60

print('Script data saving/exporting time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_3, minutes_3, seconds_3))

final_seconds = seconds_1 + seconds_2 + seconds_3
final_minutes = minutes_1 + minutes_2 + minutes_3 + final_seconds // 60
final_seconds = final_seconds % 60
final_hours = hours_1 + hours_2 + hours_3 + final_minutes // 60
final_minutes = final_minutes % 60

print('Script execution time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(final_hours, final_minutes, final_seconds))