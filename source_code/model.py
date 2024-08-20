import os
import io
import sys
import time
import datetime
import numpy as np
import pandas as pd
import pyomo.environ as py
import plotly.io as pio
import plotly.graph_objects as go

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

scenarios = ['0_basic', '1_high_electricity_price']
scenarios_weighting = {'0_basic': 0.5, '1_high_electricity_price': 0.5}
years = [2025, 2030, 2035, 2040, 2045, 2050]
hours = list(range(8760))
heating_demand = {}
electricity_price = {}
electricity_mean_price = {}
electricity_co2_share = {}
electricity_mean_co2_share = {}
gas_price = {}
co2_price = {}
data_eb = {}
data_hp = {}
data_st = {}
data_wi = {}
data_gt = {}
data_dgt = {}
data_ieh = {}
data_chp = {}
data_ates = {}
data_ttes = {}
data = {}

#-----------------------------------------------------------------------------#
#                                                                             #
# setting file paths for reading the data                                     #
#                                                                             #
#-----------------------------------------------------------------------------#

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, 'data')
path_to_file_demand = os.path.join(path_to_input_folder, 'demand.xlsx')
path_to_file_electricity_price = os.path.join(path_to_input_folder, 'electricity_price.xlsx')
path_to_file_gas_price = os.path.join(path_to_input_folder, 'gas_price.xlsx')
path_to_file_co2_price = os.path.join(path_to_input_folder, 'co2_price.xlsx')
path_to_file_hp_cop = os.path.join(path_to_input_folder, 'temperature_washington_dc.xlsx')
path_to_file_solar_radiation = os.path.join(path_to_input_folder, 'solar_radiation_washington_dc.xlsx')
path_to_file_ieh_profile = os.path.join(path_to_input_folder, 'ieh_profile.xlsx')
path_to_file_eb = os.path.join(path_to_input_folder, 'eb.xlsx')
path_to_file_hp = os.path.join(path_to_input_folder, 'hp.xlsx')
path_to_file_st = os.path.join(path_to_input_folder, 'st.xlsx')
path_to_file_wi = os.path.join(path_to_input_folder, 'wi.xlsx')
path_to_file_gt = os.path.join(path_to_input_folder, 'gt.xlsx')
path_to_file_dgt = os.path.join(path_to_input_folder, 'dgt.xlsx')
path_to_file_ieh = os.path.join(path_to_input_folder, 'ieh.xlsx')
path_to_file_chp = os.path.join(path_to_input_folder, 'chp.xlsx')
path_to_file_ates = os.path.join(path_to_input_folder, 'ates.xlsx')
path_to_file_ttes = os.path.join(path_to_input_folder, 'ttes.xlsx')

#-----------------------------------------------------------------------------#
#                                                                             #
# reading the input data                                                      #
#                                                                             #
#-----------------------------------------------------------------------------#

for year in years:
    df_demand = pd.read_excel(path_to_file_demand, sheet_name=str(year))
    df_electricity_price = pd.read_excel(path_to_file_electricity_price, sheet_name=str(year))
    df_gas_price = pd.read_excel(path_to_file_gas_price, sheet_name=str(year))
    df_co2_price = pd.read_excel(path_to_file_co2_price, sheet_name=str(year))
    df_hp_cop = pd.read_excel(path_to_file_hp_cop, sheet_name=str(year))
    df_solar_radiation = pd.read_excel(path_to_file_solar_radiation, sheet_name=str(year))
    df_ieh_profile = pd.read_excel(path_to_file_ieh_profile, sheet_name=str(year))
    df_eb = pd.read_excel(path_to_file_eb, sheet_name=str(year))
    df_hp = pd.read_excel(path_to_file_hp, sheet_name=str(year))
    df_st = pd.read_excel(path_to_file_st, sheet_name=str(year))
    df_wi = pd.read_excel(path_to_file_wi, sheet_name=str(year))
    df_gt = pd.read_excel(path_to_file_gt, sheet_name=str(year))
    df_dgt = pd.read_excel(path_to_file_dgt, sheet_name=str(year))
    df_ieh = pd.read_excel(path_to_file_ieh, sheet_name=str(year))
    df_chp = pd.read_excel(path_to_file_chp, sheet_name=str(year))
    df_ates = pd.read_excel(path_to_file_ates, sheet_name=str(year))
    df_ttes = pd.read_excel(path_to_file_ttes, sheet_name=str(year))
    heating_demand[year] = df_demand['heating_demand_districts_building'].tolist()
    electricity_price[year] = df_electricity_price['electricity_price'].tolist()
    electricity_mean_price[year] = np.mean(electricity_price[year])
    electricity_co2_share[year] = df_electricity_price['electricity_co2_share'].tolist()
    electricity_mean_co2_share[year] = np.mean(electricity_co2_share[year])
    gas_price[year] = df_gas_price['gas_price'].tolist()
    co2_price[year] = df_co2_price['co2_price'].tolist()[0]
    p_eb_eta = df_eb['p_eb_eta'].tolist()[0]
    p_eb_c_inv = df_eb['p_eb_c_inv'].tolist()[0]
    # p_eb_c_fix = df_eb['p_eb_c_fix'].tolist()[0]
    data_eb[year] = {'p_eb_eta': p_eb_eta, 'p_eb_c_inv': p_eb_c_inv}
    p_hp_c_inv = df_hp['p_hp_c_inv'].tolist()[0]
    # p_hp_c_fix = df_hp['p_hp_c_fix'].tolist()[0]
    p_hp_cop = df_hp_cop['p_hp_cop'].tolist()
    data_hp[year] = {'p_hp_c_inv': p_hp_c_inv, 'p_hp_cop': p_hp_cop}
    p_st_eta = df_st['p_st_eta'].tolist()[0]
    p_st_c_inv = df_st['p_st_c_inv'].tolist()[0]
    # p_st_c_fix = df_st['p_st_c_fix'].tolist()[0]
    p_st_cop = df_st['p_st_cop'].tolist()[0]
    p_st_solar_radiation = df_solar_radiation['p_st_solar_radiation'].tolist()
    data_st[year] = {'p_st_eta': p_st_eta, 'p_st_c_inv': p_st_c_inv, 'p_st_cop': p_st_cop, 'p_st_solar_radiation': p_st_solar_radiation}
    p_wi_eta = df_wi['p_wi_eta'].tolist()[0]
    p_wi_q_waste = df_wi['p_wi_q_waste'].tolist()[0]
    p_wi_c_waste = df_wi['p_wi_c_waste'].tolist()[0]
    p_wi_h_waste = df_wi['p_wi_h_waste'].tolist()[0]
    p_wi_heat = df_wi['p_wi_heat'].tolist()[0]
    p_wi_elec = df_wi['p_wi_elec'].tolist()[0]    
    p_wi_co2_share = df_wi['p_wi_co2_share'].tolist()[0]
    p_wi_c_inv = df_wi['p_wi_c_inv'].tolist()[0]
    # p_wi_c_fix = df_wi['p_wi_c_fix'].tolist()[0]
    data_wi[year] = {'p_wi_eta': p_wi_eta, 'p_wi_q_waste': p_wi_q_waste, 'p_wi_c_waste': p_wi_c_waste, 'p_wi_h_waste': p_wi_h_waste, 'p_wi_heat': p_wi_heat, 'p_wi_elec': p_wi_elec, 'p_wi_co2_share': p_wi_co2_share, 'p_wi_c_inv': p_wi_c_inv}
    p_gt_c_inv = df_gt['p_gt_c_inv'].tolist()[0]
    # p_gt_c_fix = df_gt['p_gt_c_fix'].tolist()[0]
    p_gt_cop = df_gt['p_gt_cop'].tolist()[0]
    data_gt[year] = {'p_gt_c_inv': p_gt_c_inv, 'p_gt_cop': p_gt_cop}
    p_dgt_c_inv = df_dgt['p_dgt_c_inv'].tolist()[0]
    # p_dgt_c_fix = df_dgt['p_dgt_c_fix'].tolist()[0]
    data_dgt[year] = {'p_dgt_c_inv': p_dgt_c_inv}
    p_ieh_c_inv = df_ieh['p_ieh_c_inv'].tolist()[0]
    # p_ieh_c_fix = df_ieh['p_ieh_c_fix'].tolist()[0]
    p_ieh_c_in = df_ieh['p_ieh_c_in'].tolist()[0]
    p_ieh_elec = df_ieh['p_ieh_elec'].tolist()[0]
    p_ieh_in = df_ieh_profile['p_ieh_in'].tolist()
    data_ieh[year] = {'p_ieh_c_inv': p_ieh_c_inv, 'p_ieh_c_in': p_ieh_c_in, 'p_ieh_elec': p_ieh_elec, 'p_ieh_in': p_ieh_in}
    p_chp_eta = df_chp['p_chp_eta'].tolist()[0]
    p_chp_h_gas = df_chp['p_chp_h_gas'].tolist()[0]
    p_chp_heat = df_chp['p_chp_heat'].tolist()[0]
    p_chp_elec = df_chp['p_chp_elec'].tolist()[0]
    p_chp_co2_share = df_chp['p_chp_co2_share'].tolist()[0]
    p_chp_c_inv = df_chp['p_chp_c_inv'].tolist()[0]
    # p_chp_c_fix = df_chp['p_chp_c_fix'].tolist()[0]
    data_chp[year] = {'p_chp_eta': p_chp_eta, 'p_chp_h_gas': p_chp_h_gas, 'p_chp_heat': p_chp_heat, 'p_chp_elec': p_chp_elec, 'p_chp_co2_share': p_chp_co2_share, 'p_chp_c_inv': p_chp_c_inv}
    p_ates_losses = df_ates['p_ates_losses'].tolist()[0]
    p_ates_eta = df_ates['p_ates_eta'].tolist()[0]
    p_ates_init = df_ates['p_ates_init'].tolist()[0]
    p_ates_end = df_ates['p_ates_end'].tolist()[0]
    p_ates_c_inv = df_ates['p_ates_c_inv'].tolist()[0]
    p_ates_elec = df_ates['p_ates_elec'].tolist()[0]
    p_ates_cop = df_ates['p_ates_cop'].tolist()[0]
    p_ates_c_charge_discharge = df_ates['p_ates_c_charge_discharge'].tolist()[0]
    data_ates[year] = {'p_ates_losses' : p_ates_losses, 'p_ates_eta' : p_ates_eta, 'p_ates_init' : p_ates_init, 'p_ates_end' : p_ates_end, 'p_ates_c_inv' : p_ates_c_inv, 'p_ates_elec' : p_ates_elec, 'p_ates_cop': p_ates_cop, 'p_ates_c_charge_discharge': p_ates_c_charge_discharge}
    p_ttes_losses = df_ttes['p_ttes_losses'].tolist()[0]
    p_ttes_eta = df_ttes['p_ttes_eta'].tolist()[0]
    p_ttes_init = df_ttes['p_ttes_init'].tolist()[0]
    p_ttes_end = df_ttes['p_ttes_end'].tolist()[0]
    p_ttes_c_inv = df_ttes['p_ttes_c_inv'].tolist()[0]
    p_ttes_elec = df_ttes['p_ttes_elec'].tolist()[0]
    p_ttes_cop = df_ttes['p_ttes_cop'].tolist()[0]
    p_ttes_c_charge_discharge = df_ttes['p_ttes_c_charge_discharge'].tolist()[0]
    data_ttes[year] = {'p_ttes_losses' : p_ttes_losses, 'p_ttes_eta' : p_ttes_eta, 'p_ttes_init' : p_ttes_init, 'p_ttes_end' : p_ttes_end, 'p_ttes_c_inv' : p_ttes_c_inv, 'p_ttes_elec' : p_ttes_elec, 'p_ttes_cop': p_ttes_cop, 'p_ttes_c_charge_discharge': p_ttes_c_charge_discharge}

#-----------------------------------------------------------------------------#
#                                                                             #
# creating the basic data structure                                           #
#                                                                             #
#-----------------------------------------------------------------------------#

data['0_basic'] = {'scenario_weighting': scenarios_weighting['0_basic'], 'demand': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
data['1_high_electricity_price'] = {'scenario_weighting': scenarios_weighting['1_high_electricity_price'], 'demand': heating_demand, 'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
data_structure = {'scenarios': scenarios, 'years': years, 'hours': hours}
model_name = 'FLXenabler'

#-----------------------------------------------------------------------------#
#                                                                             #
# definition of the model                                                     #
#                                                                             #
#-----------------------------------------------------------------------------#

model = py.ConcreteModel()
model.name = model_name
model.set_scenarios = py.Set(initialize=data_structure['scenarios'])
model.set_years = py.Set(initialize=data_structure['years'])
model.set_hours = py.Set(initialize=data_structure['hours'])
model.data_values = data

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the general parameters for the model                                 #
#                                                                             #
#-----------------------------------------------------------------------------#

from general import add_general_parameters
add_general_parameters(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the parameters, variables and equations of the heating technologies  #
#                                                                             #
#-----------------------------------------------------------------------------#

from eb import add_eb_variables, add_eb_parameters, add_eb_equations
add_eb_parameters(model)
add_eb_variables(model)
add_eb_equations(model)

from hp import add_hp_variables, add_hp_parameters, add_hp_equations
add_hp_parameters(model)
add_hp_variables(model)
add_hp_equations(model)

from st import add_st_variables, add_st_parameters, add_st_equations
add_st_parameters(model)
add_st_variables(model)
add_st_equations(model)

from wi import add_wi_variables, add_wi_parameters, add_wi_equations
add_wi_parameters(model)
add_wi_variables(model)
add_wi_equations(model)

from gt import add_gt_variables, add_gt_parameters, add_gt_equations
add_gt_parameters(model)
add_gt_variables(model)
add_gt_equations(model)

from dgt import add_dgt_variables, add_dgt_parameters, add_dgt_equations
add_dgt_parameters(model)
add_dgt_variables(model)
add_dgt_equations(model)

from ieh import add_ieh_variables, add_ieh_parameters, add_ieh_equations
add_ieh_parameters(model)
add_ieh_variables(model)
add_ieh_equations(model)

from chp import add_chp_variables, add_chp_parameters, add_chp_equations
add_chp_parameters(model)
add_chp_variables(model)
add_chp_equations(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the parameters, variables and equations of the storage technologies  #
#                                                                             #
#-----------------------------------------------------------------------------#

from ates import add_ates_variables, add_ates_parameters, add_ates_equations
add_ates_parameters(model)
add_ates_variables(model)
add_ates_equations(model)

from ttes import add_ttes_variables, add_ttes_parameters, add_ttes_equations
add_ttes_parameters(model)
add_ttes_variables(model)
add_ttes_equations(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting the demand balance equation                                         #
#                                                                             #
#-----------------------------------------------------------------------------#

def demand_balance(m, s, y, t):
    return m.v_eb_q_heat_in[s, y, t] + m.v_hp_q_heat_in[s, y, t] + m.v_st_q_heat_in[s, y, t] + m.v_wi_q_heat_in[s, y, t] + m.v_gt_q_heat_in[s, y, t] + m.v_dgt_q_heat_in[s, y, t] + m.v_ieh_q_heat_in[s, y, t] + m.v_chp_q_heat_in[s, y, t] + m.v_ttes_q_thermal_in[s, y, t] - m.v_ttes_q_thermal_out[s, y, t]  + m.v_ates_q_thermal_in[s, y, t] - m.v_ates_q_thermal_out[s, y, t] == model.data_values[s]['demand'][y][t]

model.con_demand_balance = py.Constraint(model.set_scenarios, model.set_years, model.set_hours, rule=demand_balance)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting objective function                                                  #
#                                                                             #
#-----------------------------------------------------------------------------#

def objective_function(m):
    return sum(m.v_eb_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_eb_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_eb_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_hp_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_hp_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_hp_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_st_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_st_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_st_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_wi_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_wi_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_wi_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_gt_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_gt_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_gt_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_dgt_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_dgt_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_dgt_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_ieh_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ieh_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ieh_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_chp_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_chp_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_chp_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_ates_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ates_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ates_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios) + \
           sum(m.v_ttes_c_inv[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ttes_c_fix[s, y] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ttes_c_var[s, y, t] for t in m.set_hours for y in m.set_years for s in m.set_scenarios)

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
#solver.options['NonConvex'] = 2
solution = solver.solve(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# ADDITIONAL COMMENTS                                                         #
#                                                                             #
#-----------------------------------------------------------------------------#

#DEMAND FEHLT
#nichtlinear beseitigen in ttes (cop)
#eb limitieren, damit speicher verwendet wird
#data statt liste dictionary verwenden
#ev tupel löschen
#OBJECTIV FUNCTION reperaieren (+ttes mit stromkosten bei variable mit t ändern)
#ttes stromkosten für wärmepumpe
#ttes das mit 1 prozent von maximaler größe funktioniert in gleichung nicht, weil von t abhängig
#ttes charge discharge kosten
#einheiten überprüfen
#dieses file besser die abschnitte kommentieren
#fixkosten z.B. eb tatsächlich anpassen pro Jahr oder festsetzen pro Investition
#Notizen von Felix durchgehen

#-----------------------------------------------------------------------------#
#                                                                             #
# storing the output in output.txt                                            #
#                                                                             #
#-----------------------------------------------------------------------------#

original_stdout = sys.stdout
captured_output = io.StringIO()
sys.stdout = captured_output

model.display()

sys.stdout = original_stdout
output = captured_output.getvalue()
# with open('output.txt', 'w') as f:
#     f.write(output)

max_file_size = 100 * 1000 * 1000 #100 MB Beschränkung auf GitHub: 100 * 1024 * 1024

def write_output_to_files(output, base_filename, max_file_size):
    file_index = 1
    bytes_written = 0
    buffer = []
    for line in output.splitlines(keepends=True):
        buffer.append(line)
        bytes_written += len(line.encode('utf-8'))
        if bytes_written >= max_file_size:
            file_path = '{}_{}.txt'.format(base_filename, file_index)
            with open(file_path, 'w') as f:
                f.writelines(buffer)
            buffer = []
            bytes_written = 0
            file_index += 1
    if buffer:
        file_path = '{}_{}.txt'.format(base_filename, file_index)
        with open(file_path, 'w') as f:
            f.writelines(buffer)

write_output_to_files(output, 'output', max_file_size)

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
# visualization of the data                                                   #
#                                                                             #
#-----------------------------------------------------------------------------#

pio.renderers.default = 'browser'

visualize_hours = hours
visualize_year = 2025
visualize_scenario = '0_basic'

eb_in = []
hp_in = []
st_in = []
wi_in = []
gt_in = []
dgt_in = []
ieh_in = []
chp_in = []
ates_in = []
ates_out = []
ttes_in = []
ttes_out = []

demand = heating_demand[visualize_year]

for hour in visualize_hours:
    eb_in.append(py.value(model.v_eb_q_heat_in[visualize_scenario, visualize_year, hour]))
    hp_in.append(py.value(model.v_hp_q_heat_in[visualize_scenario, visualize_year, hour]))
    st_in.append(py.value(model.v_st_q_heat_in[visualize_scenario, visualize_year, hour]))
    wi_in.append(py.value(model.v_wi_q_heat_in[visualize_scenario, visualize_year, hour]))
    gt_in.append(py.value(model.v_gt_q_heat_in[visualize_scenario, visualize_year, hour]))
    dgt_in.append(py.value(model.v_dgt_q_heat_in[visualize_scenario, visualize_year, hour]))
    ieh_in.append(py.value(model.v_ieh_q_heat_in[visualize_scenario, visualize_year, hour]))
    chp_in.append(py.value(model.v_chp_q_heat_in[visualize_scenario, visualize_year, hour]))
    ates_in.append(py.value(model.v_ates_q_thermal_in[visualize_scenario, visualize_year, hour]))
    ates_out.append(-py.value(model.v_ates_q_thermal_out[visualize_scenario, visualize_year, hour]))
    ttes_in.append(py.value(model.v_ttes_q_thermal_in[visualize_scenario, visualize_year, hour]))
    ttes_out.append(-py.value(model.v_ttes_q_thermal_out[visualize_scenario, visualize_year, hour]))

df = pd.DataFrame({'hour': hours, 'demand': demand, 'eb': eb_in, 'hp': hp_in, 'st': st_in, 'wi': wi_in, 'gt': gt_in, 'dgt': dgt_in, 'ieh': ieh_in, 'chp': chp_in, 'ates+': ates_in, 'ates-': ates_out, 'ttes+': ttes_in, 'ttes-': ttes_out})

fig = go.Figure()

# fig.add_trace(go.Scatter(x=df['hour'], y=df['demand'], fill='tozeroy', name='Demand'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['eb'], fill='tonexty', name='Electric Boiler'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['hp'], fill='tonexty', name='Heat Pump'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['st'], fill='tonexty', name='Solar Thermal'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['wi'], fill='tonexty', name='Waste Incineration'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['gt'], fill='tonexty', name='Geothermal'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['dgt'], fill='tonexty', name='Deep Geothermal'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['ieh'], fill='tonexty', name='Industrial Excess Heat'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['chp'], fill='tonexty', name='Combined Heat and Power'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['ates+'], fill='tonexty', name='ATES in'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['ates-'], fill='tonexty', name='ATES out'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['ttes+'], fill='tonexty', name='TTES in'))
# fig.add_trace(go.Scatter(x=df['hour'], y=df['ttes-'], fill='tonexty', name='TTES out'))

fig.add_trace(go.Scatter(x=df['hour'], y=df['demand'], mode='lines', name='Demand', line=dict(color='black', width=2)))
fig.add_trace(go.Scatter(x=df['hour'], y=df['eb'], mode='lines', name='Electric Boiler', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['hp'], mode='lines', name='Heat Pump', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['st'], mode='lines', name='Solar Thermal', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['wi'], mode='lines', name='Waste Incineration', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['gt'], mode='lines', name='Geothermal', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['dgt'], mode='lines', name='Deep Geothermal', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['ieh'], mode='lines', name='Industrial Excess Heat', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['chp'], mode='lines', name='Combined Heat and Power', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['ates+'], mode='lines', name='ATES in', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['ates-'], mode='lines', name='ATES out', stackgroup='two'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['ttes+'], mode='lines', name='TTES in', stackgroup='one'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['ttes-'], mode='lines', name='TTES out', stackgroup='two'))


fig.update_layout(title='Load Curve', xaxis_title='time in h', yaxis_title='energy in MWh', legend_title='Technologies')

fig.show()



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

print('Script visualizing time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_3, minutes_3, seconds_3))

final_seconds = seconds_1 + seconds_2 + seconds_3
final_minutes = minutes_1 + minutes_2 + minutes_3 + final_seconds // 60
final_seconds = final_seconds % 60
final_hours = hours_1 + hours_2 + hours_3 + final_minutes // 60
final_minutes = final_minutes % 60

print('Script execution time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(final_hours, final_minutes, final_seconds))