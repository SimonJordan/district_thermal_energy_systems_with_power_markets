import os
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import plotly.subplots as sp

# assumptions
eta_electricity = 3
co2_conversion = 0.2
cp_seer = 5
cp_hp_cop = 6.0525

pio.renderers.default = 'browser'

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, '..', 'inputs')
path_to_result_folder = os.path.join(cur_dir, '..', 'results')
path_to_file_scenarios = os.path.join(path_to_result_folder, 'scenarios.txt')

with open(path_to_file_scenarios, 'r') as file:
    scenarios = [line.strip() for line in file]
    
years = [2025, 2030, 2035, 2040, 2045, 2050]
year_expansion_range = {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1}
hours = list(range(8760))

visualize_scenario = '1_reference'
visualize_year = 2035

cooling_demand = {}
ac_cool_in = {}
ab_ct_cool_in = {}
ab_hp_cool_in = {}
cp_ct_cool_in = {}
cp_hp_cool_in = {}
ites_cool_in = {}
ites_cool_out = {}

ac_inv = {}
ab_ct_inv = {}
ab_hp_inv = {}
cp_ct_inv = {}
cp_hp_inv = {}
ites_inv = {}

ac_c_inv = {}
ab_ct_c_inv = {}
ab_hp_c_inv = {}
cp_ct_c_inv = {}
cp_hp_c_inv = {}
ites_c_inv = {}

ac_c_fix = {}
ab_ct_c_fix = {}
ab_hp_c_fix = {}
cp_ct_c_fix = {}
cp_hp_c_fix = {}
ites_c_fix = {}

ac_c_var = {}
ab_ct_c_var = {}
ab_hp_c_var = {}
cp_ct_c_var = {}
cp_hp_c_var = {}
ites_c_var = {}

ac_elec = {}
ab_ct_elec = {}
ab_hp_elec = {}
cp_ct_elec = {}
cp_hp_elec = {}
ites_elec = {}

ites_soc = {}

electricity_price = {}
electricity_co2_share = {}
gas_price = {}
co2_price = {}

for scenario in scenarios:
    cooling_demand_scenario = {}
    ac_cool_in_scenario = {}
    ab_ct_cool_in_scenario = {}
    ab_hp_cool_in_scenario = {}
    cp_ct_cool_in_scenario = {}
    cp_hp_cool_in_scenario = {}
    ites_cool_in_scenario = {}
    ites_cool_out_scenario = {}
    
    ac_inv_scenario = {}
    ab_ct_inv_scenario = {}
    ab_hp_inv_scenario = {}
    cp_ct_inv_scenario = {}
    cp_hp_inv_scenario = {}
    ites_inv_scenario = {}
    
    ac_c_inv_scenario = {}
    ab_ct_c_inv_scenario = {}
    ab_hp_c_inv_scenario = {}
    cp_ct_c_inv_scenario = {}
    cp_hp_c_inv_scenario = {}
    ites_c_inv_scenario = {}
    
    ac_c_fix_scenario = {}
    ab_ct_c_fix_scenario = {}
    ab_hp_c_fix_scenario = {}
    cp_ct_c_fix_scenario = {}
    cp_hp_c_fix_scenario = {}
    ites_c_fix_scenario = {}
    
    ac_c_var_scenario = {}
    ab_ct_c_var_scenario = {}
    ab_hp_c_var_scenario = {}
    cp_ct_c_var_scenario = {}
    cp_hp_c_var_scenario = {}
    ites_c_var_scenario = {}
    
    ac_elec_scenario = {}
    ab_ct_elec_scenario = {}
    ab_hp_elec_scenario = {}
    cp_ct_elec_scenario = {}
    cp_hp_elec_scenario = {}
    ites_elec_scenario = {}
    
    ites_soc_scenario = {}
    
    electricity_price_scenario = {}
    electricity_co2_share_scenario = {}
    gas_price_scenario = {}
    co2_price_scenario = {}
    
    path_to_cool_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_cool_supply.xlsx')
    path_to_inv_capacity = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_capacity.xlsx')
    path_to_inv_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_cost.xlsx')
    path_to_fix_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_fix_cost.xlsx')
    path_to_var_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_var_cost.xlsx')
    path_to_elec_consumption = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_consumption.xlsx')
    path_to_elec_price_co2_share_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_co2_share_gas_price.xlsx')
    path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
    path_to_storage_soc = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_storage_soc.xlsx')
    
    for year in years:
        df_cool_supply = pd.read_excel(path_to_cool_supply, sheet_name=str(year))
        df_inv_capacity = pd.read_excel(path_to_inv_capacity, sheet_name=str(year))
        df_inv_cost = pd.read_excel(path_to_inv_cost, sheet_name=str(year))
        df_fix_cost = pd.read_excel(path_to_fix_cost, sheet_name=str(year))
        df_var_cost = pd.read_excel(path_to_var_cost, sheet_name=str(year))
        df_elec_consumption = pd.read_excel(path_to_elec_consumption, sheet_name=str(year))
        df_elec_price_co2_share_gas_price = pd.read_excel(path_to_elec_price_co2_share_gas_price, sheet_name=str(year))
        df_co2_price = pd.read_excel(path_to_co2_price, sheet_name=str(year))
        df_storage_soc = pd.read_excel(path_to_storage_soc, sheet_name=str(year))
        
        cooling_demand_scenario[year] = df_cool_supply['cooling'].tolist()
        ac_cool_in_scenario[year] = df_cool_supply['ac'].tolist()
        ab_ct_cool_in_scenario[year] = df_cool_supply['ab_ct'].tolist()
        ab_hp_cool_in_scenario[year] = df_cool_supply['ab_hp'].tolist()
        cp_ct_cool_in_scenario[year] = df_cool_supply['cp_ct'].tolist()
        cp_hp_cool_in_scenario[year] = df_cool_supply['cp_hp'].tolist()
        ites_cool_in_scenario[year] = df_cool_supply['ites+'].tolist()
        ites_cool_out_scenario[year] = df_cool_supply['ites-'].tolist()
        
        ac_inv_scenario[year] = df_inv_capacity['ac'].tolist()[0]
        ab_ct_inv_scenario[year] = df_inv_capacity['ab_ct'].tolist()[0]
        ab_hp_inv_scenario[year] = df_inv_capacity['ab_hp'].tolist()[0]
        cp_ct_inv_scenario[year] = df_inv_capacity['cp_ct'].tolist()[0]
        cp_hp_inv_scenario[year] = df_inv_capacity['cp_hp'].tolist()[0]
        ites_inv_scenario[year] = df_inv_capacity['ites'].tolist()[0]
        
        ac_c_inv_scenario[year] = df_inv_cost['ac'].tolist()[0]
        ab_ct_c_inv_scenario[year] = df_inv_cost['ab_ct'].tolist()[0]
        ab_hp_c_inv_scenario[year] = df_inv_cost['ab_hp'].tolist()[0]
        cp_ct_c_inv_scenario[year] = df_inv_cost['cp_ct'].tolist()[0]
        cp_hp_c_inv_scenario[year] = df_inv_cost['cp_hp'].tolist()[0]
        ites_c_inv_scenario[year] = df_inv_cost['ites'].tolist()[0]
        
        ac_c_fix_scenario[year] = df_fix_cost['ac'].tolist()[0]
        ab_ct_c_fix_scenario[year] = df_fix_cost['ab_ct'].tolist()[0]
        ab_hp_c_fix_scenario[year] = df_fix_cost['ab_hp'].tolist()[0]
        cp_ct_c_fix_scenario[year] = df_fix_cost['cp_ct'].tolist()[0]
        cp_hp_c_fix_scenario[year] = df_fix_cost['cp_hp'].tolist()[0]
        ites_c_fix_scenario[year] = df_fix_cost['ites'].tolist()[0]
        
        ac_c_var_scenario[year] = df_var_cost['ac'].tolist()
        ab_ct_c_var_scenario[year] = df_var_cost['ab_ct'].tolist()
        ab_hp_c_var_scenario[year] = df_var_cost['ab_hp'].tolist()
        cp_ct_c_var_scenario[year] = df_var_cost['cp_ct'].tolist()
        cp_hp_c_var_scenario[year] = df_var_cost['cp_hp'].tolist()
        ites_c_var_scenario[year] = df_var_cost['ites'].tolist()
        
        ac_elec_scenario[year] = df_elec_consumption['ac'].tolist()
        ab_ct_elec_scenario[year] = df_elec_consumption['ab_ct'].tolist()
        ab_hp_elec_scenario[year] = df_elec_consumption['ab_hp'].tolist()
        cp_ct_elec_scenario[year] = df_elec_consumption['cp_ct'].tolist()
        cp_hp_elec_scenario[year] = [value * cp_hp_cop / (cp_seer + cp_hp_cop) for value in df_elec_consumption['cp_hp'].tolist()]
        ites_elec_scenario[year] = df_elec_consumption['ites'].tolist()
        
        ites_soc_scenario[year] = df_storage_soc['ites'].tolist()
        
        electricity_price_scenario[year] = df_elec_price_co2_share_gas_price['elec'].tolist()
        electricity_co2_share_scenario[year] = df_elec_price_co2_share_gas_price['co2'].tolist()
        gas_price_scenario[year] = df_elec_price_co2_share_gas_price['gas'].tolist()
        co2_price_scenario[year] = df_co2_price['co2'].tolist()[0]
        
    cooling_demand[scenario] = cooling_demand_scenario
    ac_cool_in[scenario] = ac_cool_in_scenario
    ab_ct_cool_in[scenario] = ab_ct_cool_in_scenario
    ab_hp_cool_in[scenario] = ab_hp_cool_in_scenario
    cp_ct_cool_in[scenario] = cp_ct_cool_in_scenario
    cp_hp_cool_in[scenario] = cp_hp_cool_in_scenario
    ites_cool_in[scenario] = ites_cool_in_scenario
    ites_cool_out[scenario] = ites_cool_out_scenario
    
    ac_inv[scenario] = ac_inv_scenario
    ab_ct_inv[scenario] = ab_ct_inv_scenario
    ab_hp_inv[scenario] = ab_hp_inv_scenario
    cp_ct_inv[scenario] = cp_ct_inv_scenario
    cp_hp_inv[scenario] = cp_hp_inv_scenario
    ites_inv[scenario] = ites_inv_scenario
    
    ac_c_inv[scenario] = ac_c_inv_scenario
    ab_ct_c_inv[scenario] = ab_ct_c_inv_scenario
    ab_hp_c_inv[scenario] = ab_hp_c_inv_scenario
    cp_ct_c_inv[scenario] = cp_ct_c_inv_scenario
    cp_hp_c_inv[scenario] = cp_hp_c_inv_scenario
    ites_c_inv[scenario] = ites_c_inv_scenario
    
    ac_c_fix[scenario] = ac_c_fix_scenario
    ab_ct_c_fix[scenario] = ab_ct_c_fix_scenario
    ab_hp_c_fix[scenario] = ab_hp_c_fix_scenario
    cp_ct_c_fix[scenario] = cp_ct_c_fix_scenario
    cp_hp_c_fix[scenario] = cp_hp_c_fix_scenario
    ites_c_fix[scenario] = ites_c_fix_scenario
    
    ac_c_var[scenario] = ac_c_var_scenario
    ab_ct_c_var[scenario] = ab_ct_c_var_scenario
    ab_hp_c_var[scenario] = ab_hp_c_var_scenario
    cp_ct_c_var[scenario] = cp_ct_c_var_scenario
    cp_hp_c_var[scenario] = cp_hp_c_var_scenario
    ites_c_var[scenario] = ites_c_var_scenario
    
    ac_elec[scenario] = ac_elec_scenario
    ab_ct_elec[scenario] = ab_ct_elec_scenario
    ab_hp_elec[scenario] = ab_hp_elec_scenario
    cp_ct_elec[scenario] = cp_ct_elec_scenario
    cp_hp_elec[scenario] = cp_hp_elec_scenario
    ites_elec[scenario] = ites_elec_scenario
    
    ites_soc[scenario] = ites_soc_scenario
    
    electricity_price[scenario] = electricity_price_scenario
    electricity_co2_share[scenario] = electricity_co2_share_scenario
    gas_price[scenario] = gas_price_scenario
    co2_price[scenario] = co2_price_scenario

#%% FIG 0 - Demand dispatch

df_0 = pd.DataFrame({'hour': hours, 'electricity': electricity_price[visualize_scenario][visualize_year], 'cooling_demand': cooling_demand[visualize_scenario][visualize_year], 'ac': ac_cool_in[visualize_scenario][visualize_year], 'ab_ct': ab_ct_cool_in[visualize_scenario][visualize_year], 'ab_hp': ab_hp_cool_in[visualize_scenario][visualize_year], 'cp_ct': cp_ct_cool_in[visualize_scenario][visualize_year], 'cp_hp': cp_hp_cool_in[visualize_scenario][visualize_year], 'ites+': ites_cool_in[visualize_scenario][visualize_year], 'ites-': ites_cool_out[visualize_scenario][visualize_year]})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cp_hp'], mode='lines', name='Compression with heat pump', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cp_ct'], mode='lines', name='Compression with cooling tower', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_hp'], mode='lines', name='Absorption with heat pump', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_ct'], mode='lines', name='Absorption with cooling tower', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ac'], mode='lines', name='Airchiller', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ites-'], mode='lines', name='ITES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ites+'], mode='lines', name='ITES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cooling_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cp_hp'], mode='lines', name='Compression with heat pump', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cp_ct'], mode='lines', name='Compression with cooling tower', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_hp'], mode='lines', name='Absorption with heat pump', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_ct'], mode='lines', name='Absorption with cooling tower', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ac'], mode='lines', name='Airchiller', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ites-'], mode='lines', name='ITES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ites+'], mode='lines', name='ITES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cooling_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['electricity'], mode='lines', name='Electricity price', line=dict(color='black', width=2), yaxis='y2'))

fig.update_layout(title=dict(text='Load curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Cool supply in MWh/h', titlefont=dict(size=20), range=[-1, 8 * 1.1], tickvals=np.linspace(-1, 8, 10), tickfont=dict(size=20)), yaxis2=dict(title='Electricity price in $/MWh', titlefont=dict(size=20), range=[-37.5, 300 * 1.1], tickvals=np.linspace(-37.5, 300, 10), tickfont=dict(size=20), overlaying='y', side='right'), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))
fig.update_layout(legend=dict(x=1.05, y=1, xanchor='left'), margin=dict(l=50, r=150, t=50, b=50))

fig.show()

cooling_demand_sorted_1 = sorted(cooling_demand[visualize_scenario][visualize_year], reverse=True)
ac_cool_in_sorted_1 = sorted(ac_cool_in[visualize_scenario][visualize_year], reverse=True)
ab_ct_cool_in_sorted_1 = sorted(ab_ct_cool_in[visualize_scenario][visualize_year], reverse=True)
ab_hp_cool_in_sorted_1 = sorted(ab_hp_cool_in[visualize_scenario][visualize_year], reverse=True)
cp_ct_cool_in_sorted_1 = sorted(cp_ct_cool_in[visualize_scenario][visualize_year], reverse=True)
cp_hp_cool_in_sorted_1 = sorted(cp_hp_cool_in[visualize_scenario][visualize_year], reverse=True)
ites_cool_in_sorted_1 = sorted(ites_cool_in[visualize_scenario][visualize_year], reverse=True)
ites_cool_out_sorted_1 = sorted(ites_cool_out[visualize_scenario][visualize_year])

df_1 = pd.DataFrame({'hour': hours, 'cooling_demand': cooling_demand_sorted_1, 'ac': ac_cool_in_sorted_1, 'ab_ct': ab_ct_cool_in_sorted_1, 'ab_hp': ab_hp_cool_in_sorted_1, 'cp_ct': cp_ct_cool_in_sorted_1, 'cp_hp': cp_hp_cool_in_sorted_1, 'ites+': ites_cool_in_sorted_1, 'ites-': ites_cool_out_sorted_1})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['cp_hp'], mode='lines', name='Compression with heat pump', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['cp_ct'], mode='lines', name='Compression with cooling tower', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ab_hp'], mode='lines', name='Absorption with heat pump', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ab_ct'], mode='lines', name='Absorption with cooling', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ac'], mode='lines', name='Airchiller', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ites-'], mode='lines', name='ITES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ites+'], mode='lines', name='ITES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['cooling_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

index_sorted = sorted(range(len(cooling_demand[visualize_scenario][visualize_year])), key=lambda i: cooling_demand[visualize_scenario][visualize_year][i], reverse=True)
cooling_demand_sorted_2 = [cooling_demand[visualize_scenario][visualize_year][i] for i in index_sorted]
ac_cool_in_sorted_2 = [ac_cool_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ab_ct_cool_in_sorted_2 = [ab_ct_cool_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ab_hp_cool_in_sorted_2 = [ab_hp_cool_in[visualize_scenario][visualize_year][i] for i in index_sorted]
cp_ct_cool_in_sorted_2 = [cp_ct_cool_in[visualize_scenario][visualize_year][i] for i in index_sorted]
cp_hp_cool_in_sorted_2 = [cp_hp_cool_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ites_cool_in_sorted_2 = [ites_cool_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ites_cool_out_sorted_2 = [ites_cool_out[visualize_scenario][visualize_year][i] for i in index_sorted]

df_2 = pd.DataFrame({'hour': hours, 'cooling_demand': cooling_demand_sorted_2, 'ac': ac_cool_in_sorted_2, 'ab_ct': ab_ct_cool_in_sorted_2, 'ab_hp': ab_hp_cool_in_sorted_2, 'cp_ct': cp_ct_cool_in_sorted_2, 'cp_hp': cp_hp_cool_in_sorted_2, 'ites+': ites_cool_in_sorted_2, 'ites-': ites_cool_out_sorted_2})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['cp_hp'], mode='lines', name='Compression with heat pump', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['cp_ct'], mode='lines', name='Compression with cooling tower', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ab_hp'], mode='lines', name='Absorption with heat pump', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ab_ct'], mode='lines', name='Absorption with cooling', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ac'], mode='lines', name='Airchiller', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ites-'], mode='lines', name='ITES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ites+'], mode='lines', name='ITES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['cooling_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

#%% FIG 1 - Technology dispatch

df_3 = pd.DataFrame({'hour': dict(zip(scenarios, [hours]*len(scenarios))), 'ac': ac_cool_in, 'ab_ct': ab_ct_cool_in, 'ab_hp': ab_hp_cool_in, 'cp_ct': cp_ct_cool_in, 'cp_hp': cp_hp_cool_in, 'ites+': ites_cool_in, 'ites-': ites_cool_out})

technologies_abb = ['ac', 'ab_ct', 'ab_hp', 'cp_ct', 'cp_hp', 'ites+', 'ites-']
technologies_name = {'ac': 'Airchiller', 'ab_ct': 'Absorption with cooling tower', 'ab_hp': 'Absorption with heat pump', 'cp_ct': 'Compression with cooling tower', 'cp_hp': 'Compression with heat pump', 'ites+': 'ITES feed in', 'ites-': 'ITES store'}

for technology in technologies_abb: 
    fig = go.Figure()
    
    for scenario in scenarios:
        fig.add_trace(go.Scatter(x=df_3['hour'][scenario], y=df_3[technology][scenario][visualize_year], mode='lines', name=scenario))

    fig.update_layout(title=dict(text=technologies_name[technology], font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

    fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Winter week', 'Summer week'))

fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['ac'][scenarios[0]][visualize_year][:168], mode='lines', name='Scenario 1: reference', line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['ac'][scenarios[12]][visualize_year][:168], mode='lines', name='Scenario 13: zero co2 price', line=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)) + list(range(168))[::-1], y=df_3['ac'][scenarios[0]][visualize_year][:168] + df_3['ac'][scenarios[12]][visualize_year][:168][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)

#fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['ac'][scenarios[12]][visualize_year], mode='lines', name='Scenario 1: high electricity price', fill='tonexty', fillcolor='#00CC96'))

fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_3['ac'][scenarios[0]][visualize_year][4380:4548], mode='lines', name='Scenario 1: reference', line=dict(color='#636EFA'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_3['ac'][scenarios[12]][visualize_year][4380:4548], mode='lines', name='Scenario 13: zero co2 price', line=dict(color='#00CC96'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)) + list(range(4380, 4548))[::-1], y=df_3['ac'][scenarios[0]][visualize_year][4380:4548] + df_3['ac'][scenarios[12]][visualize_year][4380:4548][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=2)

fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=1)
fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=2)

fig.update_yaxes(title_text='Cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Airchiller', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

#%% FIG 2 - SOC

df_4 = pd.DataFrame({'hour': hours, 'ites_absolute': ites_soc[visualize_scenario][visualize_year],})
df_4['ites_relative'] = (df_4['ites_absolute'] / df_4['ites_absolute'].max()) * 100

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_4['hour'], y=df_4['ites_absolute'], mode='lines', name='ITES SOC', line=dict(color='#FFA15A', width=2)))
fig.add_trace(go.Scatter(x=df_4['hour'], y=df_4['ites_relative'], mode='lines', name='ITES SOC', line=dict(color='#FFA15A', width=2), yaxis='y2', showlegend=False))

fig.update_layout(title=dict(text='State of charge', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='State of charge in MWh', titlefont=dict(size=20), tickfont=dict(size=20), range=[0, df_4['ites_absolute'].max() * 1.1], tickvals=np.linspace(0, df_4['ites_absolute'].max(), 6), tickformat='.2f'), yaxis2=dict(title='State of charge in %', titlefont=dict(size=20), tickfont=dict(size=20), overlaying='y', side='right', range=[0, 100 * 1.1]), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

#%% FIG 3 - Investments

ratio_ac_inv = []
ratio_inv = []
index = 0

for year in years[:5]:
    index +=1
    
    cooling_ac_inv_sum = sum(list(ac_inv[visualize_scenario].values())[:index])
    cooling_technology_inv_sum = sum(list(ac_inv[visualize_scenario].values())[:index])
    storage_technology_inv_sum = sum(list(ites_inv[visualize_scenario].values())[:index])
    
    ratio_ac_inv.append(cooling_ac_inv_sum / storage_technology_inv_sum * 100)
    ratio_inv.append(cooling_technology_inv_sum / storage_technology_inv_sum * 100)
    
    technologies = ['Airchiller', 'Absorption with cooling tower', 'Absorption with heat pump', 'Compression with cooling tower', 'Compression with heat pump']
    technologies_map = {'Airchiller': ac_inv, 'Absorption with cooling tower': ab_ct_inv, 'Absorption with heat pump': ab_hp_inv, 'Compression with cooling tower': cp_ct_inv, 'Compression with heat pump': cp_hp_inv}
    storages = ['Ice thermal energy storage']
    storages_map = {'Ice thermal energy storage': ites_inv}

fig = go.Figure()

fig = sp.make_subplots(rows=2, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}], [{'colspan': 1}, None]], subplot_titles=('Cooling technology investments', 'Storage technology investments', 'Ratio cooling to storage capacity'))

fig.add_trace(go.Scatter(x=years[:5], y=ratio_inv[:5], name='Ratio'), row=2, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(storages_map['Ice thermal energy storage'][visualize_scenario].values())[:5], name='Ice thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Airchiller'][visualize_scenario].values())[:5], name='Airchiller', marker=dict(color='#19D3F3')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with cooling tower'][visualize_scenario].values())[:5], name='Compression with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with heat pump'][visualize_scenario].values())[:5], name='Compression with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with cooling tower'][visualize_scenario].values())[:5], name='Absorption with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with heat pump'][visualize_scenario].values())[:5], name='Absorption with heat pump', marker=dict(color='grey')), row=1, col=1)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=2)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=2, col=1)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=1)

fig.update_yaxes(range=[0, 40], row=2, col=1)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(x=0.7, y=0, traceorder='normal', font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack', width=1200, height=900)

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=2, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}], [{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Cooling technology investments', 'Storage technology investments', 'Ratio cooling to storage capacity', 'Ratio cooling to storage capacity'))

fig.add_trace(go.Scatter(x=years[:5], y=ratio_inv[:5], name='Ratio total', line=dict(color='#EF553B')), row=2, col=2)

fig.add_trace(go.Scatter(x=years[:5], y=ratio_ac_inv[:5], name='Ratio airchiller', line=dict(color='#19D3F3')), row=2, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with heat pump'][visualize_scenario].values())[:5], name='Absorption with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with cooling tower'][visualize_scenario].values())[:5], name='Absorption with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with heat pump'][visualize_scenario].values())[:5], name='Compression with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with cooling tower'][visualize_scenario].values())[:5], name='Compression with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Airchiller'][visualize_scenario].values())[:5], name='Airchiller', marker=dict(color='#19D3F3')), row=1, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(storages_map['Ice thermal energy storage'][visualize_scenario].values())[:5], name='Ice thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=2)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=2, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=2, col=2)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=1)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=2)

fig.update_yaxes(range=[0, 40], row=2, col=1)
fig.update_yaxes(range=[0, 40], row=2, col=2)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack')

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Cooling technology investments', 'Storage technology investments'))

fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with heat pump'][visualize_scenario].values())[:5], name='Absorption with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with cooling tower'][visualize_scenario].values())[:5], name='Absorption with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with heat pump'][visualize_scenario].values())[:5], name='Compression with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with cooling tower'][visualize_scenario].values())[:5], name='Compression with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Airchiller'][visualize_scenario].values())[:5], name='Airchiller', marker=dict(color='#19D3F3')), row=1, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(storages_map['Ice thermal energy storage'][visualize_scenario].values())[:5], name='Ice thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=2)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack')

fig.show()

fig = go.Figure()

fig.add_trace(go.Scatter(x=years[:5], y=ratio_ac_inv[:5], name='Ratio airchiller', line=dict(width=4, color='#19D3F3')))

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5])

fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20))

fig.update_yaxes(range=[0, 40])

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)))

fig.show()

#%% FIG 4 - LCOC

#NOTIZ: building 35 kein cooling demand

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
             34: {2025: 0, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1}}

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

demand_cool_sum_variation = {}

for building in range(1, 35):
    variation = 0
    
    for scenario in scenarios:
            
        for year in years:
            variation += buildings[building][year] * demand_cool_variation[scenario][year]
    
    demand_cool_sum_variation[building] = variation / len(scenarios)

buildings_demand = {}
buildings_demand_sum = {}
buildings_lcoc = {}

path_to_file_cooling_demand_building = os.path.join(path_to_input_folder, 'districts_cooling_demand_phase2.xlsx')
df_cooling_demand_building = pd.read_excel(path_to_file_cooling_demand_building)

for building in range(1, 35):
    cooling_demand_building = df_cooling_demand_building[f'cooling_demand_building_{building}'].tolist()
    buildings_demand[building] = cooling_demand_building
    buildings_demand_sum[building] = sum(cooling_demand_building)

for building in range(1, 35):
    buildings_lcoc_scenario = []
    for scenario in scenarios:
        building_c_sum = 0
        
        for year in years:
            for hour in hours:
                building_c_sum += buildings[building][year] * demand_cool_variation[scenario][year] * buildings_demand[building][hour] / eta_electricity * (electricity_price[scenario][year][hour] + electricity_co2_share[scenario][year][hour] * co2_price[scenario][year])
            
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
building_lcoc_min_index = [i + 1 for i in sorted(range(len(building_lcoc_min)), key=lambda i: building_lcoc_min[i], reverse=True)]
building_lcoc_avg_index = [i + 1 for i in sorted(range(len(building_lcoc_avg)), key=lambda i: building_lcoc_avg[i], reverse=True)]

x_bar = []
y_bar = []
widths = []
bases = []
labels = []

for building in range(1, 35):
    if building == 1:
        x_bar.append(buildings_demand_sum[building] / 2)
        
    else:
        x_bar.append(x_bar[building-2] + buildings_demand_sum[building-1] / 2 + buildings_demand_sum[building] / 2)
    
    y_bar.append(max(buildings_lcoc[building]) - min(buildings_lcoc[building]))
    widths.append(buildings_demand_sum[building])
    bases.append(min(buildings_lcoc[building]))
    labels.append(f'Building_{building}')

lcoc = {}

for scenario in scenarios:
    sum_cooling_cost = 0
    sum_cooling_demand = 0
    for year in years:
        sum_cooling_demand_scenario = 0
        
        sum_cooling_demand_scenario = sum(cooling_demand[scenario][year])
        sum_cooling_demand += sum_cooling_demand_scenario * year_expansion_range[year]
        sum_cooling_cost += sum(ac_c_var[scenario][year]) + sum(ab_ct_c_var[scenario][year]) + sum(ab_hp_c_var[scenario][year]) + sum(cp_ct_c_var[scenario][year]) + sum(cp_hp_c_var[scenario][year]) * cp_hp_cop / (cp_seer + cp_hp_cop) + sum(ites_c_var[scenario][year]) + \
                            ac_c_inv[scenario][year] + ab_ct_c_inv[scenario][year] + ab_hp_c_inv[scenario][year] + cp_ct_c_inv[scenario][year] + cp_hp_c_inv[scenario][year] * 1 / (1 + 1 + 1 / cp_seer) + ites_c_inv[scenario][year] + \
                            ac_c_fix[scenario][year] + ab_ct_c_fix[scenario][year] + ab_hp_c_fix[scenario][year] + cp_ct_c_fix[scenario][year] + cp_hp_c_fix[scenario][year] * 1 / (1 + 1 + 1 / cp_seer) + ites_c_fix[scenario][year]
                            
    lcoc[scenario] = sum_cooling_cost / sum_cooling_demand

fig = go.Figure()

lcoc_min = min(lcoc, key=lcoc.get)
lcoc_max = max(lcoc, key=lcoc.get)

# for scenario in scenarios:
#     fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario], y=[lcoc[scenario], lcoc[scenario]], mode='lines', name=scenario))

fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario], y=[lcoc[lcoc_min], lcoc[lcoc_min]], mode='lines', line=dict(color='black'), name=lcoc_min, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario], y=[lcoc[lcoc_max], lcoc[lcoc_max]], mode='lines', line=dict(color='black'), name=lcoc_max, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario, sum_cooling_demand_scenario, 0], y=[lcoc[lcoc_min], lcoc[lcoc_min], lcoc[lcoc_max], lcoc[lcoc_max]],  fill='toself', fillcolor='gray', opacity=0.5, line=dict(color='gray'), showlegend=False))
# , fillpattern=dict(shape="x",  fgcolor="black")

for i in range(len(x_bar)):
    fig.add_trace(go.Bar(x=[x_bar[i]], y=[y_bar[i]], width=widths[i], base=bases[i], text=labels[i], textposition='outside', textangle=0, name=labels[i]))

fig.update_xaxes(range=[0, sum_cooling_demand_scenario])

fig.update_layout(title=dict(text='Levelized costs of cooling', font=dict(size=30)), xaxis=dict(title='Annual building cool demand in MWh', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Lcoc in $/MWh', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Buildings', font=dict(size=20)), legend=dict(font=dict(size=20)), barmode='overlay', bargap=0)

fig.show()

x_bar = []
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

fig = go.Figure()

lcoc_min = min(lcoc, key=lcoc.get)
lcoc_max = max(lcoc, key=lcoc.get)

# for scenario in scenarios:
#     fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario], y=[lcoc[scenario], lcoc[scenario]], mode='lines', name=scenario))

fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario], y=[lcoc[lcoc_min], lcoc[lcoc_min]], mode='lines', line=dict(color='rgb(253, 180, 98)'), name=lcoc_min, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario], y=[lcoc[lcoc_max], lcoc[lcoc_max]], mode='lines', line=dict(color='rgb(253, 180, 98)'), name=lcoc_max, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_cooling_demand_scenario, sum_cooling_demand_scenario, 0], y=[lcoc[lcoc_min], lcoc[lcoc_min], lcoc[lcoc_max], lcoc[lcoc_max]], name='DC-system', fill='toself', fillcolor='rgb(253, 180, 98)', opacity=0.5, line=dict(color='rgb(253, 180, 98)')))
# , fillpattern=dict(shape="x",  fgcolor="black")

for i in range(len(x_bar)-1):
    fig.add_trace(go.Bar(x=[x_bar[i]], y=[y_bar[i]], width=widths[i], base=bases[i], marker=dict(color='rgb(128, 177, 211)'), showlegend=False))

fig.add_trace(go.Bar(x=[x_bar[i+1]], y=[y_bar[i+1]], width=widths[i+1], base=bases[i+1], marker=dict(color='rgb(128, 177, 211)'), name='Buildings'))

fig.update_xaxes(range=[0, sum_cooling_demand_scenario])
fig.update_yaxes(range=[0, bases[0]+y_bar[0]+20])

fig.update_layout(title=dict(text='Levelized costs of cooling', font=dict(size=30)), uniformtext_minsize=10, uniformtext_mode='show', xaxis=dict(title='Annual building cool demand in MWh', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Lcoc in $/MWh', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='lcoc', font=dict(size=20)), legend=dict(font=dict(size=20)), barmode='overlay', bargap=0)

fig.show()

#%% FIG 5 - Load duration curve

load_duration_curve_demand = cooling_demand[visualize_scenario][visualize_year]

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
    load_duration_curve_scenario = [elec_0 + elec_1 + elec_2 + elec_3 + elec_4 + elec_5 for elec_0, elec_1, elec_2, elec_3, elec_4, elec_5 in zip(ac_elec[scenario][visualize_year], ab_ct_elec[scenario][visualize_year], ab_hp_elec[scenario][visualize_year], cp_ct_elec[scenario][visualize_year], cp_hp_elec[scenario][visualize_year], ites_elec[scenario][visualize_year])]
    load_duration_curve[scenario] =  sorted(load_duration_curve_scenario, reverse=True)

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=load_duration_curve_demand, mode='lines', fill='tozeroy', name='Buildings'))
fig.add_trace(go.Scatter(x=df_0['hour'], y=load_duration_curve[visualize_scenario], mode='lines', fill='tozeroy', name=visualize_scenario))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Electric energy per hour in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Profiles', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()
