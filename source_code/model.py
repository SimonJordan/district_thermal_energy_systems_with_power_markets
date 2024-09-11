import os
import io
import sys
import time
import datetime
import numpy as np
import pandas as pd
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
# scenarios = ['0_basic', '3_non_neg_electricity_price', '5_zero_co2_price', '6_high_co2_price', '9_high_electricity_price_high_gas_price_high_co2_price']
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
path_to_result_folder = os.path.join(path_to_input_folder, 'results')

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
    data_eb[year] = {'p_eb_eta': p_eb_eta, 'p_eb_c_inv': p_eb_c_inv}
    p_hp_c_inv = df_hp['p_hp_c_inv'].tolist()[0]
    p_hp_cop = df_hp_cop['p_hp_cop'].tolist()
    data_hp[year] = {'p_hp_c_inv': p_hp_c_inv, 'p_hp_cop': p_hp_cop}
    p_st_eta = df_st['p_st_eta'].tolist()[0]
    p_st_c_inv = df_st['p_st_c_inv'].tolist()[0]
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
    data_wi[year] = {'p_wi_eta': p_wi_eta, 'p_wi_q_waste': p_wi_q_waste, 'p_wi_c_waste': p_wi_c_waste, 'p_wi_h_waste': p_wi_h_waste, 'p_wi_heat': p_wi_heat, 'p_wi_elec': p_wi_elec, 'p_wi_co2_share': p_wi_co2_share, 'p_wi_c_inv': p_wi_c_inv}
    p_gt_c_inv = df_gt['p_gt_c_inv'].tolist()[0]
    p_gt_cop = df_gt['p_gt_cop'].tolist()[0]
    data_gt[year] = {'p_gt_c_inv': p_gt_c_inv, 'p_gt_cop': p_gt_cop}
    p_dgt_c_inv = df_dgt['p_dgt_c_inv'].tolist()[0]
    data_dgt[year] = {'p_dgt_c_inv': p_dgt_c_inv}
    p_ieh_c_inv = df_ieh['p_ieh_c_inv'].tolist()[0]
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
data['0_basic'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
data['1_high_electricity_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['2_low_electricity_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['3_non_neg_electricity_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': {year: [max(0, value) for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: sum(values)/len(values) for year, values in {year: [max(0, value) for value in values] for year, values in electricity_price.items()}.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['4_high_gas_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': {year: [value * 1.3 for value in values] for year, values in gas_price.items()}, 'co2_price': co2_price, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['5_zero_co2_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': {year: value * 0 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['6_high_co2_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': {year: value * 1.5 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['7_half_investment_c'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': co2_price, 'eb': {year: {name: (value * 0.5 if name == 'p_eb_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_eb.items()}, 'hp': {year: {name: (value * 0.5 if name == 'p_hp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_hp.items()}, 'st': {year: {name: (value * 0.5 if name == 'p_st_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_st.items()}, 'wi': {year: {name: (value * 0.5 if name == 'p_wi_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_wi.items()}, 'gt': {year: {name: (value * 0.5 if name == 'p_gt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_gt.items()}, 'dgt': {year: {name: (value * 0.5 if name == 'p_dgt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_dgt.items()}, 'ieh': {year: {name: (value * 0.5 if name == 'p_ieh_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ieh.items()}, 'chp': {year: {name: (value * 0.5 if name == 'p_chp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_chp.items()}, 'ates': {year: {name: (value * 0.5 if name == 'p_ates_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ates.items()}, 'ttes': {year: {name: (value * 0.5 if name == 'p_ttes_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()}}
# data['8_low_electricity_price_high_co2_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': gas_price, 'co2_price': {year: value * 1.5 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
# data['9_high_electricity_price_high_gas_price_high_co2_price'] = {'year_expansion_range': year_expansion_range,'heating': heating_demand, 'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()}, 'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()}, 'electricity_co2_share': electricity_co2_share, 'electricity_mean_co2_share': electricity_mean_co2_share, 'gas_price': {year: [value * 1.3 for value in values] for year, values in gas_price.items()}, 'co2_price': {year: value * 1.5 for year, value in co2_price.items()}, 'eb': data_eb, 'hp': data_hp, 'st': data_st, 'wi': data_wi, 'gt': data_gt, 'dgt': data_dgt, 'ieh': data_ieh, 'chp': data_chp, 'ates': data_ates, 'ttes': data_ttes}
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
    return m.v_eb_q_heat_in[s, y, t] + m.v_hp_q_heat_in[s, y, t] + m.v_st_q_heat_in[s, y, t] + m.v_wi_q_heat_in[s, y, t] + m.v_gt_q_heat_in[s, y, t] + m.v_dgt_q_heat_in[s, y, t] + m.v_ieh_q_heat_in[s, y, t] + m.v_chp_q_heat_in[s, y, t] + m.v_ttes_q_thermal_in[s, y, t] - m.v_ttes_q_thermal_out[s, y, t]  + m.v_ates_q_thermal_in[s, y, t] - m.v_ates_q_thermal_out[s, y, t] == model.data_values[s]['heating'][y][t]

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
            file_name = '{}_{}.txt'.format(base_filename, file_index)
            file_path = os.path.join(path_to_input_folder, 'output', file_name)
            with open(file_path, 'w') as f:
                f.writelines(buffer)
            buffer = []
            bytes_written = 0
            file_index += 1
    if buffer:
        file_name = '{}_{}.txt'.format(base_filename, file_index)
        file_path = os.path.join(path_to_input_folder, 'output', file_name)
        with open(file_path, 'w') as f:
            f.writelines(buffer)

write_output_to_files(output, 'output', max_file_size)

print(solution)

#-----------------------------------------------------------------------------#
#                                                                             #
# storing relevant results in the folder results                              #
#                                                                             #
#-----------------------------------------------------------------------------#

path_to_file_scenarios = os.path.join(path_to_result_folder, 'scenarios.txt')

with open(path_to_file_scenarios, 'w') as file:
    for scenario in scenarios:
        file.write(scenario + '\n')

for scenario in scenarios:
    path_to_heat_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_heat_supply.xlsx')
    path_to_inv_capacity = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_capacity.xlsx')
    path_to_inv_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_cost.xlsx')
    path_to_fix_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_fix_cost.xlsx')
    path_to_var_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_var_cost.xlsx')
    path_to_elec_consumption = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_consumption.xlsx')
    path_to_elec_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_co2_share_gas_price.xlsx')
    path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
    
    df_0 = []
    df_1 = []
    df_2 = []
    df_3 = []
    df_4 = []
    df_5 = []
    df_6 = []
    df_7 = []
    
    for year in years:
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
        
        eb_c_inv = []
        hp_c_inv = []
        st_c_inv = []
        wi_c_inv = []
        gt_c_inv = []
        dgt_c_inv = []
        ieh_c_inv = []
        chp_c_inv = []
        ates_c_inv = []
        ttes_c_inv = []
        
        eb_c_fix = []
        hp_c_fix = []
        st_c_fix = []
        wi_c_fix = []
        gt_c_fix = []
        dgt_c_fix = []
        ieh_c_fix = []
        chp_c_fix = []
        ates_c_fix = []
        ttes_c_fix = []
        
        eb_c_var = []
        hp_c_var = []
        st_c_var = []
        wi_c_var = []
        gt_c_var = []
        dgt_c_var = []
        ieh_c_var = []
        chp_c_var = []
        ates_c_var = []
        ttes_c_var = []
        
        eb_elec = []
        hp_elec = []
        st_elec = []
        gt_elec = []
        ates_elec = []
        ttes_elec = []

        eb_inv.append(py.value(model.v_eb_Q_inv[scenario, year]))
        hp_inv.append(py.value(model.v_hp_Q_inv[scenario, year]))
        st_inv.append(py.value(model.v_st_P_inv[scenario, year]))
        wi_inv.append(py.value(model.v_wi_Q_inv[scenario, year]))
        gt_inv.append(py.value(model.v_gt_Q_inv[scenario, year]))
        dgt_inv.append(py.value(model.v_dgt_Q_inv[scenario, year]))
        ieh_inv.append(py.value(model.v_ieh_Q_inv[scenario, year]))
        chp_inv.append(py.value(model.v_chp_Q_inv[scenario, year]))
        ates_inv.append(py.value(model.v_ates_k_inv[scenario, year]))
        ttes_inv.append(py.value(model.v_ttes_k_inv[scenario, year]))
        
        eb_c_inv.append(py.value(model.v_eb_c_inv[scenario, year]))
        hp_c_inv.append(py.value(model.v_hp_c_inv[scenario, year]))
        st_c_inv.append(py.value(model.v_st_c_inv[scenario, year]))
        wi_c_inv.append(py.value(model.v_wi_c_inv[scenario, year]))
        gt_c_inv.append(py.value(model.v_gt_c_inv[scenario, year]))
        dgt_c_inv.append(py.value(model.v_dgt_c_inv[scenario, year]))
        ieh_c_inv.append(py.value(model.v_ieh_c_inv[scenario, year]))
        chp_c_inv.append(py.value(model.v_chp_c_inv[scenario, year]))
        ates_c_inv.append(py.value(model.v_ates_c_inv[scenario, year]))
        ttes_c_inv.append(py.value(model.v_ttes_c_inv[scenario, year]))
        
        eb_c_fix.append(py.value(model.v_eb_c_fix[scenario, year]))
        hp_c_fix.append(py.value(model.v_hp_c_fix[scenario, year]))
        st_c_fix.append(py.value(model.v_st_c_fix[scenario, year]))
        wi_c_fix.append(py.value(model.v_wi_c_fix[scenario, year]))
        gt_c_fix.append(py.value(model.v_gt_c_fix[scenario, year]))
        dgt_c_fix.append(py.value(model.v_dgt_c_fix[scenario, year]))
        ieh_c_fix.append(py.value(model.v_ieh_c_fix[scenario, year]))
        chp_c_fix.append(py.value(model.v_chp_c_fix[scenario, year]))
        ates_c_fix.append(py.value(model.v_ates_c_fix[scenario, year]))
        ttes_c_fix.append(py.value(model.v_ttes_c_fix[scenario, year]))
        
        for hour in hours:
            eb_in.append(py.value(model.v_eb_q_heat_in[scenario, year, hour]))
            hp_in.append(py.value(model.v_hp_q_heat_in[scenario, year, hour]))
            st_in.append(py.value(model.v_st_q_heat_in[scenario, year, hour]))
            wi_in.append(py.value(model.v_wi_q_heat_in[scenario, year, hour]))
            gt_in.append(py.value(model.v_gt_q_heat_in[scenario, year, hour]))
            dgt_in.append(py.value(model.v_dgt_q_heat_in[scenario, year, hour]))
            ieh_in.append(py.value(model.v_ieh_q_heat_in[scenario, year, hour]))
            chp_in.append(py.value(model.v_chp_q_heat_in[scenario, year, hour]))
            ates_in.append(py.value(model.v_ates_q_thermal_in[scenario, year, hour]))
            ates_out.append(-py.value(model.v_ates_q_thermal_out[scenario, year, hour]))
            ttes_in.append(py.value(model.v_ttes_q_thermal_in[scenario, year, hour]))
            ttes_out.append(-py.value(model.v_ttes_q_thermal_out[scenario, year, hour]))
            
            eb_c_var.append(py.value(model.v_eb_c_var[scenario, year, hour]))
            hp_c_var.append(py.value(model.v_hp_c_var[scenario, year, hour]))
            st_c_var.append(py.value(model.v_st_c_var[scenario, year, hour]))
            wi_c_var.append(py.value(model.v_wi_c_var[scenario, year, hour]))
            gt_c_var.append(py.value(model.v_gt_c_var[scenario, year, hour]))
            dgt_c_var.append(py.value(model.v_dgt_c_var[scenario, year, hour]))
            ieh_c_var.append(py.value(model.v_ieh_c_var[scenario, year, hour]))
            chp_c_var.append(py.value(model.v_chp_c_var[scenario, year, hour]))
            ates_c_var.append(py.value(model.v_ates_c_var[scenario, year, hour]))
            ttes_c_var.append(py.value(model.v_ttes_c_var[scenario, year, hour]))
            
            eb_elec.append(py.value(model.v_eb_q_elec_consumption[scenario, year, hour]))
            hp_elec.append(py.value(model.v_hp_q_elec_consumption[scenario, year, hour]))
            st_elec.append(py.value(model.v_st_q_elec_consumption[scenario, year, hour]))
            gt_elec.append(py.value(model.v_gt_q_elec_consumption[scenario, year, hour]))
            ates_elec.append(py.value(model.v_ates_q_elec_consumption[scenario, year, hour]))
            ttes_elec.append(py.value(model.v_ttes_q_elec_consumption[scenario, year, hour]))
            
        df_0.append(pd.DataFrame({'hour': hours, 'heating': heating_demand[year], 'eb': eb_in, 'hp': hp_in, 'st': st_in, 'wi': wi_in, 'gt': gt_in, 'dgt': dgt_in, 'ieh': ieh_in, 'chp': chp_in, 'ates+': ates_in, 'ates-': ates_out, 'ttes+': ttes_in, 'ttes-': ttes_out}))
        df_1.append(pd.DataFrame({'eb': eb_inv, 'hp': hp_inv, 'st': st_inv, 'wi': wi_inv, 'gt': gt_inv, 'dgt': dgt_inv, 'ieh': ieh_inv, 'chp': chp_inv, 'ates': ates_inv, 'ttes': ttes_inv}))
        df_2.append(pd.DataFrame({'eb': eb_c_inv, 'hp': hp_c_inv, 'st': st_c_inv, 'wi': wi_c_inv, 'gt': gt_c_inv, 'dgt': dgt_c_inv, 'ieh': ieh_c_inv, 'chp': chp_c_inv, 'ates': ates_c_inv, 'ttes': ttes_c_inv}))
        df_3.append(pd.DataFrame({'eb': eb_c_fix, 'hp': hp_c_fix, 'st': st_c_fix, 'wi': wi_c_fix, 'gt': gt_c_fix, 'dgt': dgt_c_fix, 'ieh': ieh_c_fix, 'chp': chp_c_fix, 'ates': ates_c_fix, 'ttes': ttes_c_fix}))
        df_4.append(pd.DataFrame({'eb': eb_c_var, 'hp': hp_c_var, 'st': st_c_var, 'wi': wi_c_var, 'gt': gt_c_var, 'dgt': dgt_c_var, 'ieh': ieh_c_var, 'chp': chp_c_var, 'ates': ates_c_var, 'ttes': ttes_c_var}))
        df_5.append(pd.DataFrame({'eb': eb_elec, 'hp': hp_elec, 'st': st_elec, 'gt': gt_elec, 'ates': ates_elec, 'ttes': ttes_elec}))
        df_6.append(pd.DataFrame({'elec': data[scenario]['electricity_price'][year], 'co2': data[scenario]['electricity_co2_share'][year], 'gas': data[scenario]['gas_price'][year]}))
        df_7.append(pd.DataFrame({'co2': [data[scenario]['co2_price'][year]]}, index=[year]))
    
    with pd.ExcelWriter(path_to_heat_supply) as writer:
        for df, year in zip(df_0, years):
            df.to_excel(writer, sheet_name=str(year), index=False)
            
    with pd.ExcelWriter(path_to_inv_capacity) as writer:
        for df, year in zip(df_1, years):
            df.to_excel(writer, sheet_name=str(year), index=False)
            
    with pd.ExcelWriter(path_to_inv_cost) as writer:
        for df, year in zip(df_2, years):
            df.to_excel(writer, sheet_name=str(year), index=False)
            
    with pd.ExcelWriter(path_to_fix_cost) as writer:
        for df, year in zip(df_3, years):
            df.to_excel(writer, sheet_name=str(year), index=False)
                    
    with pd.ExcelWriter(path_to_var_cost) as writer:
        for df, year in zip(df_4, years):
            df.to_excel(writer, sheet_name=str(year), index=False)

    with pd.ExcelWriter(path_to_elec_consumption) as writer:
        for df, year in zip(df_5, years):
            df.to_excel(writer, sheet_name=str(year), index=False)

    with pd.ExcelWriter(path_to_elec_gas_price) as writer:
        for df, year in zip(df_6, years):
            df.to_excel(writer, sheet_name=str(year), index=False)
            
    with pd.ExcelWriter(path_to_co2_price) as writer:
        for df, year in zip(df_7, years):
            df.to_excel(writer, sheet_name=str(year), index=False)

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

print('Script data exporting time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_3, minutes_3, seconds_3))

final_seconds = seconds_1 + seconds_2 + seconds_3
final_minutes = minutes_1 + minutes_2 + minutes_3 + final_seconds // 60
final_seconds = final_seconds % 60
final_hours = hours_1 + hours_2 + hours_3 + final_minutes // 60
final_minutes = final_minutes % 60

print('Script execution time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(final_hours, final_minutes, final_seconds))