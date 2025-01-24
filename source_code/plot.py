def plot_result():
    #%% set paths
    import os
    import numpy as np
    import pandas as pd
    
    cur_dir = os.path.dirname(__file__)
    path_to_input_folder = os.path.join(cur_dir, '..', 'inputs')
    path_to_result_folder = os.path.join(cur_dir, '..', 'results')
    path_to_visualization_folder = os.path.join(cur_dir, '..', 'visualizations')
    path_to_plot_folder = os.path.join(cur_dir, '..', 'plots')
    
    path_to_file_scenarios = os.path.join(path_to_result_folder, 'scenarios.txt')
    path_to_file_demand_cooling = os.path.join(path_to_input_folder, 'districts_cooling_demand_phase2.xlsx')
    path_to_file_demand_heating = os.path.join(path_to_input_folder, 'districts_heating_demand_phase2.xlsx')
    path_to_file_sum_cooling = os.path.join(path_to_visualization_folder, 'sum_cooling_demand_scenario.xlsx')
    path_to_file_sum_heating = os.path.join(path_to_visualization_folder, 'sum_heating_demand_scenario.xlsx')
    path_to_file_min_max_cooling = os.path.join(path_to_visualization_folder, 'min_max_scenario_cooling.xlsx')
    path_to_file_min_max_heating = os.path.join(path_to_visualization_folder, 'min_max_scenario_heating.xlsx')
    path_to_file_demands_per_scenario_year = os.path.join(path_to_visualization_folder, 'demands_per_scenario_year.xlsx')
    path_to_file_elec_consumption_per_scenario_year = os.path.join(path_to_visualization_folder, 'elec_consumption_per_scenario_year.xlsx')
    path_to_file_lcoc = os.path.join(path_to_visualization_folder, 'lcoc.xlsx')
    path_to_file_lcoh = os.path.join(path_to_visualization_folder, 'lcoh.xlsx')
    path_to_file_bar_all_info_cooling = os.path.join(path_to_visualization_folder, 'bar_all_info_cooling.xlsx')
    path_to_file_bar_all_info_heating = os.path.join(path_to_visualization_folder, 'bar_all_info_heating.xlsx')
    path_to_file_mean_all_info_cooling = os.path.join(path_to_visualization_folder, 'mean_all_info_cooling.xlsx')
    path_to_file_mean_all_info_heating = os.path.join(path_to_visualization_folder, 'mean_all_info_heating.xlsx')
    path_to_file_lcoc_buildings = os.path.join(path_to_visualization_folder, 'lcoc_buildings.xlsx')
    path_to_file_lcoh_buildings = os.path.join(path_to_visualization_folder, 'lcoh_buildings.xlsx')
    
    #%% create visualization data
    with open(path_to_file_scenarios, 'r') as file:
        scenarios = [line.strip() for line in file]
    
    data_demand_cooling = pd.read_excel(path_to_file_demand_cooling)
    data_demand_heating = pd.read_excel(path_to_file_demand_heating)
    
    sum_demand_cooling_general = data_demand_cooling['cooling_demand_sum'].sum()
    sum_demand_heating_general = data_demand_heating['heating_demand_sum'].sum()
    
    output_data_demand_cooling = pd.DataFrame({'sum_cooling_demand_scenario': [sum_demand_cooling_general]})
    output_data_demand_heating = pd.DataFrame({'sum_heating_demand_scenario': [sum_demand_heating_general]})
    
    output_data_demand_cooling.to_excel(path_to_file_sum_cooling, index=True)
    output_data_demand_heating.to_excel(path_to_file_sum_heating, index=True)
    
    years = [2025, 2030, 2035, 2040, 2045, 2050]
    year_expansion_range = {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1}
    hours = list(range(8760))
    column_cooling_technologies = {'ac': 1, 'ab_ct': 1, 'ab_hp': 1, 'cp_ct': 1, 'cp_hp': 0.5021779714, 'ites': 1}
    column_heating_technologies = {'eb': 1, 'hp': 1, 'st': 1, 'wi': 1, 'gt': 1, 'dgt': 1, 'ieh': 1, 'chp': 1, 'ab_hp': 0, 'cp_hp': 0.4978220286, 'ttes': 1}
    
    eta_gas = 0.9
    co2_conversion = 0.2
    eta_electricity_cooling = 3
    eta_electricity_heating = 0.99
    
    electricity_price = {}
    electricity_co2_share = {}
    gas_price = {}
    co2_price = {}
    
    for scenario in scenarios:
        electricity_price_scenario = {}
        electricity_co2_share_scenario = {}
        gas_price_scenario = {}
        co2_price_scenario = {}
        
        path_to_elec_price_co2_share_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_co2_share_gas_price.xlsx')
        path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
        
        
        for year in years:
            df_elec_price_co2_share_gas_price = pd.read_excel(path_to_elec_price_co2_share_gas_price, sheet_name=str(year))
            df_co2_price = pd.read_excel(path_to_co2_price, sheet_name=str(year))
            
            electricity_price_scenario[year] = df_elec_price_co2_share_gas_price['elec'].tolist()
            electricity_co2_share_scenario[year] = df_elec_price_co2_share_gas_price['co2'].tolist()
            gas_price_scenario[year] = df_elec_price_co2_share_gas_price['gas'].tolist()
            co2_price_scenario[year] = df_co2_price['co2'].tolist()[0]
            
        electricity_price[scenario] = electricity_price_scenario
        electricity_co2_share[scenario] = electricity_co2_share_scenario
        gas_price[scenario] = gas_price_scenario
        co2_price[scenario] = co2_price_scenario
    
    sum_cost_cooling = {}
    sum_cost_heating = {}
    
    for scenario in scenarios:
        path_to_file_inv_cost = os.path.join(path_to_result_folder, f'[{scenario}]_#_inv_cost.xlsx')
        path_to_file_fix_cost = os.path.join(path_to_result_folder, f'[{scenario}]_#_fix_cost.xlsx')
        path_to_file_var_cost = os.path.join(path_to_result_folder, f'[{scenario}]_#_var_cost.xlsx')
        
        sum_inv_cost_cooling_scenario = 0
        sum_inv_cost_heating_scenario = 0
        sum_fix_cost_cooling_scenario = 0
        sum_fix_cost_heating_scenario = 0
        sum_var_cost_cooling_scenario = 0
        sum_var_cost_heating_scenario = 0
        sum_cost_cooling_scenario = 0
        sum_cost_heating_scenario = 0
    
        for year in years:
            df_inv_cost = pd.read_excel(path_to_file_inv_cost, sheet_name=str(year))
            df_fix_cost = pd.read_excel(path_to_file_fix_cost, sheet_name=str(year))
            df_var_cost = pd.read_excel(path_to_file_var_cost, sheet_name=str(year))    
        
            sum_inv_cost_cooling_sheet = 0
            sum_inv_cost_heating_sheet = 0
            sum_fix_cost_cooling_sheet = 0
            sum_fix_cost_heating_sheet = 0
            sum_var_cost_cooling_sheet = 0
            sum_var_cost_heating_sheet = 0
            
            for column in df_inv_cost.columns:
                if column in column_cooling_technologies:
                    sum_inv_cost_cooling_sheet += df_inv_cost[column].iloc[0] * column_cooling_technologies[column]
                
                if column in column_heating_technologies:
                    sum_inv_cost_heating_sheet += df_inv_cost[column].iloc[0] * column_heating_technologies[column]
                
            for column in df_fix_cost.columns:
                if column in column_cooling_technologies:
                    sum_fix_cost_cooling_sheet += df_fix_cost[column].iloc[0] * column_cooling_technologies[column]
                
                if column in column_heating_technologies:
                    sum_fix_cost_heating_sheet += df_fix_cost[column].iloc[0] * column_heating_technologies[column]
                    
            for column in df_var_cost.columns:
                if column in column_cooling_technologies:
                    sum_var_cost_cooling_sheet += df_var_cost[column].sum() * column_cooling_technologies[column]
                
                if column in column_heating_technologies:
                    sum_var_cost_heating_sheet += df_var_cost[column].sum() * column_heating_technologies[column]
            
            sum_inv_cost_cooling_scenario += sum_inv_cost_cooling_sheet
            sum_inv_cost_heating_scenario += sum_inv_cost_heating_sheet
            sum_fix_cost_cooling_scenario += sum_fix_cost_cooling_sheet
            sum_fix_cost_heating_scenario += sum_fix_cost_heating_sheet 
            sum_var_cost_cooling_scenario += sum_var_cost_cooling_sheet
            sum_var_cost_heating_scenario += sum_var_cost_heating_sheet
        
        sum_cost_cooling_scenario = sum_inv_cost_cooling_scenario + sum_fix_cost_cooling_scenario + sum_var_cost_cooling_scenario
        sum_cost_heating_scenario = sum_inv_cost_heating_scenario + sum_fix_cost_heating_scenario + sum_var_cost_heating_scenario
        
        sum_cost_cooling[scenario] = sum_cost_cooling_scenario
        sum_cost_heating[scenario] = sum_cost_heating_scenario
    
    min_cooling_scenario = min(sum_cost_cooling, key=sum_cost_cooling.get)
    max_cooling_scenario = max(sum_cost_cooling, key=sum_cost_cooling.get)  
    min_heating_scenario = min(sum_cost_heating, key=sum_cost_heating.get)
    max_heating_scenario = max(sum_cost_heating, key=sum_cost_heating.get)  
    
    output_min_max_scenario_cooling = pd.DataFrame({'min': [min_cooling_scenario], 'max': [max_cooling_scenario]})
    output_min_max_scenario_heating = pd.DataFrame({'min': [min_heating_scenario], 'max': [max_heating_scenario]})
    
    output_min_max_scenario_cooling.to_excel(path_to_file_min_max_cooling, index=True)
    output_min_max_scenario_heating.to_excel(path_to_file_min_max_heating, index=True)
    
    sum_demand_cooling = {}
    sum_demand_heating = {}
    
    thermal_energy_type_list = []
    years_list = []
    scenarios_list = []
    values_list = []
    
    for scenario in scenarios:
        path_to_file_cool_supply = os.path.join(path_to_result_folder, f'[{scenario}]_#_cool_supply.xlsx')
        path_to_file_heat_supply = os.path.join(path_to_result_folder, f'[{scenario}]_#_heat_supply.xlsx')
        
        sum_demand_cooling_scenario = 0
        sum_demand_heating_scenario = 0
        
        for year in years:
            df_cool_supply = pd.read_excel(path_to_file_cool_supply, sheet_name=str(year))
            df_heat_supply = pd.read_excel(path_to_file_heat_supply, sheet_name=str(year))
            
            for thermal_energy_type in ['Heating', 'Cooling']:
                thermal_energy_type_list.append(thermal_energy_type)
                years_list.append(str(year))
                scenarios_list.append(scenario)
                
                if thermal_energy_type == 'Cooling':
                    values_list.append(df_cool_supply['cooling'].sum())
                    sum_demand_cooling_scenario += df_cool_supply['cooling'].sum() * year_expansion_range[year]
                
                if thermal_energy_type == 'Heating':
                    values_list.append(df_heat_supply['heating'].sum())
                    sum_demand_heating_scenario += df_heat_supply['heating'].sum() * year_expansion_range[year]
    
        sum_demand_cooling[scenario] = sum_demand_cooling_scenario
        sum_demand_heating[scenario] = sum_demand_heating_scenario
    
    output_demands_per_scenario_year = pd.DataFrame({'Type': thermal_energy_type_list, 'Year': years_list, 'Scenarios': scenarios_list, 'Values': values_list})
    
    output_demands_per_scenario_year.to_excel(path_to_file_demands_per_scenario_year, index=True)
    
    thermal_energy_type_list = []
    years_list = []
    scenarios_list = []
    values_list = []
    
    for scenario in scenarios:
        path_to_file_elec_consumption = os.path.join(path_to_result_folder, f'[{scenario}]_#_elec_consumption.xlsx')
        path_to_file_inv_capacity = os.path.join(path_to_result_folder, f'[{scenario}]_#_inv_capacity.xlsx')
        
        ites_capacity = 0
        ttes_capacity = 0
        
        for year in years:
            df_elec_consumption = pd.read_excel(path_to_file_elec_consumption, sheet_name=str(year))
            df_inv_capacity = pd.read_excel(path_to_file_inv_capacity, sheet_name=str(year))
            
            sum_elec_consumption_cooling_sheet = 0
            sum_elec_consumption_heating_sheet = 0
            
            for column in df_elec_consumption.columns:
                if column in column_cooling_technologies:
                    sum_elec_consumption_cooling_sheet += df_elec_consumption[column].sum() * column_cooling_technologies[column]
                    
                    if column == 'ites':
                        ites_capacity += df_inv_capacity[column].iloc[0]
                        sum_elec_consumption_cooling_sheet += ites_capacity * 0.01
                
                if column in column_heating_technologies:
                    sum_elec_consumption_heating_sheet += df_elec_consumption[column].sum() * column_heating_technologies[column]
                    
                    if column == 'ttes':
                        ttes_capacity += df_inv_capacity[column].iloc[0]
                        sum_elec_consumption_heating_sheet += ttes_capacity * 0.01
            
            for thermal_energy_type in ['Heating', 'Cooling']:
                thermal_energy_type_list.append(thermal_energy_type)
                years_list.append(str(year))
                scenarios_list.append(scenario)
                
                if thermal_energy_type == 'Cooling':
                    values_list.append(sum_elec_consumption_cooling_sheet)
                
                if thermal_energy_type == 'Heating':
                    values_list.append(sum_elec_consumption_heating_sheet)
        
    output_elec_consumption = pd.DataFrame({'Type': thermal_energy_type_list, 'Year': years_list, 'Scenarios': scenarios_list, 'Values': values_list})
    
    output_elec_consumption.to_excel(path_to_file_elec_consumption_per_scenario_year, index=True)
    
    lcoc = {}
    lcoh = {}
    
    for scenario in scenarios:
        lcoc[scenario] = [sum_cost_cooling[scenario] / sum_demand_cooling[scenario]]
        lcoh[scenario] = [sum_cost_heating[scenario] / sum_demand_heating[scenario]]
    
    output_lcoc = pd.DataFrame(lcoc)
    output_lcoh = pd.DataFrame(lcoh)
    
    output_lcoc.to_excel(path_to_file_lcoc, index=True)
    output_lcoh.to_excel(path_to_file_lcoh, index=True)
    
    buildings_gas = []
    buildings_electricity = [11, 16, 19, 30, 37]
    
    for building in range(1, 36):
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
                 35: {2025: 0, 2030: 0, 2035: 5, 2040: 5, 2045: 5, 2050: 1}}
    
    demand_cool_variation = {'1_reference': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '2_high_electricity_prices': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '3_low_electricity_prices': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '4_flexible_energy_market': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '5_energy_congestion': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '6_green_friendly': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '7_low_gas_demand': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '8_natural_gas_friendly': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '9_cold_winters': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '10_hot_summers': {2025: 1, 2030: 1.1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '11_warm_summers': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1.05, 2050: 1.05},
                             '12_moderate_climate': {2025: 0.9, 2030: 0.9, 2035: 0.9, 2040: 0.9, 2045: 0.9, 2050: 0.9},
                             '13_zero_co2_price': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '14_delayed_co2_pricing': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '15_ambitious_co2_pricing': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '16_expiring_support_res': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1}}
    
    demand_heat_variation = {'1_reference': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '2_high_electricity_prices': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '3_low_electricity_prices': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '4_flexible_energy_market': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '5_energy_congestion': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '6_green_friendly': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '7_low_gas_demand': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '8_natural_gas_friendly': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '9_cold_winters': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1.1, 2050: 1.1},
                             '10_hot_summers': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '11_warm_summers': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '12_moderate_climate': {2025: 0.9, 2030: 0.9, 2035: 0.9, 2040: 0.9, 2045: 0.9, 2050: 0.9},
                             '13_zero_co2_price': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '14_delayed_co2_pricing': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '15_ambitious_co2_pricing': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1},
                             '16_expiring_support_res': {2025: 1, 2030: 1, 2035: 1, 2040: 1, 2045: 1, 2050: 1}}
    
    demand_cool_sum_variation = {}
    demand_heat_sum_variation = {}
    
    for building in range(1, 35):
        variation = 0
        
        for scenario in scenarios:
                
            for year in years:
                variation += buildings[building][year] * demand_cool_variation[scenario][year]
        
        demand_cool_sum_variation[building] = variation / len(scenarios)
    
    for building in range(1, 36):
        variation = 0
        
        for scenario in scenarios:
                
            for year in years:
                variation += buildings[building][year] * demand_heat_variation[scenario][year]
        
        demand_heat_sum_variation[building] = variation / len(scenarios)
    
    buildings_demand = {}
    buildings_demand_sum = {}
    buildings_lcoc = {}
    
    for building in range(1, 35):
        cooling_demand_building = data_demand_cooling[f'cooling_demand_building_{building}'].tolist()
        buildings_demand[building] = cooling_demand_building
        buildings_demand_sum[building] = sum(cooling_demand_building)
    
    for building in range(1, 35):
        buildings_lcoc_scenario = []
        for scenario in scenarios:
            building_c_sum = 0
            
            for year in years:
                for hour in hours:
                    building_c_sum += buildings[building][year] * demand_cool_variation[scenario][year] * buildings_demand[building][hour] / eta_electricity_cooling * (electricity_price[scenario][year][hour] + electricity_co2_share[scenario][year][hour] * co2_price[scenario][year])
                
            buildings_lcoc_scenario.append(building_c_sum / (buildings_demand_sum[building] * demand_cool_sum_variation[building]))
    
        buildings_lcoc[building] = buildings_lcoc_scenario
    
    building_lcoc_max = []
    building_lcoc_min = []
    building_lcoc_avg = []
    
    for building in range(1, 35):
        building_lcoc_max.append(max(buildings_lcoc[building]))
        building_lcoc_min.append(min(buildings_lcoc[building]))
        building_lcoc_avg.append(np.mean([min(buildings_lcoc[building]), max(buildings_lcoc[building])]))
    
    building_lcoc_max_index = [i + 1 for i in sorted(range(len(building_lcoc_max)), key=lambda i: building_lcoc_max[i], reverse=True)]
    
    x_bar = []
    x_mean = []
    y_bar = []
    widths = []
    bases = []
    labels = []
    index = 0
    
    for building in building_lcoc_max_index:
        if building == building_lcoc_max_index[0]:
            x_bar.append(buildings_demand_sum[building] / 2)
            
        else:
            x_bar.append(x_bar[index-1] + buildings_demand_sum[building_lcoc_max_index[index-1]] / 2 + buildings_demand_sum[building] / 2)
        
        y_bar.append(max(buildings_lcoc[building]) - min(buildings_lcoc[building]))
        widths.append(buildings_demand_sum[building])
        bases.append(min(buildings_lcoc[building]))
        labels.append(f'{building}')
        index += 1
    
    mean_cool = {key: sum(values) / len(values) for key, values in buildings_lcoc.items()}
    #mean_cool_sorted = {key: mean_cool[key] for key in building_lcoc_max_index if key in mean_cool}
    mean_cool_sorted = {key: value for key, value in sorted(mean_cool.items(), key=lambda item: item[1], reverse=True)}
    
    index = 0
    
    for building in list(mean_cool_sorted.keys()):
        if building == list(mean_cool_sorted.keys())[0]:
            x_mean.append(buildings_demand_sum[building] / 2)
            
        else:
            x_mean.append(x_mean[index-1] + buildings_demand_sum[list(mean_cool_sorted.keys())[index-1]] / 2 + buildings_demand_sum[building] / 2)

        index += 1
    
    output_bar_cooling = pd.DataFrame({'x_bar': x_bar, 'y_bar': y_bar, 'widths': widths, 'bases': bases, 'labels': labels})
    output_mean_cooling = pd.DataFrame({'labels': list(mean_cool_sorted.keys()), 'x_mean': x_mean, 'y_mean': list(mean_cool_sorted.values())})
    
    output_bar_cooling.to_excel(path_to_file_bar_all_info_cooling, index=True)
    output_mean_cooling.to_excel(path_to_file_mean_all_info_cooling, index=True)
    
    buildings_demand = {}
    buildings_demand_sum = {}
    buildings_lcoh = {}
    
    for building in range(1, 36):
        heating_demand_building = data_demand_heating[f'heating_demand_building_{building}'].tolist()
        buildings_demand[building] = heating_demand_building
        buildings_demand_sum[building] = sum(heating_demand_building)
    
    for building in range(1, 36):
        buildings_lcoh_scenario = []
        for scenario in scenarios:
            building_c_sum = 0
            
            for year in years:
                for hour in hours:
                    if building in buildings_gas:
                        building_c_sum += buildings[building][year] * demand_heat_variation[scenario][year] * buildings_demand[building][hour] / eta_gas * (gas_price[scenario][year][hour] + co2_conversion * co2_price[scenario][year])
                        
                    else:
                        building_c_sum += buildings[building][year] * demand_heat_variation[scenario][year] * buildings_demand[building][hour] / eta_electricity_heating * (electricity_price[scenario][year][hour] + electricity_co2_share[scenario][year][hour] * co2_price[scenario][year])
                
            buildings_lcoh_scenario.append(building_c_sum / (buildings_demand_sum[building] * demand_heat_sum_variation[building]))
    
        buildings_lcoh[building] = buildings_lcoh_scenario
    
    building_lcoh_max = []
    building_lcoh_min = []
    building_lcoh_avg = []
    
    for building in range(1, 36):
        building_lcoh_max.append(max(buildings_lcoh[building]))
        building_lcoh_min.append(min(buildings_lcoh[building]))
        building_lcoh_avg.append(np.mean([min(buildings_lcoh[building]), max(buildings_lcoh[building])]))
    
    building_lcoh_max_index = [i + 1 for i in sorted(range(len(building_lcoh_max)), key=lambda i: building_lcoh_max[i], reverse=True)]
    
    x_bar = []
    x_mean = []
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
    
    mean_heat = {key: sum(values) / len(values) for key, values in buildings_lcoh.items()}
    #mean_heat_sorted = {key: mean_heat[key] for key in building_lcoh_max_index if key in mean_heat}
    mean_heat_sorted = {key: value for key, value in sorted(mean_heat.items(), key=lambda item: item[1], reverse=True)}
   
    index = 0
    
    for building in list(mean_heat_sorted.keys()):
        if building == list(mean_heat_sorted.keys())[0]:
            x_mean.append(buildings_demand_sum[building] / 2)
            
        else:
            x_mean.append(x_mean[index-1] + buildings_demand_sum[list(mean_heat_sorted.keys())[index-1]] / 2 + buildings_demand_sum[building] / 2)

        index += 1
    
    output_bar_heating = pd.DataFrame({'x_bar': x_bar, 'y_bar': y_bar, 'widths': widths, 'bases': bases, 'labels': labels})
    output_mean_heating = pd.DataFrame({'labels': list(mean_heat_sorted.keys()), 'x_mean': x_mean, 'y_mean': list(mean_heat_sorted.values())})
    
    output_bar_heating.to_excel(path_to_file_bar_all_info_heating, index=True)
    output_mean_heating.to_excel(path_to_file_mean_all_info_heating, index=True)
    
    output_lcoc_buildings = pd.DataFrame.from_dict(buildings_lcoc, orient='index', columns=scenarios)
    output_lcoh_buildings = pd.DataFrame.from_dict(buildings_lcoh, orient='index', columns=scenarios)
    
    output_lcoc_buildings.to_excel(path_to_file_lcoc_buildings, index=True)
    output_lcoh_buildings.to_excel(path_to_file_lcoh_buildings, index=True)
    
    #%% original
    # import pyam as py
    import matplotlib.pyplot as plt
    import os
    #import matplotlib.patches as mpatches
    import matplotlib.ticker as ticker
    import numpy as np
    #from matplotlib.ticker import FuncFormatter
    import pandas as pd
    #from matplotlib.patches import FancyBboxPatch
    # import matplotlib.ticker as ticker
    
    
    def format_thousands(x, pos):
        """
        Format the tick labels with a space between thousands.
        """
        return "{:,.0f}".format(x).replace(",", " ")
    
    
    #_font = 16
    plt.style.use("default")
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    
    _colors = {
        "eb": "#E6D9A2",
        "ieh": "#c51b8a",
        "gt": "#7a0177",
        "hp": "#CDC1FF",
        "cp_hp+": "#006BFF",
        "ttes+": "#feebe2",
        "ac": "#BCF2F6",
        "cp_ct": "#08C2FF",
        "cp_hp": "#006BFF",
        "ites+": "#D2E0FB",
    }
    
    _factor = 1.35
    
    data = pd.read_excel(os.path.join(path_to_result_folder, '[1_reference]_#_inv_capacity.xlsx'), sheet_name=None)
    _technologies = data["2025"].columns
    
    newly_installed_capacities = dict()
    
    for _tech in _technologies:
        newly_installed_capacities[_tech] = [
            np.around(data[year][_tech].iloc[0] * 1000, 2) for year in data.keys()
        ]
    
    for _key in _technologies:
        if sum(newly_installed_capacities[_key]) == 0:
            newly_installed_capacities.pop(_key)
        else:
            pass
    
    
    ###############################################################################
    ####### COOLING GENERATION TECHNOLOGIES
    ###############################################################################
    
    fig, ax = plt.subplots(figsize=(_factor * 4, _factor * 3))
    x_axis = [int(key) for key in data.keys()]
    _width = 2
    
    _bottom = np.zeros(len(x_axis))
    for _key, _label, _color in [
        ["ac", "Air-cooled chiller", "#BCF2F6"],
        ["ab_ct", "Absorber (+ cold tower)", "red"],
        ["ab_hp", "Absorber (+ hp)", "red"],
        ["cp_ct", "Water-cooled chiller", "#08C2FF"],
        ["cp_hp", "Heat recovery chiller", "#006BFF"],
    ]:
        if _key in newly_installed_capacities.keys():
            ax.bar(
                x_axis,
                newly_installed_capacities[_key],
                _width,
                label=_label,
                color=_color,
                bottom=_bottom,
                linewidth=0.5,
                zorder=2,
                edgecolor="black",
            )
            _bottom = np.add(_bottom, newly_installed_capacities[_key])
        else:
            pass
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    _legend.get_frame().set_linewidth(0.5)
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.yaxis.set_major_formatter(formatter)
    
    ax.set_ylabel("Cold generation additions (in kW)", fontsize=15)
    
    plt.tight_layout()
    fig.savefig(os.path.join(path_to_plot_folder, "Newly_installed_cooling_generation_capacities.pdf"), dpi=1000)
    
    
    ###############################################################################
    ####### HEATING GENERATION TECHNOLOGIES
    ###############################################################################
    
    fig, ax = plt.subplots(figsize=(_factor * 4, _factor * 3))
    x_axis = [int(key) for key in data.keys()]
    _width = 2
    
    _bottom = np.zeros(len(x_axis))
    for _key, _label, _color in [
        ["eb", "Electric boiler", "#E6D9A2"],
        ["hp", "Air-source HP", "#CDC1FF"],
        ["ieh", "Excess heat", "#c51b8a"],
        ["gt", "Geothermal HP", "#7a0177"],
    ]:
        if _key in newly_installed_capacities.keys():
            ax.bar(
                x_axis,
                newly_installed_capacities[_key],
                _width,
                label=_label,
                color=_color,
                bottom=_bottom,
                linewidth=0.5,
                zorder=2,
                edgecolor="black",
            )
            _bottom = np.add(_bottom, newly_installed_capacities[_key])
        else:
            pass
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    _legend.get_frame().set_linewidth(0.5)
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.yaxis.set_major_formatter(formatter)
    
    ax.set_ylabel("Heat generation additions (in kW)", fontsize=15)
    
    plt.tight_layout()
    fig.savefig(os.path.join(path_to_plot_folder, "Newly_installed_heating_generation_capacities.pdf"), dpi=1000)
    
    ###############################################################################
    ####### COOLING STORAGE SYSTEMS
    ###############################################################################
    
    fig, ax = plt.subplots(figsize=(_factor * 4, _factor * 3))
    x_axis = [int(key) for key in data.keys()]
    _width = 2
    
    _bottom = np.zeros(len(x_axis))
    for _key, _label, _color in [
        ["ites", "Ice TES", "#D2E0FB"],
    ]:
        final = list(map(lambda x: x / 1000, newly_installed_capacities[_key]))
    
        if _key in newly_installed_capacities.keys():
            ax.bar(
                x_axis,
                final,
                _width,
                label=_label,
                color=_color,
                bottom=_bottom,
                linewidth=0.5,
                zorder=2,
                edgecolor="black",
            )
            _bottom = np.add(_bottom, final)
        else:
            pass
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    _legend.get_frame().set_linewidth(0.5)
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.yaxis.set_major_formatter(formatter)
    
    ax.set_ylim([0, 6.25])
    
    ax.set_ylabel("Cold storage additions (in MWh)", fontsize=15)
    
    plt.tight_layout()
    fig.savefig(os.path.join(path_to_plot_folder, "Newly_installed_cooling_storage_capacities.pdf"), dpi=1000)
    
    ###############################################################################
    ####### HEATING STORAGE SYSTEMS
    ###############################################################################
    
    fig, ax = plt.subplots(figsize=(_factor * 4, _factor * 3))
    x_axis = [int(key) for key in data.keys()]
    _width = 2
    
    _bottom = np.zeros(len(x_axis))
    for _key, _label, _color in [
        ["ttes", "Tank TES", "#feebe2"],
    ]:
        final = list(map(lambda x: x / 1000, newly_installed_capacities[_key]))
    
        if _key in newly_installed_capacities.keys():
            ax.bar(
                x_axis,
                final,
                _width,
                label=_label,
                color=_color,
                bottom=_bottom,
                linewidth=0.5,
                zorder=2,
                edgecolor="black",
            )
            _bottom = np.add(_bottom, final)
        else:
            pass
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    _legend.get_frame().set_linewidth(0.5)
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.yaxis.set_major_formatter(formatter)
    
    ax.set_ylabel("Heat storage additions (in MWh)", fontsize=15)
    
    plt.tight_layout()
    fig.savefig(os.path.join(path_to_plot_folder, "Newly_installed_heating_storage_capacities.pdf"), dpi=1000)
    
    ###############################################################################
    ####### HEAT DURATION CURVE
    ###############################################################################
    
    generation = pd.read_excel(os.path.join(path_to_result_folder, '[1_reference]_#_heat_supply.xlsx'), sheet_name="2035")
    
    hours = generation["hour"]
    #demand_old = generation["heating"]
    demand = generation["heating"] - generation["ttes-"]
    
    generation.drop(columns="ttes-", inplace=True)
    
    fig, ax = plt.subplots(figsize=(_factor * 4, _factor * 3))
    ax.plot(
        hours,
        sorted(demand, reverse=True),
        linestyle="dashed",
        color="black",
        label="Demand",
    )
    
    ax.set_ylabel("Heat duration curve (in MWh)", fontsize=15)
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    _dict_results = dict()
    
    for _col in generation:
        if _col == "hour":
            pass
        elif _col == "heating":
            pass
        elif sum(generation[_col]) == 0:
            pass
        else:
            _dict_results[_col] = sorted(generation[_col], reverse=True)
    
    
    non_zero_counts = {
        key: sum(1 for x in values if x != 0) for key, values in _dict_results.items()
    }
    sorted_keys = sorted(non_zero_counts, key=non_zero_counts.get, reverse=True)
    _dict_colors = []
    
    for key in sorted_keys:
        if key in _colors.keys():
            _dict_colors.append(_colors.get(key))
        else:
            _dict_colors.append("blue")
    
    sorted_data = [_dict_results[key] for key in sorted_keys]
    
    for _index, _name in enumerate(sorted_keys):
        if _name == "eb":
            sorted_keys[_index] = "Electric boiler"
        elif _name == "ieh":
            sorted_keys[_index] = "Excess heat"
        elif _name == "gt":
            sorted_keys[_index] = "Geothermal HP"
        elif _name == "cp_hp+":
            sorted_keys[_index] = "Heat recovery chiller"
        elif _name == "hp":
            sorted_keys[_index] = "Air-source HP"
        elif _name == "ttes+":
            sorted_keys[_index] = "Tank TES"
    
    
    x = np.arange(len(next(iter(_dict_results.values()))))
    
    ax.stackplot(x, *sorted_data, labels=sorted_keys, colors=_dict_colors)
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=0,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    handles, labels = ax.get_legend_handles_labels()
    
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    
    _legend = ax.legend(
        handles=handles,
        labels=labels,
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.set_ylim([0, 4.15])
    
    plt.tight_layout()
    fig.savefig(os.path.join(path_to_plot_folder, "Load_duration_curve_heating.pdf"), dpi=1000)
    
    ###############################################################################
    ####### COLD DURATION CURVE
    ###############################################################################
    
    
    generation = pd.read_excel(os.path.join(path_to_result_folder, '[1_reference]_#_cool_supply.xlsx'), sheet_name="2035")
    
    hours = generation["hour"]
    demand = generation["cooling"] - generation["ites-"]
    
    generation.drop(columns="ites-", inplace=True)
    
    
    fig, ax = plt.subplots(figsize=(_factor * 4, _factor * 3))
    ax.plot(
        hours,
        sorted(demand, reverse=True),
        linestyle="dashed",
        color="black",
        label="Demand",
    )
    
    ax.set_ylabel("Cold duration curve (in MWh)", fontsize=15)
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    _dict_results = dict()
    
    for _col in generation:
        if _col == "hour":
            pass
        elif _col == "cooling":
            pass
        elif sum(generation[_col]) == 0:
            pass
        else:
            _dict_results[_col] = sorted(generation[_col], reverse=True)
    
    
    non_zero_counts = {
        key: sum(1 for x in values if x != 0) for key, values in _dict_results.items()
    }
    sorted_keys = sorted(non_zero_counts, key=non_zero_counts.get, reverse=True)
    _dict_colors = []
    
    for key in sorted_keys:
        if key in _colors.keys():
            _dict_colors.append(_colors.get(key))
        else:
            _dict_colors.append("blue")
    
    sorted_data = [_dict_results[key] for key in sorted_keys]
    
    for _index, _name in enumerate(sorted_keys):
        if _name == "ac":
            sorted_keys[_index] = "Air-cooled chiller"
        elif _name == "cp_ct":
            sorted_keys[_index] = "Water-cooled chiller"
        elif _name == "cp_hp":
            sorted_keys[_index] = "Heat recovery chiller"
        elif _name == "ites+":
            sorted_keys[_index] = "Ice TES"
        elif _name == "hp":
            sorted_keys[_index] = "HP (AS)"
        elif _name == "ttes+":
            sorted_keys[_index] = "Tank TES"
    
    
    x = np.arange(len(next(iter(_dict_results.values()))))
    
    ax.stackplot(x, *sorted_data, labels=sorted_keys, colors=_dict_colors)
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=0,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    handles, labels = ax.get_legend_handles_labels()
    
    # Sort labels alphabetically, but ensure 'Demand' comes first
    # labels, handles = zip(
    #     *sorted(
    #         zip(labels, handles),
    #         key=lambda t: (
    #             0 if t[0] == "Demand" else 1,
    #             t[0],
    #         ),  # 'Demand' gets priority (0)
    #     )
    # )
    
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        
    _legend = ax.legend(
        handles=handles,
        labels=labels,
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    ax.set_ylim([0, 4.15])
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Load_duration_curve_cooling.pdf"), dpi=1000)
    
    
    ###############################################################################
    ####### LEVELIZED COST OF HEATING COMPARISON
    ###############################################################################
    
    bar_all_info = pd.read_excel(os.path.join(path_to_visualization_folder, 'bar_all_info_heating.xlsx'), sheet_name="Sheet1", index_col=0)
    lcoh = pd.read_excel(os.path.join(path_to_visualization_folder, 'lcoh.xlsx'), sheet_name="Sheet1", index_col=0)
    minmaxscenario = pd.read_excel(os.path.join(path_to_visualization_folder, 'min_max_scenario_heating.xlsx'), sheet_name="Sheet1", index_col=0)
    sum_heating_demand_scenario = pd.read_excel(os.path.join(path_to_visualization_folder, 'sum_heating_demand_scenario.xlsx'), sheet_name="Sheet1", index_col=0)["sum_heating_demand_scenario"]
    
    
    fig, ax = plt.subplots(figsize=(_factor * 6, _factor * 3))
    lcoh_min = minmaxscenario["min"]
    lcoh_max = minmaxscenario["max"]
    
    dh_max = lcoh[lcoh_max].iloc[0].item()
    dh_min = lcoh[lcoh_min].iloc[0].item()
    
    _color = "#F09319"
    ax.plot(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [dh_max, dh_max],
        color=_color,
        linestyle="solid",
    )
    ax.plot(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [dh_min, dh_min],
        color=_color,
        linestyle="solid",
    )
    ax.fill_between(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [dh_min, dh_min],
        [dh_max, dh_max],
        color=_color,
        alpha=0.5,
        zorder=4,
        label="District heating",
    )
    
    _dict = {0: "Buildings 1-35"}
    
    for index, row in bar_all_info.iterrows():
        _x_offset = sum(bar_all_info.widths[0:index])
        ax.fill_between(
            [_x_offset, _x_offset + row.widths],
            [row.bases, row.bases],
            [row.bases + row.y_bar, row.bases + row.y_bar],
            color="#3D5300",
            edgecolor="#FFE5CF",
            linewidth=0.15,
            zorder=0,
            label=_dict.get(index, None),
        )
    
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    # ax.set_ylim([0, 4.15])
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.set_ylabel("Min-Max range of LCOH (in $/MWh)", fontsize=14)
    ax.set_xlabel("Annual building heat demand (in MWh)", fontsize=14)
    
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Levelized_cost_of_heating.pdf"), dpi=1000)
    
    
    ###############################################################################
    ####### LEVELIZED COST OF COOLING COMPARISON
    ###############################################################################
    
    bar_all_info = pd.read_excel(os.path.join(path_to_visualization_folder, 'bar_all_info_cooling.xlsx'), sheet_name="Sheet1", index_col=0)
    lcoh = pd.read_excel(os.path.join(path_to_visualization_folder, 'lcoc.xlsx'), sheet_name="Sheet1", index_col=0)
    minmaxscenario = pd.read_excel(os.path.join(path_to_visualization_folder, 'min_max_scenario_cooling.xlsx'), sheet_name="Sheet1", index_col=0)
    sum_heating_demand_scenario = pd.read_excel(os.path.join(path_to_visualization_folder, 'sum_cooling_demand_scenario.xlsx'), sheet_name="Sheet1", index_col=0)["sum_cooling_demand_scenario"]
    
    fig, ax = plt.subplots(figsize=(_factor * 6, _factor * 3))
    lcoh_min = minmaxscenario["min"]
    lcoh_max = minmaxscenario["max"]
    
    dh_max = lcoh[lcoh_max].iloc[0].item()
    dh_min = lcoh[lcoh_min].iloc[0].item()
    
    _color = "#FFE31A"
    ax.plot(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [dh_max, dh_max],
        color=_color,
        linestyle="solid",
    )
    ax.plot(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [dh_min, dh_min],
        color=_color,
        linestyle="solid",
    )
    ax.fill_between(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [dh_min, dh_min],
        [dh_max, dh_max],
        color=_color,
        alpha=0.5,
        zorder=4,
        label="District cooling",
    )
    
    _dict = {0: "Buildings 1-35"}
    
    _dict_linewidth = {0: 0}
    
    for index, row in bar_all_info.iterrows():
        _x_offset = sum(bar_all_info.widths[0:index])
        ax.fill_between(
            [_x_offset, _x_offset + row.widths],
            [row.bases, row.bases],
            [row.bases + row.y_bar, row.bases + row.y_bar],
            color="#3A6D8C",
            edgecolor="#001F3F",
            linewidth=_dict_linewidth.get(index, 0.15),
            zorder=0,
            label=_dict.get(index, None),
        )
    
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.set_ylabel("Min-Max range of LCOC (in $/MWh)", fontsize=14)
    ax.set_xlabel("Annual building cold demand (in MWh)", fontsize=14)
    
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Levelized_cost_of_cooling.pdf"), dpi=1000)
    
    ###############################################################################
    ####### MEAN LEVELIZED COST OF HEATING COMPARISON
    ###############################################################################
    
    mean_all_info = pd.read_excel(os.path.join(path_to_visualization_folder, 'mean_all_info_heating.xlsx'), sheet_name="Sheet1", index_col=0)
    lcoh = pd.read_excel(os.path.join(path_to_visualization_folder, 'lcoh.xlsx'), sheet_name="Sheet1", index_col=0)
    sum_heating_demand_scenario = pd.read_excel(os.path.join(path_to_visualization_folder, 'sum_heating_demand_scenario.xlsx'), sheet_name="Sheet1", index_col=0)["sum_heating_demand_scenario"]
    
    
    fig, ax = plt.subplots(figsize=(_factor * 6, _factor * 3))
    
    lcoh_mean = np.mean(lcoh.values.flatten().tolist())
        
    _color = "#F09319"
    ax.plot(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [lcoh_mean, lcoh_mean],
        color=_color,
        linestyle="solid",
        label="District heating",
    )
    
    x_value = mean_all_info['x_mean']
    y_value = mean_all_info['y_mean']
    
    ax.plot(
        x_value,
        y_value,
        marker='d',            
        color="#3D5300",
        linestyle="solid",
        linewidth=1.0,
        zorder=0,
        label="Buildings 1-35",
    )
    
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    # ax.set_ylim([0, 4.15])
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.set_ylabel("Mean LCOH (in $/MWh)", fontsize=14)
    ax.set_xlabel("Annual building heat demand (in MWh)", fontsize=14)
    
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Mean_levelized_cost_of_heating.pdf"), dpi=1000)
    
    
    ###############################################################################
    ####### MEAN LEVELIZED COST OF COOLING COMPARISON
    ###############################################################################
    
    mean_all_info = pd.read_excel(os.path.join(path_to_visualization_folder, 'mean_all_info_cooling.xlsx'), sheet_name="Sheet1", index_col=0)
    lcoh = pd.read_excel(os.path.join(path_to_visualization_folder, 'lcoc.xlsx'), sheet_name="Sheet1", index_col=0)
    sum_heating_demand_scenario = pd.read_excel(os.path.join(path_to_visualization_folder, 'sum_cooling_demand_scenario.xlsx'), sheet_name="Sheet1", index_col=0)["sum_cooling_demand_scenario"]
    
    fig, ax = plt.subplots(figsize=(_factor * 6, _factor * 3))
    
    lcoh_mean = np.mean(lcoh.values.flatten().tolist())
    
    _color = "#FFE31A"
    ax.plot(
        [0, sum_heating_demand_scenario.iloc[0].item()],
        [lcoh_mean, lcoh_mean],
        color=_color,
        linestyle="solid",
        label="District cooling",
    )
    
    _dict_linewidth = {0: 0}
    
    x_value = mean_all_info['x_mean']
    y_value = mean_all_info['y_mean']
    
    ax.plot(
        x_value,
        y_value,
        marker='d',
        color="#3A6D8C",
        linestyle="solid",
        linewidth=1.0,
        zorder=0,
        label="Buildings 1-35",
    )
    
    
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    _legend = ax.legend(
        loc="upper right",
        facecolor="white",
        fontsize=14,
        handlelength=1,
        handletextpad=0.5,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 1),
        shadow=False,
        framealpha=1,
    )
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    
    ax.set_ylabel("Mean LCOC (in $/MWh)", fontsize=14)
    ax.set_xlabel("Annual building cold demand (in MWh)", fontsize=14)
    
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Mean_levelized_cost_of_cooling.pdf"), dpi=1000)
    
    ###############################################################################
    ####### SCATTER PLOT
    ###############################################################################
    
    _scenarios = [
        "1_reference",
        "2_high_electricity_prices",
        "3_low_electricity_prices",
        "4_flexible_energy_market",
        "5_energy_congestion",
        "6_green_friendly",
        "7_low_gas_demand",
        "8_natural_gas_friendly",
        "9_cold_winters",
        "10_hot_summers",
        "11_warm_summers",
        "12_moderate_climate",
        "13_zero_co2_price",
        "14_delayed_co2_pricing",
        "15_ambitious_co2_pricing",
        "16_expiring_support_res",
    ]
    
    if False:
        _type = []
        _years = []
        _scenarios_save = []
        _values = []
    
        for _sce in _scenarios:
            for year in ["2025", "2030", "2035", "2040", "2045", "2050"]:
                data = sum(
                    pd.read_excel(os.path.join(path_to_result_folder, f'[{_sce}]_#_heat_supply.xlsx'), sheet_name=year)["heating"])
                _type.append("Heating")
                _years.append(int(year))
                _scenarios_save.append(_sce)
                _values.append(data)
                data = sum(
                    pd.read_excel(os.path.join(path_to_result_folder, f'[{_sce}]_#_cool_supply.xlsx'), sheet_name=year)["cooling"])
                _type.append("Cooling")
                _years.append(int(year))
                _scenarios_save.append(_sce)
                _values.append(data)
    
        _d = {
            "Type": _type,
            "Year": _years,
            "Scenarios": _scenarios_save,
            "Values": _values,
        }
        _df = pd.DataFrame(data=_d)
        _df.to_excel(os.path.join(path_to_visualization_folder, 'demands_per_scenario_year'))
    ###############################################################################
    
    if False:
        _type = []
        _years = []
        _scenarios_save = []
        _values = []
    
        for _sce in _scenarios:
            for year in ["2025", "2030", "2035", "2040", "2045", "2050"]:
                _demand_heat = 0
                _demand_cold = 0
                data = pd.read_excel(os.path.join(path_to_result_folder, f'[{_sce}]_#_elec_consumption.xlsx'), sheet_name=year)
                for t in ["eb", "hp", "st", "gt", "dgt", "ieh", "ttes"]:
                    _demand_heat += sum(data[t])
                _demand_heat += 0.4978220286 * sum(data["cp_hp"])
    
                for t in ["ac", "cp_ct", "ites"]:
                    _demand_cold += sum(data[t])
                _demand_cold += 0.5021779714 * sum(data["cp_hp"])
                _type.append("Heating")
                _years.append(int(year))
                _scenarios_save.append(_sce)
                _values.append(_demand_heat)
                _type.append("Cooling")
                _years.append(int(year))
                _scenarios_save.append(_sce)
                _values.append(_demand_cold)
    
        _d = {
            "Type": _type,
            "Year": _years,
            "Scenarios": _scenarios_save,
            "Values": _values,
        }
        _df = pd.DataFrame(data=_d)
        _df.to_excel(os.path.join(path_to_result_folder, 'elec_consumption_per_scenario_year.xlsx'))
    
    ###############################################################################
    # %% FIG X (SCATTERPLOT)
    import matplotlib.pyplot as plt
    import os
    #import matplotlib.patches as mpatches
    import matplotlib.ticker as ticker
    import numpy as np
    #from matplotlib.ticker import FuncFormatter
    import pandas as pd
    #from matplotlib.patches import FancyBboxPatch
    from scipy.spatial import ConvexHull
    
    #_font = 16
    plt.style.use("default")
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    
    supply = pd.read_excel(os.path.join(path_to_visualization_folder, 'demands_per_scenario_year.xlsx'), index_col=0)
    elec_con = pd.read_excel(os.path.join(path_to_visualization_folder, 'elec_consumption_per_scenario_year.xlsx'), index_col=0)
    
    supply_heat = supply.loc[supply.Type == "Heating"]
    supply_cold = supply.loc[supply.Type == "Cooling"]
    
    marker_dict = {
        # 2025 : 'd',
        # 2030 : 's',
        # 2035 : 'x',
        # 2040 : '*',
        # 2045 : '+',
        # 2050 : '<'
    }
    
    _array1 = []
    _array2 = []
    
    # HEATING
    _factor = 1.35
    fig, ax = plt.subplots(figsize=(_factor * 6, _factor * 3))
    for index, row in supply_heat.iterrows():
        _x = row.Values
        _y = elec_con.loc[
            (elec_con["Type"] == "Heating")
            & (elec_con["Year"] == row.Year)
            & (elec_con["Scenarios"] == row.Scenarios),
            "Values",
        ].item()
        if index == supply_heat.index[-1]:
            ax.scatter(
                _x, _y, color="#5A6C57", marker=marker_dict.get(row.Year, "o"), s=16, zorder=3, label='Scenarios'
            )
        else:
            ax.scatter(
                _x, _y, color="#5A6C57", marker=marker_dict.get(row.Year, "o"), s=16, zorder=3
            )
            
        _array1.append(_x)
        _array2.append(_y)
    
    array = np.array(list(zip(_array1, _array2)))
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    hull = ConvexHull(np.array(array))
    
    for simplex in hull.simplices:
        ax.plot(
            array[simplex, 0],
            array[simplex, 1],
            color="#F09319",
            lw=1,
            zorder=-1,
            linestyle="dashed",
        )
    
    ax.fill(
        array[hull.vertices, 0],
        array[hull.vertices, 1],
        color="#F09319",
        alpha=0.25,
        label="Heat flexibility",
    )
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([0, 8000])
    ax.set_ylim([0, 1500])
    
    _legend = ax.legend(
        loc="lower right",
        facecolor="white",
        fontsize=14,
        handlelength=2,
        handletextpad=0.25,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 0),
        shadow=False,
        framealpha=1,
    )
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", " ")))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", " ")))
    
    ax.set_ylabel("Electricity consumption (in MWh)", fontsize=14)
    ax.set_xlabel("Heat supply (in MWh)", fontsize=14)
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Scatter_heating.pdf"), dpi=1000)
    
    # COOLING
    _array1 = []
    _array2 = []
    _factor = 1.35
    fig, ax = plt.subplots(figsize=(_factor * 6, _factor * 3))
    for index, row in supply_cold.iterrows():
        if index == supply_cold.index[-1]:
            _x = row.Values
            _y = elec_con.loc[
                (elec_con["Type"] == "Cooling")
                & (elec_con["Year"] == row.Year)
                & (elec_con["Scenarios"] == row.Scenarios),
                "Values",
            ].item()
            ax.scatter(
                _x, _y, color="#5A6C57", marker=marker_dict.get(row.Year, "o"), s=16, zorder=3, label='Scenarios'
            )
            _array1.append(_x)
            _array2.append(_y)
        else:
            _x = row.Values
            _y = elec_con.loc[
                (elec_con["Type"] == "Cooling")
                & (elec_con["Year"] == row.Year)
                & (elec_con["Scenarios"] == row.Scenarios),
                "Values",
            ].item()
            ax.scatter(
                _x, _y, color="#5A6C57", marker=marker_dict.get(row.Year, "o"), s=16, zorder=3
            )
            _array1.append(_x)
            _array2.append(_y)
    
    array = np.array(list(zip(_array1, _array2)))
    ax.grid(which="major", axis="y", color="#758D99", alpha=0.2, zorder=1)
    
    hull = ConvexHull(np.array(array))
    
    for simplex in hull.simplices:
        ax.plot(
            array[simplex, 0],
            array[simplex, 1],
            color="#80C4E9",
            lw=1,
            zorder=-1,
            linestyle="dashed",
        )
    
    ax.fill(
        array[hull.vertices, 0],
        array[hull.vertices, 1],
        color="#80C4E9",
        alpha=0.25,
        label="Cold flexibility",
    )
    
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 4))
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    
    ax.set_xlim([0, 8000])
    ax.set_ylim([0, 1500])
    
    _legend = ax.legend(
        loc="lower right",
        facecolor="white",
        fontsize=14,
        handlelength=2,
        handletextpad=0.25,
        ncol=1,
        borderpad=0.5,
        columnspacing=1,
        edgecolor="black",
        frameon=True,
        bbox_to_anchor=(1, 0),
        shadow=False,
        framealpha=1,
    )
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", " ")))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", " ")))
    
    ax.set_ylabel("Electricity consumption (in MWh)", fontsize=14)
    ax.set_xlabel("Cold supply (in MWh)", fontsize=14)
    plt.tight_layout()
    
    fig.savefig(os.path.join(path_to_plot_folder, "Scatter_cooling.pdf"), dpi=1000)
