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
import plotly.subplots as sp

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

# scenarios = ['0_basic', '1_high_electricity_price', '2_low_electricity_price', '3_non_neg_electricity_price', '4_high_gas_price', '5_zero_co2_price', '6_high_co2_price', '7_half_investment_c', '8_low_electricity_price_high_co2_price', '9_high_electricity_price_high_gas_price_high_co2_price']
scenarios = ['0_basic', '1_high_electricity_price']
scenarios_weighting = {'0_basic': 1, '1_high_electricity_price': 1}
years = [2025, 2030, 2035, 2040, 2045, 2050]
year_expansion_range = {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1}
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
    data_ates[year] = {'p_ates_losses': p_ates_losses, 'p_ates_eta': p_ates_eta, 'p_ates_init': p_ates_init, 'p_ates_end': p_ates_end, 'p_ates_c_inv': p_ates_c_inv, 'p_ates_elec': p_ates_elec, 'p_ates_cop': p_ates_cop, 'p_ates_c_charge_discharge': p_ates_c_charge_discharge}
    p_ttes_losses = df_ttes['p_ttes_losses'].tolist()[0]
    p_ttes_eta = df_ttes['p_ttes_eta'].tolist()[0]
    p_ttes_init = df_ttes['p_ttes_init'].tolist()[0]
    p_ttes_end = df_ttes['p_ttes_end'].tolist()[0]
    p_ttes_c_inv = df_ttes['p_ttes_c_inv'].tolist()[0]
    p_ttes_elec = df_ttes['p_ttes_elec'].tolist()[0]
    p_ttes_cop = df_ttes['p_ttes_cop'].tolist()[0]
    p_ttes_c_charge_discharge = df_ttes['p_ttes_c_charge_discharge'].tolist()[0]
    data_ttes[year] = {'p_ttes_losses': p_ttes_losses, 'p_ttes_eta': p_ttes_eta, 'p_ttes_init': p_ttes_init, 'p_ttes_end': p_ttes_end, 'p_ttes_c_inv': p_ttes_c_inv, 'p_ttes_elec': p_ttes_elec, 'p_ttes_cop': p_ttes_cop, 'p_ttes_c_charge_discharge': p_ttes_c_charge_discharge}

#-----------------------------------------------------------------------------#
#                                                                             #
# creating the basic data structure                                           #
#                                                                             #
#-----------------------------------------------------------------------------#

data['0_basic'] = {'scenario_weighting': scenarios_weighting['0_basic'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
data['1_high_electricity_price'] = {'scenario_weighting': scenarios_weighting['1_high_electricity_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['2_low_electricity_price'] = {'scenario_weighting': scenarios_weighting['2_low_electricity_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['3_non_neg_electricity_price'] = {'scenario_weighting': scenarios_weighting['3_non_neg_electricity_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': {year: [max(0, value) for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: sum(values)/len(values) for year, values in {year: [max(0, value) for value in values] for year, values in electricity_price.items()}.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['4_high_gas_price'] = {'scenario_weighting': scenarios_weighting['4_high_gas_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': {year: [value * 1.3 for value in values] for year, values in gas_price.items()}, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['5_zero_co2_price'] = {'scenario_weighting': scenarios_weighting['5_zero_co2_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': {year: value * 0 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['6_high_co2_price'] = {'scenario_weighting': scenarios_weighting['6_high_co2_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': {year: value * 1.5 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['7_half_investment_c'] = {'scenario_weighting': scenarios_weighting['7_half_investment_c'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': {year: {name: (value * 0.5 if name == 'p_eb_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_eb.items()}, 'hp': {year: {name: (value * 0.5 if name == 'p_hp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_hp.items()}, 'st': {year: {name: (value * 0.5 if name == 'p_st_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_st.items()}, 'wi': {year: {name: (value * 0.5 if name == 'p_wi_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_wi.items()}, 'gt': {year: {name: (value * 0.5 if name == 'p_gt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_gt.items()}, 'dgt': {year: {name: (value * 0.5 if name == 'p_dgt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_dgt.items()}, 'ieh': {year: {name: (value * 0.5 if name == 'p_ieh_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ieh.items()}, 'chp': {year: {name: (value * 0.5 if name == 'p_chp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_chp.items()}, 'ates': {year: {name: (value * 0.5 if name == 'p_ates_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ates.items()}, 'ttes': {year: {name: (value * 0.5 if name == 'p_ttes_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()}}
# data['8_low_electricity_price_high_co2_price'] = {'scenario_weighting': scenarios_weighting['8_low_electricity_price_high_co2_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': {year: value * 1.5 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['9_high_electricity_price_high_gas_price_high_co2_price'] = {'scenario_weighting': scenarios_weighting['9_high_electricity_price_high_gas_price_high_co2_price'], 'year_expansion_range': year_expansion_range,'demand': heating_demand, 'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': {year: [value * 1.3 for value in values] for year, values in gas_price.items()}, 'co2_price': {year: value * 1.5 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
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
# SERVER !!!
# solver.options['threads'] = 40
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

# FIG 0

visualize_hours = hours
visualize_year = 2035
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

df_0 = pd.DataFrame({'hour': hours, 'demand': demand, 'eb': eb_in, 'hp': hp_in, 'st': st_in, 'wi': wi_in, 'gt': gt_in, 'dgt': dgt_in, 'ieh': ieh_in, 'chp': chp_in, 'ates+': ates_in, 'ates-': ates_out, 'ttes+': ttes_in, 'ttes-': ttes_out})

demand_sorted = sorted(demand, reverse=True)
eb_in_sorted = sorted(eb_in, reverse=True)
hp_in_sorted = sorted(hp_in, reverse=True)
st_in_sorted = sorted(st_in, reverse=True)
wi_in_sorted = sorted(wi_in, reverse=True)
gt_in_sorted = sorted(gt_in, reverse=True)
dgt_in_sorted = sorted(dgt_in, reverse=True)
ieh_in_sorted = sorted(ieh_in, reverse=True)
chp_in_sorted = sorted(chp_in, reverse=True)
ates_in_sorted = sorted(ates_in, reverse=True)
ates_out_sorted = sorted(ates_out)
ttes_in_sorted = sorted(ttes_in, reverse=True)
ttes_out_sorted = sorted(ttes_out)

df_1 = pd.DataFrame({'hour': hours, 'demand': demand_sorted, 'eb': eb_in_sorted, 'hp': hp_in_sorted, 'st': st_in_sorted, 'wi': wi_in_sorted, 'gt': gt_in_sorted, 'dgt': dgt_in_sorted, 'ieh': ieh_in_sorted, 'chp': chp_in_sorted, 'ates+': ates_in_sorted, 'ates-': ates_out_sorted, 'ttes+': ttes_in_sorted, 'ttes-': ttes_out_sorted})

fig = go.Figure()

# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['demand'], fill='tozeroy', name='Demand'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['eb'], fill='tonexty', name='Electric Boiler'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['hp'], fill='tonexty', name='Heat Pump'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['st'], fill='tonexty', name='Solar Thermal'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['wi'], fill='tonexty', name='Waste Incineration'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['gt'], fill='tonexty', name='Geothermal'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['dgt'], fill='tonexty', name='Deep Geothermal'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ieh'], fill='tonexty', name='Industrial Excess Heat'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['chp'], fill='tonexty', name='Combined Heat and Power'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ates+'], fill='tonexty', name='ATES in'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ates-'], fill='tonexty', name='ATES out'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ttes+'], fill='tonexty', name='TTES in'))
# fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ttes-'], fill='tonexty', name='TTES out'))

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['chp'], mode='lines', name='Combined heat and power', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['wi'], mode='lines', name='Waste incineration', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['dgt'], mode='lines', name='Deep geothermal', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['st'], mode='lines', name='Solar thermal', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['gt'], mode='lines', name='Geothermal', stackgroup='one', line=dict(color='#00CC96')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['hp'], mode='lines', name='Heat pump', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ieh'], mode='lines', name='Industrial excess heat', stackgroup='one', line=dict(color='#B6E880')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['eb'], mode='lines', name='Electric boiler', stackgroup='one', line=dict(color='#FF6692')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ttes-'], mode='lines', name='TTES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ttes+'], mode='lines', name='TTES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ates-'], mode='lines', name='ATES store', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ates+'], mode='lines', name='ATES feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

# fig.update_layout(title='Load curve', xaxis_title='time in h', yaxis_title='thermal heating energy per hour in MWh/h', legend_title='Technologies')

fig.update_layout(title=dict(text='Load curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['chp'], mode='lines', name='Combined heat and power', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['wi'], mode='lines', name='Waste incineration', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['dgt'], mode='lines', name='Deep geothermal', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['st'], mode='lines', name='Solar thermal', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['gt'], mode='lines', name='Geothermal', stackgroup='one', line=dict(color='#00CC96')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['hp'], mode='lines', name='Heat pump', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ieh'], mode='lines', name='Industrial excess heat', stackgroup='one', line=dict(color='#B6E880')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['eb'], mode='lines', name='Electric boiler', stackgroup='one', line=dict(color='#FF6692')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ttes-'], mode='lines', name='TTES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ttes+'], mode='lines', name='TTES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ates-'], mode='lines', name='ATES store', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ates+'], mode='lines', name='ATES feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

# FIG 1

eb_in_all = []
hp_in_all = []
st_in_all = []
wi_in_all = []
gt_in_all = []
dgt_in_all = []
ieh_in_all = []
chp_in_all = []
ates_in_all = []
ates_out_all = []
ttes_in_all = []
ttes_out_all = []

for scenario in scenarios:
    eb_in_scenario = []
    hp_in_scenario = []
    st_in_scenario = []
    wi_in_scenario = []
    gt_in_scenario = []
    dgt_in_scenario = []
    ieh_in_scenario = []
    chp_in_scenario = []
    ates_in_scenario = []
    ates_out_scenario = []
    ttes_in_scenario = []
    ttes_out_scenario = []
    
    for hour in visualize_hours:
        eb_in_scenario.append(py.value(model.v_eb_q_heat_in[scenario, visualize_year, hour]))
        hp_in_scenario.append(py.value(model.v_hp_q_heat_in[scenario, visualize_year, hour]))
        st_in_scenario.append(py.value(model.v_st_q_heat_in[scenario, visualize_year, hour]))
        wi_in_scenario.append(py.value(model.v_wi_q_heat_in[scenario, visualize_year, hour]))
        gt_in_scenario.append(py.value(model.v_gt_q_heat_in[scenario, visualize_year, hour]))
        dgt_in_scenario.append(py.value(model.v_dgt_q_heat_in[scenario, visualize_year, hour]))
        ieh_in_scenario.append(py.value(model.v_ieh_q_heat_in[scenario, visualize_year, hour]))
        chp_in_scenario.append(py.value(model.v_chp_q_heat_in[scenario, visualize_year, hour]))
        ates_in_scenario.append(py.value(model.v_ates_q_thermal_in[scenario, visualize_year, hour]))
        ates_out_scenario.append(-py.value(model.v_ates_q_thermal_out[scenario, visualize_year, hour]))
        ttes_in_scenario.append(py.value(model.v_ttes_q_thermal_in[scenario, visualize_year, hour]))
        ttes_out_scenario.append(-py.value(model.v_ttes_q_thermal_out[scenario, visualize_year, hour]))
    
    eb_in_all.append(eb_in_scenario)
    hp_in_all.append(hp_in_scenario)
    st_in_all.append(st_in_scenario)
    wi_in_all.append(wi_in_scenario)
    gt_in_all.append(gt_in_scenario)
    dgt_in_all.append(dgt_in_scenario)
    ieh_in_all.append(ieh_in_scenario)
    chp_in_all.append(chp_in_scenario)
    ates_in_all.append(ates_in_scenario)
    ates_out_all.append(ates_out_scenario)
    ttes_in_all.append(ttes_in_scenario)
    ttes_out_all.append(ttes_out_scenario)

df_2 = pd.DataFrame({'hour': [hours]*len(scenarios), 'eb': eb_in_all, 'hp': hp_in_all, 'st': st_in_all, 'wi': wi_in_all, 'gt': gt_in_all, 'dgt': dgt_in_all, 'ieh': ieh_in_all, 'chp': chp_in_all, 'ates+': ates_in_all, 'ates-': ates_out_all, 'ttes+': ttes_in_all, 'ttes-': ttes_out_all})

technologies_abb = ['eb', 'hp', 'st', 'wi', 'gt', 'dgt', 'ieh', 'chp', 'ates+', 'ates-', 'ttes+', 'ttes-']
technologies_name = {'eb': 'Electric boiler', 'hp': 'Heat pump', 'st': 'Solar thermal', 'wi': 'Waste incineration', 'gt': 'Geothermal', 'dgt': 'Deep geothermal', 'ieh': 'Industrial excess heat', 'chp': 'Combined heat and power', 'ates+': 'ATES feed in', 'ates-': 'ATES store', 'ttes+': 'TTES feed in', 'ttes-': 'TTES store'}

for technology in technologies_abb: 
    fig = go.Figure()
    
    for scenario_index in range(len(scenarios)):
        fig.add_trace(go.Scatter(x=df_2['hour'][scenario_index], y=df_2[technology][scenario_index], mode='lines', name=scenarios[scenario_index]))

    fig.update_layout(title=dict(text=technologies_name[technology], font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

    fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Winter week', 'Summer week'))

fig.add_trace(go.Scatter(x=list(range(168)), y=df_2['gt'][0][:168], mode='lines', name='Scenario 0: basic', line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)), y=df_2['gt'][1][:168], mode='lines', name='Scenario 1: high electricity price', line=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)) + list(range(168))[::-1], y=df_2['gt'][0][:168] + df_2['gt'][1][:168][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)

#fig.add_trace(go.Scatter(x=list(range(168)), y=df_2['gt'][1], mode='lines', name='Scenario 1: high electricity price', fill='tonexty', fillcolor='#00CC96'))

fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_2['gt'][0][4380:4548], mode='lines', name='Scenario 0: basic', line=dict(color='#636EFA'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_2['gt'][1][4380:4548], mode='lines', name='Scenario 1: high electricity price', line=dict(color='#00CC96'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)) + list(range(4380, 4548))[::-1], y=df_2['gt'][0][4380:4548] + df_2['gt'][1][4380:4548][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=2)

fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=1)
fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=2)

fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Geothermal', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Winter week', 'Summer week'))

fig.add_trace(go.Scatter(x=list(range(168)), y=df_2['ieh'][0][:168], mode='lines', name='Scenario 0: basic', line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)), y=df_2['ieh'][1][:168], mode='lines', name='Scenario 1: high electricity price', line=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)) + list(range(168))[::-1], y=df_2['ieh'][0][:168] + df_2['ieh'][1][:168][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)

#fig.add_trace(go.Scatter(x=list(range(168)), y=df_2['gt'][1], mode='lines', name='Scenario 1: high electricity price', fill='tonexty', fillcolor='#00CC96'))

fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_2['ieh'][0][4380:4548], mode='lines', name='Scenario 0: basic', line=dict(color='#636EFA'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_2['ieh'][1][4380:4548], mode='lines', name='Scenario 1: high electricity price', line=dict(color='#00CC96'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)) + list(range(4380, 4548))[::-1], y=df_2['ieh'][0][4380:4548] + df_2['ieh'][1][4380:4548][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=2)

fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=1)
fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=2)

fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Industrial excess heat', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

# FIG 2

# eb_inv = []
# hp_inv = []
# st_inv = []
# wi_inv = []
# gt_inv = []
# dgt_inv = []
# ieh_inv = []
# chp_inv = []
# ates_inv = []
# ttes_inv = []

# for year in years:
#     eb_inv.append(py.value(model.v_eb_Q_inv[visualize_scenario, year]))
#     hp_inv.append(py.value(model.v_hp_Q_inv[visualize_scenario, year]))
#     st_inv.append(py.value(model.v_st_P_inv[visualize_scenario, year]))
#     wi_inv.append(py.value(model.v_wi_Q_inv[visualize_scenario, year]))
#     gt_inv.append(py.value(model.v_gt_Q_inv[visualize_scenario, year]))
#     dgt_inv.append(py.value(model.v_dgt_Q_inv[visualize_scenario, year]))
#     ieh_inv.append(py.value(model.v_ieh_Q_inv[visualize_scenario, year]))
#     chp_inv.append(py.value(model.v_chp_Q_inv[visualize_scenario, year]))
#     ates_inv.append(py.value(model.v_ates_k_inv[visualize_scenario, year]))
#     ttes_inv.append(py.value(model.v_ttes_k_inv[visualize_scenario, year]))

# technologies = ['Electric Boiler', 'Heat Pump', 'Solar Thermal', 'Waste Incineration', 'Geothermal', 'Deep Geothermal', 'Industrial Excess Heat', 'Combined Heat and Power', 'ATES', 'TTES']
# technologies_map = {'Electric Boiler': eb_inv, 'Heat Pump': hp_inv, 'Solar Thermal': st_inv, 'Waste Incineration': wi_inv, 'Geothermal': gt_inv, 'Deep Geothermal': dgt_inv, 'Industrial Excess Heat': ieh_inv, 'Combined Heat and Power': chp_inv, 'ATES': ates_inv, 'TTES': ttes_inv}
# technologies_inv = []

# for year_index in range(len(years)):
#     year_inv = []
#     for technology in technologies:
#         year_inv.append(technologies_map[technology][year_index])
        
#     technologies_inv.append(year_inv)

# fig = go.Figure()

# fig.add_trace(go.Bar(x=technologies, y=technologies_inv[0], name='2025'))
# fig.add_trace(go.Bar(x=technologies, y=technologies_inv[1], name='2030'))
# fig.add_trace(go.Bar(x=technologies, y=technologies_inv[2], name='2035'))
# fig.add_trace(go.Bar(x=technologies, y=technologies_inv[3], name='2040'))
# fig.add_trace(go.Bar(x=technologies, y=technologies_inv[4], name='2045'))
# fig.add_trace(go.Bar(x=technologies, y=technologies_inv[5], name='2050'))

# fig.update_layout(title='Investments', legend_title='Years', barmode='stack')

# fig.show()

eb_inv = []
hp_inv = []
st_inv = []
wi_inv = []
gt_inv = []
dgt_inv = []
ieh_inv = []
chp_inv = []
ates_inv = []
ttes_inv = []
ratio_eb_inv = []
ratio_hp_inv = []
ratio_gt_inv = []
ratio_ieh_inv = []
ratio_inv = []
index = 0
heating_eb_inv_sum = 0
heating_hp_inv_sum = 0
heating_gt_inv_sum = 0
heating_ieh_inv_sum = 0
heating_technology_inv_sum = 0
storage_technology_inv_sum = 0

for year in years[:3]:
    eb_inv.append(py.value(model.v_eb_Q_inv[year]))
    hp_inv.append(py.value(model.v_hp_Q_inv[year]))
    st_inv.append(py.value(model.v_st_P_inv[year]))
    wi_inv.append(py.value(model.v_wi_Q_inv[year]))
    gt_inv.append(py.value(model.v_gt_Q_inv[year]))
    dgt_inv.append(py.value(model.v_dgt_Q_inv[year]))
    ieh_inv.append(py.value(model.v_ieh_Q_inv[year]))
    chp_inv.append(py.value(model.v_chp_Q_inv[year]))
    ates_inv.append(py.value(model.v_ates_k_inv[year]))
    ttes_inv.append(py.value(model.v_ttes_k_inv[year]))
    
    heating_eb_inv_sum += eb_inv[index]
    heating_hp_inv_sum += hp_inv[index]
    heating_gt_inv_sum += gt_inv[index]
    heating_ieh_inv_sum += ieh_inv[index]
    heating_technology_inv_sum += eb_inv[index] + hp_inv[index] + st_inv[index] + wi_inv[index] + gt_inv[index] + dgt_inv[index] + ieh_inv[index] + chp_inv[index]
    storage_technology_inv_sum += ates_inv[index] + ttes_inv[index]
    index +=1
    
    ratio_eb_inv.append(heating_eb_inv_sum / storage_technology_inv_sum * 100)
    ratio_hp_inv.append(heating_hp_inv_sum / storage_technology_inv_sum * 100)
    ratio_gt_inv.append(heating_gt_inv_sum / storage_technology_inv_sum * 100)
    ratio_ieh_inv.append(heating_ieh_inv_sum / storage_technology_inv_sum * 100)
    ratio_inv.append(heating_technology_inv_sum / storage_technology_inv_sum * 100)

technologies = ['Electric boiler', 'Heat pump', 'Solar thermal', 'Waste incineration', 'Geothermal', 'Deep geothermal', 'Industrial excess heat', 'Combined heat and power']
technologies_map = {'Electric boiler': eb_inv, 'Heat pump': hp_inv, 'Solar thermal': st_inv, 'Waste incineration': wi_inv, 'Geothermal': gt_inv, 'Deep geothermal': dgt_inv, 'Industrial excess heat': ieh_inv, 'Combined heat and power': chp_inv}
storages = ['Aquifer thermal energy storage', 'Tank thermal energy storage']
storages_map = {'Aquifer thermal energy storage': ates_inv, 'Tank thermal energy storage': ttes_inv}

fig = go.Figure()

fig = sp.make_subplots(rows=2, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}], [{'colspan': 1}, None]], subplot_titles=('Heating technology investments', 'Storage technology investments', 'Ratio heating to storage capacity'))

fig.add_trace(go.Scatter(x=years[:3], y=ratio_inv, name='Ratio'), row=2, col=1)

fig.add_trace(go.Bar(x=years[:3], y=storages_map['Aquifer thermal energy storage'], name='Aquifer thermal energy storage', marker=dict(color='grey')), row=1, col=2)
fig.add_trace(go.Bar(x=years[:3], y=storages_map['Tank thermal energy storage'], name='Tank thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Electric boiler'], name='Electric boiler', marker=dict(color='#FF6692')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Industrial excess heat'], name='Industrial excess heat', marker=dict(color='#B6E880')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Heat pump'], name='Heat pump', marker=dict(color='#19D3F3')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Geothermal'], name='Geothermal', marker=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Solar thermal'], name='Solar thermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Deep geothermal'], name='Deep geothermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Waste incineration'], name='Waste incineration', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Combined heat and power'], name='Combined heat and power', marker=dict(color='grey')), row=1, col=1)
    
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=1, col=2)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=2, col=1)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=1)

fig.update_yaxes(range=[0, 20], row=2, col=1)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(x=0.7, y=0, traceorder='normal', font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack', width=1200, height=900)

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=2, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}], [{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Heating technology investments', 'Storage technology investments', 'Ratio heating to storage capacity', 'Ratio heating to storage capacity'))

fig.add_trace(go.Scatter(x=years[:3], y=ratio_inv, name='Ratio total', line=dict(color='#EF553B')), row=2, col=2)

fig.add_trace(go.Scatter(x=years[:3], y=ratio_gt_inv, name='Ratio geothermal', line=dict(color='#00CC96')), row=2, col=1)
fig.add_trace(go.Scatter(x=years[:3], y=ratio_hp_inv, name='Ratio heat pump', line=dict(color='#19D3F3')), row=2, col=1)
fig.add_trace(go.Scatter(x=years[:3], y=ratio_ieh_inv, name='Ratio industrial excess heat', line=dict(color='#B6E880')), row=2, col=1)
fig.add_trace(go.Scatter(x=years[:3], y=ratio_eb_inv, name='Ratio electric boiler', line=dict(color='#FF6692')), row=2, col=1)

fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Combined heat and power'], name='Combined heat and power', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Waste incineration'], name='Waste incineration', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Deep geothermal'], name='Deep geothermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Solar thermal'], name='Solar thermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Geothermal'], name='Geothermal', marker=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Heat pump'], name='Heat pump', marker=dict(color='#19D3F3')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Industrial excess heat'], name='Industrial excess heat', marker=dict(color='#B6E880')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:3], y=technologies_map['Electric boiler'], name='Electric boiler', marker=dict(color='#FF6692')), row=1, col=1)

fig.add_trace(go.Bar(x=years[:3], y=storages_map['Tank thermal energy storage'], name='Tank thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)
fig.add_trace(go.Bar(x=years[:3], y=storages_map['Aquifer thermal energy storage'], name='Aquifer thermal energy storage', marker=dict(color='grey')), row=1, col=2)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=1, col=2)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=2, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:3], row=2, col=2)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=1)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=2)

fig.update_yaxes(range=[0, 10], row=2, col=1)
fig.update_yaxes(range=[0, 20], row=2, col=2)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack')

fig.show()

# FIG 3

buildings_gas = []
buildings_electricity = [11, 16, 19, 30, 37]

for building in range(1, 40):
    if building not in buildings_electricity:
        buildings_gas.append(building)

buildings = {1: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             2: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             3: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             4: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             5: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             6: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             7: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             8: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             9: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             10: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             11: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             12: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             13: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             14: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             15: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             16: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             17: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             18: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             19: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             20: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             21: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             22: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             23: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             24: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             25: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             26: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             27: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             28: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             29: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             30: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             31: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             32: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             33: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             34: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             35: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             36: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             37: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             38: {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1},
             39: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1}}

buildings_demand = {}
buildings_demand_sum = {}
buildings_lcoh = {}

path_to_file_heating_demand_building = os.path.join(path_to_input_folder, 'districts_heating_demand_phase2.xlsx')
df_heating_demand_building = pd.read_excel(path_to_file_heating_demand_building)

for building in range(1, 40):
    heating_demand_building = df_heating_demand_building[f'heating_demand_building_{building}'].tolist()
    buildings_demand[building] = heating_demand_building
    buildings_demand_sum[building] = sum(heating_demand_building)

# assumptions
eta_gas = 0.9
co2_conversion = 0.2
eta_electricity = 0.99

for building in range(1, 40):
    buildings_lcoh_scenario = []
    for scenario in scenarios:
        building_c_sum = 0
        
        for year in years:
            for hour in hours:
                if building in buildings_gas:
                    building_c_sum += buildings[building][year] * buildings_demand[building][hour] / eta_gas * (data[scenario]['gas_price'][year][hour] + co2_conversion * data[scenario]['co2_price'][year])
                    
                else:
                    building_c_sum += buildings[building][year] * buildings_demand[building][hour] / eta_electricity * (data[scenario]['electricity_price'][year][hour] + data[scenario]['electricity_co2_share'][year][hour] * data[scenario]['co2_price'][year])
            
        buildings_lcoh_scenario.append(building_c_sum / (buildings_demand_sum[building] * sum(buildings[building].values())))

    buildings_lcoh[building] = buildings_lcoh_scenario


building_lcoh_max = []
building_lcoh_min = []
building_lcoh_avg = []

for building in range(1, 40):
    building_lcoh_max.append(max(buildings_lcoh[building]))
    building_lcoh_min.append(min(buildings_lcoh[building]))
    building_lcoh_avg.append(np.mean([min(buildings_lcoh[building]), max(buildings_lcoh[building])]))

building_lcoh_max_index = [i + 1 for i in sorted(range(len(building_lcoh_max)), key=lambda i: building_lcoh_max[i], reverse=True)]
building_lcoh_min_index = [i + 1 for i in sorted(range(len(building_lcoh_min)), key=lambda i: building_lcoh_min[i], reverse=True)]
building_lcoh_avg_index = [i + 1 for i in sorted(range(len(building_lcoh_avg)), key=lambda i: building_lcoh_avg[i], reverse=True)]

x_bar = []
y_bar = []
widths = []
bases = []
labels = []

for building in range(1, 40):
    if building == 1:
        x_bar.append(buildings_demand_sum[building] / 2)
        
    else:
        x_bar.append(x_bar[building-2] + buildings_demand_sum[building-1] / 2 + buildings_demand_sum[building] / 2)
    
    y_bar.append(max(buildings_lcoh[building]) - min(buildings_lcoh[building]))
    widths.append(buildings_demand_sum[building])
    bases.append(min(buildings_lcoh[building]))
    labels.append(f'Building_{building}')

lcoh = {}

for scenario in scenarios:
    sum_cost_scenario = 0
    sum_demand_scenario = 0
    for y in years:
        sum_demand = 0
        
        for t in hours:
            sum_cost_scenario +=  py.value(model.v_eb_c_var[scenario, y, t]) + \
                                  py.value(model.v_hp_c_var[scenario, y, t]) + \
                                  py.value(model.v_st_c_var[scenario, y, t]) + \
                                  py.value(model.v_wi_c_var[scenario, y, t]) + \
                                  py.value(model.v_gt_c_var[scenario, y, t]) + \
                                  py.value(model.v_dgt_c_var[scenario, y, t]) + \
                                  py.value(model.v_ieh_c_var[scenario, y, t]) + \
                                  py.value(model.v_chp_c_var[scenario, y, t]) + \
                                  py.value(model.v_ates_c_var[scenario, y, t]) + \
                                  py.value(model.v_ttes_c_var[scenario, y, t])

            sum_demand += py.value(model.data_values[scenario]['demand'][y][t])
        sum_demand_scenario += sum_demand * year_expansion_range[y]
        
        sum_cost_scenario += py.value(model.v_eb_c_inv[scenario, y]) + py.value(model.v_eb_c_fix[scenario, y]) + \
                             py.value(model.v_hp_c_inv[scenario, y]) + py.value(model.v_hp_c_fix[scenario, y]) + \
                             py.value(model.v_st_c_inv[scenario, y]) + py.value(model.v_st_c_fix[scenario, y]) + \
                             py.value(model.v_wi_c_inv[scenario, y]) + py.value(model.v_wi_c_fix[scenario, y]) + \
                             py.value(model.v_gt_c_inv[scenario, y]) + py.value(model.v_gt_c_fix[scenario, y]) + \
                             py.value(model.v_dgt_c_inv[scenario, y]) + py.value(model.v_dgt_c_fix[scenario, y]) + \
                             py.value(model.v_ieh_c_inv[scenario, y]) + py.value(model.v_ieh_c_fix[scenario, y]) + \
                             py.value(model.v_chp_c_inv[scenario, y]) + py.value(model.v_chp_c_fix[scenario, y]) + \
                             py.value(model.v_ates_c_inv[scenario, y]) + py.value(model.v_ates_c_fix[scenario, y]) + \
                             py.value(model.v_ttes_c_inv[scenario, y]) + py.value(model.v_ttes_c_fix[scenario, y])
        
    lcoh[scenario] = sum_cost_scenario / scenarios_weighting[scenario] / sum_demand_scenario

fig = go.Figure()

lcoh_min = min(lcoh, key=lcoh.get)
lcoh_max = max(lcoh, key=lcoh.get)

# for scenario in scenarios:
#     fig.add_trace(go.Scatter(x=[0, sum_demand], y=[lcoh[scenario], lcoh[scenario]], mode='lines', name=scenario))

fig.add_trace(go.Scatter(x=[0, sum_demand], y=[lcoh[lcoh_min], lcoh[lcoh_min]], mode='lines', line=dict(color='black'), name=lcoh_min, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_demand], y=[lcoh[lcoh_max], lcoh[lcoh_max]], mode='lines', line=dict(color='black'), name=lcoh_max, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_demand, sum_demand, 0], y=[lcoh[lcoh_min], lcoh[lcoh_min], lcoh[lcoh_max], lcoh[lcoh_max]],  fill='toself', fillcolor='gray', opacity=0.5, line=dict(color='gray'), showlegend=False))
# , fillpattern=dict(shape="x",  fgcolor="black")

for i in range(len(x_bar)):
    fig.add_trace(go.Bar(x=[x_bar[i]], y=[y_bar[i]], width=widths[i], base=bases[i], text=labels[i], textposition='outside', textangle=0, name=labels[i]))


fig.update_xaxes(range=[0, sum_demand])

fig.update_layout(title=dict(text='Levelized costs of heating', font=dict(size=30)), xaxis=dict(title='Annual building heat demand in MWh', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='LCOH in $/MWh', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Buildings', font=dict(size=20)), legend=dict(font=dict(size=20)), barmode='overlay', bargap=0)

fig.show()

x_bar = []
y_bar = []
widths = []
bases = []
labels = []
index = 0

for building in building_lcoh_max_index:
    if building == building_lcoh_max_index[0]:
        x_bar.append(buildings_demand_sum[building] / 2)
        
    else:
        x_bar.append(x_bar[index-1] + buildings_demand_sum[building_lcoh_max_index[index-1]] / 2 + buildings_demand_sum[building] / 2)
    
    y_bar.append(max(buildings_lcoh[building]) - min(buildings_lcoh[building]))
    widths.append(buildings_demand_sum[building])
    bases.append(min(buildings_lcoh[building]))
    labels.append(f'{building}')
    index += 1

fig = go.Figure()

lcoh_min = min(lcoh, key=lcoh.get)
lcoh_max = max(lcoh, key=lcoh.get)

# for scenario in scenarios:
#     fig.add_trace(go.Scatter(x=[0, sum_demand], y=[lcoh[scenario], lcoh[scenario]], mode='lines', name=scenario))

fig.add_trace(go.Scatter(x=[0, sum_demand], y=[lcoh[lcoh_min], lcoh[lcoh_min]], mode='lines', line=dict(color='black'), name=lcoh_min, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_demand], y=[lcoh[lcoh_max], lcoh[lcoh_max]], mode='lines', line=dict(color='black'), name=lcoh_max, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_demand, sum_demand, 0], y=[lcoh[lcoh_min], lcoh[lcoh_min], lcoh[lcoh_max], lcoh[lcoh_max]],  fill='toself', fillcolor='gray', opacity=0.5, line=dict(color='gray'), showlegend=False))
# , fillpattern=dict(shape="x",  fgcolor="black")

for i in range(len(x_bar)):
    fig.add_trace(go.Bar(x=[x_bar[i]], y=[y_bar[i]], width=widths[i], base=bases[i], marker=dict(color='#FECB52'), showlegend=False))

fig.update_xaxes(range=[0, sum_demand])
fig.update_yaxes(range=[0, bases[0]+y_bar[0]+20])

fig.update_layout(title=dict(text='Levelized costs of heating', font=dict(size=30)), uniformtext_minsize=10, uniformtext_mode='show', xaxis=dict(title='Annual building heat demand in MWh', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='LCOH in $/MWh', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Buildings', font=dict(size=20)), legend=dict(font=dict(size=20)), barmode='overlay', bargap=0)

fig.show()

# FIG 4

# visualize_year = 2035

load_duration_curve_demand = heating_demand[visualize_year]

# load_duration_curve_demand = []

# for hour in hours:
#     load_duration_curve_demand_building = 0
    
#     for building in buildings_electricity:
#         load_duration_curve_demand_building += buildings_demand[building][hour] * buildings[building][visualize_year] / year_expansion_range[visualize_year]
    
#     load_duration_curve_demand.append(load_duration_curve_demand_building)

load_duration_curve_demand = [value / eta_electricity for value in load_duration_curve_demand]
load_duration_curve_demand.sort(reverse=True)
load_duration_curve = {}

for scenario in scenarios:
    load_duration_curve_scenario = []
    
    for t in hours:
        load_duration_curve_value = py.value(model.v_eb_q_elec_consumption[scenario, visualize_year, t]) + \
                                    py.value(model.v_hp_q_elec_consumption[scenario, visualize_year, t]) + \
                                    py.value(model.v_st_q_elec_consumption[scenario, visualize_year, t]) + \
                                    py.value(model.v_gt_q_elec_consumption[scenario, visualize_year, t]) + \
                                    py.value(model.v_dgt_q_heat_in[scenario, visualize_year, t] * 0.1) + \
                                    py.value(model.v_ieh_q_heat_in[scenario, visualize_year, t] * model.p_ieh_elec[scenario, visualize_year]) + \
                                    py.value(model.v_ates_q_elec_consumption[scenario, visualize_year, t]) + \
                                    py.value(model.v_ttes_q_elec_consumption[scenario, visualize_year, t])
    
        load_duration_curve_scenario.append(load_duration_curve_value)
        load_duration_curve_scenario.sort(reverse=True)
        
    load_duration_curve[scenario] = load_duration_curve_scenario

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_1['hour'], y=load_duration_curve_demand, mode='lines', fill='tozeroy', name='Buildings'))
fig.add_trace(go.Scatter(x=df_1['hour'], y=load_duration_curve[visualize_scenario], mode='lines', fill='tozeroy', name=visualize_scenario))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Electric energy per hour in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Profiles', font=dict(size=20)), legend=dict(font=dict(size=20)))

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