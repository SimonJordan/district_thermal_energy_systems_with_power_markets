import os
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import plotly.subplots as sp

# assumptions
eta_gas = 0.9
co2_conversion = 0.2
eta_electricity = 0.99
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

heating_demand = {}
eb_heat_in = {}
hp_heat_in = {}
st_heat_in = {}
wi_heat_in = {}
gt_heat_in = {}
dgt_heat_in = {}
ieh_heat_in = {}
chp_heat_in = {}
ab_ct_heat_out = {}
ab_hp_heat_in = {}
ab_hp_heat_out = {}
cp_hp_heat_in = {}
ttes_heat_in = {}
ttes_heat_out = {}

eb_inv = {}
hp_inv = {}
st_inv = {}
wi_inv = {}
gt_inv = {}
dgt_inv = {}
ieh_inv = {}
chp_inv = {}
ab_ct_inv = {}
ab_hp_inv = {}
cp_hp_inv = {}
ttes_inv = {}

eb_c_inv = {}
hp_c_inv = {}
st_c_inv = {}
wi_c_inv = {}
gt_c_inv = {}
dgt_c_inv = {}
ieh_c_inv = {}
chp_c_inv = {}
ab_ct_c_inv = {}
ab_hp_c_inv = {}
cp_hp_c_inv = {}
ttes_c_inv = {}

eb_c_fix = {}
hp_c_fix = {}
st_c_fix = {}
wi_c_fix = {}
gt_c_fix = {}
dgt_c_fix = {}
ieh_c_fix = {}
chp_c_fix = {}
ab_ct_c_fix = {}
ab_hp_c_fix = {}
cp_hp_c_fix = {}
ttes_c_fix = {}

eb_c_var = {}
hp_c_var = {}
st_c_var = {}
wi_c_var = {}
gt_c_var = {}
dgt_c_var = {}
ieh_c_var = {}
chp_c_var = {}
ab_ct_c_var = {}
ab_hp_c_var = {}
cp_hp_c_var = {}
ttes_c_var = {}

eb_elec = {}
hp_elec = {}
st_elec = {}
gt_elec = {}
dgt_elec = {}
ieh_elec = {}
ab_ct_elec = {}
ab_hp_elec = {}
cp_hp_elec = {}
ttes_elec = {}

ttes_soc = {}

electricity_price = {}
electricity_co2_share = {}
gas_price = {}
co2_price = {}

for scenario in scenarios:
    heating_demand_scenario = {}
    eb_heat_in_scenario = {}
    hp_heat_in_scenario = {}
    st_heat_in_scenario = {}
    wi_heat_in_scenario = {}
    gt_heat_in_scenario = {}
    dgt_heat_in_scenario = {}
    ieh_heat_in_scenario = {}
    chp_heat_in_scenario = {}
    ab_ct_heat_out_scenario = {}
    ab_hp_heat_in_scenario = {}
    ab_hp_heat_out_scenario = {}
    cp_hp_heat_in_scenario = {}
    ttes_heat_in_scenario = {}
    ttes_heat_out_scenario = {}
    
    eb_inv_scenario = {}
    hp_inv_scenario = {}
    st_inv_scenario = {}
    wi_inv_scenario = {}
    gt_inv_scenario = {}
    dgt_inv_scenario = {}
    ieh_inv_scenario = {}
    chp_inv_scenario = {}
    ab_ct_inv_scenario = {}
    ab_hp_inv_scenario = {}
    cp_hp_inv_scenario = {}
    ttes_inv_scenario = {}
    
    eb_c_inv_scenario = {}
    hp_c_inv_scenario = {}
    st_c_inv_scenario = {}
    wi_c_inv_scenario = {}
    gt_c_inv_scenario = {}
    dgt_c_inv_scenario = {}
    ieh_c_inv_scenario = {}
    chp_c_inv_scenario = {}
    ab_ct_c_inv_scenario = {}
    ab_hp_c_inv_scenario = {}
    cp_hp_c_inv_scenario = {}
    ttes_c_inv_scenario = {}
    
    eb_c_fix_scenario = {}
    hp_c_fix_scenario = {}
    st_c_fix_scenario = {}
    wi_c_fix_scenario = {}
    gt_c_fix_scenario = {}
    dgt_c_fix_scenario = {}
    ieh_c_fix_scenario = {}
    chp_c_fix_scenario = {}
    ab_ct_c_fix_scenario = {}
    ab_hp_c_fix_scenario = {}
    cp_hp_c_fix_scenario = {}
    ttes_c_fix_scenario = {}
    
    eb_c_var_scenario = {}
    hp_c_var_scenario = {}
    st_c_var_scenario = {}
    wi_c_var_scenario = {}
    gt_c_var_scenario = {}
    dgt_c_var_scenario = {}
    ieh_c_var_scenario = {}
    chp_c_var_scenario = {}
    ab_ct_c_var_scenario = {}
    ab_hp_c_var_scenario = {}
    cp_hp_c_var_scenario = {}
    ttes_c_var_scenario = {}
    
    eb_elec_scenario = {}
    hp_elec_scenario = {}
    st_elec_scenario = {}
    gt_elec_scenario = {}
    dgt_elec_scenario = {}
    ieh_elec_scenario = {}
    ab_ct_elec_scenario = {}
    ab_hp_elec_scenario = {}
    cp_hp_elec_scenario = {}
    ttes_elec_scenario = {}
    
    ttes_soc_scenario = {}
    
    electricity_price_scenario = {}
    electricity_co2_share_scenario = {}
    gas_price_scenario = {}
    co2_price_scenario = {}
    
    path_to_heat_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_heat_supply.xlsx')
    path_to_inv_capacity = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_capacity.xlsx')
    path_to_inv_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_cost.xlsx')
    path_to_fix_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_fix_cost.xlsx')
    path_to_var_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_var_cost.xlsx')
    path_to_elec_consumption = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_consumption.xlsx')
    path_to_elec_price_co2_share_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_co2_share_gas_price.xlsx')
    path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
    path_to_storage_soc = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_storage_soc.xlsx')
    
    for year in years:
        df_heat_supply = pd.read_excel(path_to_heat_supply, sheet_name=str(year))
        df_inv_capacity = pd.read_excel(path_to_inv_capacity, sheet_name=str(year))
        df_inv_cost = pd.read_excel(path_to_inv_cost, sheet_name=str(year))
        df_fix_cost = pd.read_excel(path_to_fix_cost, sheet_name=str(year))
        df_var_cost = pd.read_excel(path_to_var_cost, sheet_name=str(year))
        df_elec_consumption = pd.read_excel(path_to_elec_consumption, sheet_name=str(year))
        df_elec_price_co2_share_gas_price = pd.read_excel(path_to_elec_price_co2_share_gas_price, sheet_name=str(year))
        df_co2_price = pd.read_excel(path_to_co2_price, sheet_name=str(year))
        df_storage_soc = pd.read_excel(path_to_storage_soc, sheet_name=str(year))
        
        heating_demand_scenario[year] = df_heat_supply['heating'].tolist()
        eb_heat_in_scenario[year] = df_heat_supply['eb'].tolist()
        hp_heat_in_scenario[year] = df_heat_supply['hp'].tolist()
        st_heat_in_scenario[year] = df_heat_supply['st'].tolist()
        wi_heat_in_scenario[year] = df_heat_supply['wi'].tolist()
        gt_heat_in_scenario[year] = df_heat_supply['gt'].tolist()
        dgt_heat_in_scenario[year] = df_heat_supply['dgt'].tolist()
        ieh_heat_in_scenario[year] = df_heat_supply['ieh'].tolist()
        chp_heat_in_scenario[year] = df_heat_supply['chp'].tolist()
        ab_ct_heat_out_scenario[year] = df_heat_supply['ab_ct-'].tolist()
        ab_hp_heat_in_scenario[year] = df_heat_supply['ab_hp+'].tolist()
        ab_hp_heat_out_scenario[year] = df_heat_supply['ab_hp-'].tolist()
        cp_hp_heat_in_scenario[year] = df_heat_supply['cp_hp+'].tolist()
        ttes_heat_in_scenario[year] = df_heat_supply['ttes+'].tolist()
        ttes_heat_out_scenario[year] = df_heat_supply['ttes-'].tolist()
        
        eb_inv_scenario[year] = df_inv_capacity['eb'].tolist()[0]
        hp_inv_scenario[year] = df_inv_capacity['hp'].tolist()[0]
        st_inv_scenario[year] = df_inv_capacity['st'].tolist()[0]
        wi_inv_scenario[year] = df_inv_capacity['wi'].tolist()[0]
        gt_inv_scenario[year] = df_inv_capacity['gt'].tolist()[0]
        dgt_inv_scenario[year] = df_inv_capacity['dgt'].tolist()[0]
        ieh_inv_scenario[year] = df_inv_capacity['ieh'].tolist()[0]
        chp_inv_scenario[year] = df_inv_capacity['chp'].tolist()[0]
        ab_ct_inv_scenario[year] = df_inv_capacity['ab_ct'].tolist()[0]
        ab_hp_inv_scenario[year] = df_inv_capacity['ab_hp'].tolist()[0]
        cp_hp_inv_scenario[year] = df_inv_capacity['cp_hp'].tolist()[0] * (1 + 1 / cp_seer)
        ttes_inv_scenario[year] = df_inv_capacity['ttes'].tolist()[0]
        
        eb_c_inv_scenario[year] = df_inv_cost['eb'].tolist()[0]
        hp_c_inv_scenario[year] = df_inv_cost['hp'].tolist()[0]
        st_c_inv_scenario[year] = df_inv_cost['st'].tolist()[0]
        wi_c_inv_scenario[year] = df_inv_cost['wi'].tolist()[0]
        gt_c_inv_scenario[year] = df_inv_cost['gt'].tolist()[0]
        dgt_c_inv_scenario[year] = df_inv_cost['dgt'].tolist()[0]
        ieh_c_inv_scenario[year] = df_inv_cost['ieh'].tolist()[0]
        chp_c_inv_scenario[year] = df_inv_cost['chp'].tolist()[0]
        ab_ct_c_inv_scenario[year] = df_inv_cost['ab_ct'].tolist()[0]
        ab_hp_c_inv_scenario[year] = df_inv_cost['ab_hp'].tolist()[0]
        cp_hp_c_inv_scenario[year] = df_inv_cost['cp_hp'].tolist()[0]
        ttes_c_inv_scenario[year] = df_inv_cost['ttes'].tolist()[0]
        
        eb_c_fix_scenario[year] = df_fix_cost['eb'].tolist()[0]
        hp_c_fix_scenario[year] = df_fix_cost['hp'].tolist()[0]
        st_c_fix_scenario[year] = df_fix_cost['st'].tolist()[0]
        wi_c_fix_scenario[year] = df_fix_cost['wi'].tolist()[0]
        gt_c_fix_scenario[year] = df_fix_cost['gt'].tolist()[0]
        dgt_c_fix_scenario[year] = df_fix_cost['dgt'].tolist()[0]
        ieh_c_fix_scenario[year] = df_fix_cost['ieh'].tolist()[0]
        chp_c_fix_scenario[year] = df_fix_cost['chp'].tolist()[0]
        ab_ct_c_fix_scenario[year] = df_fix_cost['ab_ct'].tolist()[0]
        ab_hp_c_fix_scenario[year] = df_fix_cost['ab_hp'].tolist()[0]
        cp_hp_c_fix_scenario[year] = df_fix_cost['cp_ct'].tolist()[0]
        ttes_c_fix_scenario[year] = df_fix_cost['ttes'].tolist()[0]
        
        eb_c_var_scenario[year] = df_var_cost['eb'].tolist()
        hp_c_var_scenario[year] = df_var_cost['hp'].tolist()
        st_c_var_scenario[year] = df_var_cost['st'].tolist()
        wi_c_var_scenario[year] = df_var_cost['wi'].tolist()
        gt_c_var_scenario[year] = df_var_cost['gt'].tolist()
        dgt_c_var_scenario[year] = df_var_cost['dgt'].tolist()
        ieh_c_var_scenario[year] = df_var_cost['ieh'].tolist()
        chp_c_var_scenario[year] = df_var_cost['chp'].tolist()
        ab_ct_c_var_scenario[year] = df_var_cost['ab_ct'].tolist()
        ab_hp_c_var_scenario[year] = df_var_cost['ab_hp'].tolist()
        cp_hp_c_var_scenario[year] = df_var_cost['cp_hp'].tolist()
        ttes_c_var_scenario[year] = df_var_cost['ttes'].tolist()
        
        eb_elec_scenario[year] = df_elec_consumption['eb'].tolist()
        hp_elec_scenario[year] = df_elec_consumption['hp'].tolist()
        st_elec_scenario[year] = df_elec_consumption['st'].tolist()
        gt_elec_scenario[year] = df_elec_consumption['gt'].tolist()
        dgt_elec_scenario[year] = df_elec_consumption['dgt'].tolist()
        ieh_elec_scenario[year] = df_elec_consumption['ieh'].tolist()
        ab_ct_elec_scenario[year] = df_elec_consumption['ab_ct'].tolist()
        ab_hp_elec_scenario[year] = df_elec_consumption['ab_hp'].tolist()
        cp_hp_elec_scenario[year] = [value * cp_seer / (cp_seer + cp_hp_cop) for value in df_elec_consumption['cp_hp'].tolist()]
        ttes_elec_scenario[year] = df_elec_consumption['ttes'].tolist()
        
        ttes_soc_scenario[year] = df_storage_soc['ttes'].tolist()
        
        electricity_price_scenario[year] = df_elec_price_co2_share_gas_price['elec'].tolist()
        electricity_co2_share_scenario[year] = df_elec_price_co2_share_gas_price['co2'].tolist()
        gas_price_scenario[year] = df_elec_price_co2_share_gas_price['gas'].tolist()
        co2_price_scenario[year] = df_co2_price['co2'].tolist()[0]
        
    heating_demand[scenario] = heating_demand_scenario
    eb_heat_in[scenario] = eb_heat_in_scenario
    hp_heat_in[scenario] = hp_heat_in_scenario
    st_heat_in[scenario] = st_heat_in_scenario
    wi_heat_in[scenario] = wi_heat_in_scenario
    gt_heat_in[scenario] = gt_heat_in_scenario
    dgt_heat_in[scenario] = dgt_heat_in_scenario
    ieh_heat_in[scenario] = ieh_heat_in_scenario
    chp_heat_in[scenario] = chp_heat_in_scenario
    ab_ct_heat_out[scenario] = ab_ct_heat_out_scenario
    ab_hp_heat_in[scenario] = ab_hp_heat_in_scenario
    ab_hp_heat_out[scenario] = ab_hp_heat_out_scenario
    cp_hp_heat_in[scenario] = cp_hp_heat_in_scenario
    ttes_heat_in[scenario] = ttes_heat_in_scenario
    ttes_heat_out[scenario] = ttes_heat_out_scenario
    
    eb_inv[scenario] = eb_inv_scenario
    hp_inv[scenario] = hp_inv_scenario
    st_inv[scenario] = st_inv_scenario
    wi_inv[scenario] = wi_inv_scenario
    gt_inv[scenario] = gt_inv_scenario
    dgt_inv[scenario] = dgt_inv_scenario
    ieh_inv[scenario] = ieh_inv_scenario
    chp_inv[scenario] = chp_inv_scenario
    ab_ct_inv[scenario] = ab_ct_inv_scenario
    ab_hp_inv[scenario] = ab_hp_inv_scenario
    cp_hp_inv[scenario] = cp_hp_inv_scenario
    ttes_inv[scenario] = ttes_inv_scenario
    
    eb_c_inv[scenario] = eb_c_inv_scenario
    hp_c_inv[scenario] = hp_c_inv_scenario
    st_c_inv[scenario] = st_c_inv_scenario
    wi_c_inv[scenario] = wi_c_inv_scenario
    gt_c_inv[scenario] = gt_c_inv_scenario
    dgt_c_inv[scenario] = dgt_c_inv_scenario
    ieh_c_inv[scenario] = ieh_c_inv_scenario
    chp_c_inv[scenario] = chp_c_inv_scenario
    ab_ct_c_inv[scenario] = ab_ct_c_inv_scenario
    ab_hp_c_inv[scenario] = ab_hp_c_inv_scenario
    cp_hp_c_inv[scenario] = cp_hp_c_inv_scenario
    ttes_c_inv[scenario] = ttes_c_inv_scenario
    
    eb_c_fix[scenario] = eb_c_fix_scenario
    hp_c_fix[scenario] = hp_c_fix_scenario
    st_c_fix[scenario] = st_c_fix_scenario
    wi_c_fix[scenario] = wi_c_fix_scenario
    gt_c_fix[scenario] = gt_c_fix_scenario
    dgt_c_fix[scenario] = dgt_c_fix_scenario
    ieh_c_fix[scenario] = ieh_c_fix_scenario
    chp_c_fix[scenario] = chp_c_fix_scenario
    ab_ct_c_fix[scenario] = ab_ct_c_fix_scenario
    ab_hp_c_fix[scenario] = ab_hp_c_fix_scenario
    cp_hp_c_fix[scenario] = cp_hp_c_fix_scenario
    ttes_c_fix[scenario] = ttes_c_fix_scenario
    
    eb_c_var[scenario] = eb_c_var_scenario
    hp_c_var[scenario] = hp_c_var_scenario
    st_c_var[scenario] = st_c_var_scenario
    wi_c_var[scenario] = wi_c_var_scenario
    gt_c_var[scenario] = gt_c_var_scenario
    dgt_c_var[scenario] = dgt_c_var_scenario
    ieh_c_var[scenario] = ieh_c_var_scenario
    chp_c_var[scenario] = chp_c_var_scenario
    ab_ct_c_var[scenario] = ab_ct_c_var_scenario
    ab_hp_c_var[scenario] = ab_hp_c_var_scenario
    cp_hp_c_var[scenario] = cp_hp_c_var_scenario
    ttes_c_var[scenario] = ttes_c_var_scenario
    
    eb_elec[scenario] = eb_elec_scenario
    hp_elec[scenario] = hp_elec_scenario
    st_elec[scenario] = st_elec_scenario
    gt_elec[scenario] = gt_elec_scenario
    dgt_elec[scenario] = dgt_elec_scenario
    ieh_elec[scenario] = ieh_elec_scenario
    ab_ct_elec[scenario] = ab_ct_elec_scenario
    ab_hp_elec[scenario] = ab_hp_elec_scenario
    cp_hp_elec[scenario] = cp_hp_elec_scenario
    ttes_elec[scenario] = ttes_elec_scenario
    
    ttes_soc[scenario] = ttes_soc_scenario
    
    electricity_price[scenario] = electricity_price_scenario
    electricity_co2_share[scenario] = electricity_co2_share_scenario
    gas_price[scenario] = gas_price_scenario
    co2_price[scenario] = co2_price_scenario

#%% FIG 0 - Demand dispatch

df_0 = pd.DataFrame({'hour': hours, 'heating_demand': heating_demand[visualize_scenario][visualize_year], 'eb': eb_heat_in[visualize_scenario][visualize_year], 'hp': hp_heat_in[visualize_scenario][visualize_year], 'st': st_heat_in[visualize_scenario][visualize_year], 'wi': wi_heat_in[visualize_scenario][visualize_year], 'gt': gt_heat_in[visualize_scenario][visualize_year], 'dgt': dgt_heat_in[visualize_scenario][visualize_year], 'ieh': ieh_heat_in[visualize_scenario][visualize_year], 'chp': chp_heat_in[visualize_scenario][visualize_year], 'ab_ct-': ab_ct_heat_out[visualize_scenario][visualize_year], 'ab_hp+': ab_hp_heat_in[visualize_scenario][visualize_year], 'ab_hp-': ab_hp_heat_out[visualize_scenario][visualize_year], 'cp_hp+': cp_hp_heat_in[visualize_scenario][visualize_year], 'ttes+': ttes_heat_in[visualize_scenario][visualize_year], 'ttes-': ttes_heat_out[visualize_scenario][visualize_year]})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cp_hp+'], mode='lines', name='Compression with heat pump feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_hp-'], mode='lines', name='Absorption with heat pump take out', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_hp+'], mode='lines', name='Absorption with heat pump feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['ab_ct-'], mode='lines', name='Absorption with cooling tower take out', stackgroup='two', line=dict(color='grey')))
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
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['heating_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

heating_demand_sorted_1 = sorted(heating_demand[visualize_scenario][visualize_year], reverse=True)
eb_heat_in_sorted_1 = sorted(eb_heat_in[visualize_scenario][visualize_year], reverse=True)
hp_heat_in_sorted_1 = sorted(hp_heat_in[visualize_scenario][visualize_year], reverse=True)
st_heat_in_sorted_1 = sorted(st_heat_in[visualize_scenario][visualize_year], reverse=True)
wi_heat_in_sorted_1 = sorted(wi_heat_in[visualize_scenario][visualize_year], reverse=True)
gt_heat_in_sorted_1 = sorted(gt_heat_in[visualize_scenario][visualize_year], reverse=True)
dgt_heat_in_sorted_1 = sorted(dgt_heat_in[visualize_scenario][visualize_year], reverse=True)
ieh_heat_in_sorted_1 = sorted(ieh_heat_in[visualize_scenario][visualize_year], reverse=True)
chp_heat_in_sorted_1 = sorted(chp_heat_in[visualize_scenario][visualize_year], reverse=True)
ab_ct_heat_out_sorted_1 = sorted(ab_ct_heat_out[visualize_scenario][visualize_year], reverse=True)
ab_hp_heat_in_sorted_1 = sorted(ab_hp_heat_in[visualize_scenario][visualize_year], reverse=True)
ab_hp_heat_out_sorted_1 = sorted(ab_hp_heat_out[visualize_scenario][visualize_year], reverse=True)
cp_hp_heat_in_sorted_1 = sorted(cp_hp_heat_in[visualize_scenario][visualize_year], reverse=True)
ttes_heat_in_sorted_1 = sorted(ttes_heat_in[visualize_scenario][visualize_year], reverse=True)
ttes_heat_out_sorted_1 = sorted(ttes_heat_out[visualize_scenario][visualize_year])

df_1 = pd.DataFrame({'hour': hours, 'heating_demand': heating_demand_sorted_1, 'eb': eb_heat_in_sorted_1, 'hp': hp_heat_in_sorted_1, 'st': st_heat_in_sorted_1, 'wi': wi_heat_in_sorted_1, 'gt': gt_heat_in_sorted_1, 'dgt': dgt_heat_in_sorted_1, 'ieh': ieh_heat_in_sorted_1, 'chp': chp_heat_in_sorted_1, 'ab_ct-': ab_ct_heat_out_sorted_1, 'ab_hp+': ab_hp_heat_in_sorted_1, 'ab_hp-': ab_hp_heat_out_sorted_1, 'cp_hp+': cp_hp_heat_in_sorted_1, 'ttes+': ttes_heat_in_sorted_1, 'ttes-': ttes_heat_out_sorted_1})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['cp_hp+'], mode='lines', name='Compression with heat pump feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ab_hp-'], mode='lines', name='Absorption with heat pump take out', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ab_hp+'], mode='lines', name='Absorption with heat pump feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['ab_ct-'], mode='lines', name='Absorption with cooling tower take out', stackgroup='two', line=dict(color='grey')))
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
fig.add_trace(go.Scatter(x=df_1['hour'], y=df_1['heating_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

index_sorted = sorted(range(len(heating_demand[visualize_scenario][visualize_year])), key=lambda i: heating_demand[visualize_scenario][visualize_year][i], reverse=True)
heating_demand_sorted_2 = [heating_demand[visualize_scenario][visualize_year][i] for i in index_sorted]
eb_heat_in_sorted_2 = [eb_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
hp_heat_in_sorted_2 = [hp_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
st_heat_in_sorted_2 = [st_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
wi_heat_in_sorted_2 = [wi_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
gt_heat_in_sorted_2 = [gt_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
dgt_heat_in_sorted_2 = [dgt_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ieh_heat_in_sorted_2 = [ieh_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
chp_heat_in_sorted_2 = [chp_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ab_ct_heat_out_sorted_2 = [ab_ct_heat_out[visualize_scenario][visualize_year][i] for i in index_sorted]
ab_hp_heat_in_sorted_2 = [ab_hp_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ab_hp_heat_out_sorted_2 = [ab_hp_heat_out[visualize_scenario][visualize_year][i] for i in index_sorted]
cp_hp_heat_in_sorted_2 = [cp_hp_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ttes_heat_in_sorted_2 = [ttes_heat_in[visualize_scenario][visualize_year][i] for i in index_sorted]
ttes_heat_out_sorted_2 = [ttes_heat_out[visualize_scenario][visualize_year][i] for i in index_sorted]

df_2 = pd.DataFrame({'hour': hours, 'heating_demand': heating_demand_sorted_2, 'eb': eb_heat_in_sorted_2, 'hp': hp_heat_in_sorted_2, 'st': st_heat_in_sorted_2, 'wi': wi_heat_in_sorted_2, 'gt': gt_heat_in_sorted_2, 'dgt': dgt_heat_in_sorted_2, 'ieh': ieh_heat_in_sorted_2, 'chp': chp_heat_in_sorted_2, 'ab_ct-': ab_ct_heat_out_sorted_2, 'ab_hp+': ab_hp_heat_in_sorted_2, 'ab_hp-': ab_hp_heat_out_sorted_2, 'cp_hp+': cp_hp_heat_in_sorted_2, 'ttes+': ttes_heat_in_sorted_2, 'ttes-': ttes_heat_out_sorted_2})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['cp_hp+'], mode='lines', name='Compression with heat pump feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ab_hp-'], mode='lines', name='Absorption with heat pump take out', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ab_hp+'], mode='lines', name='Absorption with heat pump feed in', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ab_ct-'], mode='lines', name='Absorption with cooling tower take out', stackgroup='two', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['chp'], mode='lines', name='Combined heat and power', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['wi'], mode='lines', name='Waste incineration', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['dgt'], mode='lines', name='Deep geothermal', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['st'], mode='lines', name='Solar thermal', stackgroup='one', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['gt'], mode='lines', name='Geothermal', stackgroup='one', line=dict(color='#00CC96')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['hp'], mode='lines', name='Heat pump', stackgroup='one', line=dict(color='#19D3F3')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ieh'], mode='lines', name='Industrial excess heat', stackgroup='one', line=dict(color='#B6E880')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['eb'], mode='lines', name='Electric boiler', stackgroup='one', line=dict(color='#FF6692')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ttes-'], mode='lines', name='TTES store', stackgroup='two', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['ttes+'], mode='lines', name='TTES feed in', stackgroup='one', line=dict(color='#FFA15A')))
fig.add_trace(go.Scatter(x=df_2['hour'], y=df_2['heating_demand'], mode='lines', name='Demand', line=dict(color='#EF553B', width=2)))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

#%% FIG 1 - Technology dispatch

df_3 = pd.DataFrame({'hour': dict(zip(scenarios, [hours]*len(scenarios))), 'eb': eb_heat_in, 'hp': hp_heat_in, 'st': st_heat_in, 'wi': wi_heat_in, 'gt': gt_heat_in, 'dgt': dgt_heat_in, 'ieh': ieh_heat_in, 'chp': chp_heat_in, 'ab_ct-': ab_ct_heat_out, 'ab_hp+': ab_hp_heat_in, 'ab_hp-': ab_hp_heat_out, 'cp_hp+': cp_hp_heat_in, 'ttes+': ttes_heat_in, 'ttes-': ttes_heat_out})

technologies_abb = ['eb', 'hp', 'st', 'wi', 'gt', 'dgt', 'ieh', 'chp', 'ab_ct-', 'ab_hp+', 'ab_hp-', 'cp_hp+', 'ttes+', 'ttes-']
technologies_name = {'eb': 'Electric boiler', 'hp': 'Heat pump', 'st': 'Solar thermal', 'wi': 'Waste incineration', 'gt': 'Geothermal', 'dgt': 'Deep geothermal', 'ieh': 'Industrial excess heat', 'chp': 'Combined heat and power', 'ab_ct-': 'Absorption with cooling tower take out', 'ab_hp+': 'Absorption with heat pump feed in', 'ab_hp-': 'Absorption with heat pump take out', 'cp_hp+': 'Compression with heat pump feed in', 'ttes+': 'TTES feed in', 'ttes-': 'TTES store'}

for technology in technologies_abb: 
    fig = go.Figure()
    
    for scenario in scenarios:
        fig.add_trace(go.Scatter(x=df_3['hour'][scenario], y=df_3[technology][scenario][visualize_year], mode='lines', name=scenario))

    fig.update_layout(title=dict(text=technologies_name[technology], font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

    fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Winter week', 'Summer week'))

fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['gt'][scenarios[0]][visualize_year][:168], mode='lines', name='Scenario 1: reference', line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['gt'][scenarios[12]][visualize_year][:168], mode='lines', name='Scenario 13: zero co2 price', line=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)) + list(range(168))[::-1], y=df_3['gt'][scenarios[0]][visualize_year][:168] + df_3['gt'][scenarios[12]][visualize_year][:168][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)

#fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['gt'][scenarios[12]][visualize_year], mode='lines', name='Scenario 1: high electricity price', fill='tonexty', fillcolor='#00CC96'))

fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_3['gt'][scenarios[0]][visualize_year][4380:4548], mode='lines', name='Scenario 1: reference', line=dict(color='#636EFA'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_3['gt'][scenarios[12]][visualize_year][4380:4548], mode='lines', name='Scenario 13: zero co2 price', line=dict(color='#00CC96'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)) + list(range(4380, 4548))[::-1], y=df_3['gt'][scenarios[0]][visualize_year][4380:4548] + df_3['gt'][scenarios[12]][visualize_year][4380:4548][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=2)

fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=1)
fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=2)

fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Geothermal', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Winter week', 'Summer week'))

fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['ieh'][scenarios[0]][visualize_year][:168], mode='lines', name='Scenario 1: reference', line=dict(color='#636EFA')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['ieh'][scenarios[12]][visualize_year][:168], mode='lines', name='Scenario 13: zero co2 price', line=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Scatter(x=list(range(168)) + list(range(168))[::-1], y=df_3['ieh'][scenarios[0]][visualize_year][:168] + df_3['ieh'][scenarios[12]][visualize_year][:168][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)

#fig.add_trace(go.Scatter(x=list(range(168)), y=df_3['gt'][scenarios[12]][visualize_year], mode='lines', name='Scenario 1: high electricity price', fill='tonexty', fillcolor='#00CC96'))

fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_3['ieh'][scenarios[0]][visualize_year][4380:4548], mode='lines', name='Scenario 1: reference', line=dict(color='#636EFA'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)), y=df_3['ieh'][scenarios[12]][visualize_year][4380:4548], mode='lines', name='Scenario 13: zero co2 price', line=dict(color='#00CC96'), showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=list(range(4380, 4548)) + list(range(4380, 4548))[::-1], y=df_3['ieh'][scenarios[0]][visualize_year][4380:4548] + df_3['ieh'][scenarios[12]][visualize_year][4380:4548][::-1], fill='toself', fillcolor='rgba(128, 128, 128, 0.1)', fillpattern=dict(shape='/', fgcolor='black'), line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=2)

fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=1)
fig.update_xaxes(title_text='Hour', titlefont=dict(size=20), tickformat=',', tickfont=dict(size=20), row=1, col=2)

fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Industrial excess heat', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend_title=dict(text='Scenarios', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

#%% FIG 2 - SOC

df_4 = pd.DataFrame({'hour': hours, 'ttes_absolute': ttes_soc[visualize_scenario][visualize_year]})
df_4['ttes_relative'] = (df_4['ttes_absolute'] / df_4['ttes_absolute'].max()) * 100

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_4['hour'], y=df_4['ttes_absolute'], mode='lines', name='TTES SOC', line=dict(color='#FFA15A', width=2)))
fig.add_trace(go.Scatter(x=df_4['hour'], y=df_4['ttes_relative'], mode='lines', name='TTES SOC', line=dict(color='#FFA15A', width=2), yaxis='y2', showlegend=False))

fig.update_layout(title=dict(text='State of charge', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='State of charge in MWh', titlefont=dict(size=20), tickfont=dict(size=20), range=[0, df_4['ttes_absolute'].max() * 1.1], tickvals=np.linspace(0, df_4['ttes_absolute'].max(), 6), tickformat='.2f'), yaxis2=dict(title='State of charge in %', titlefont=dict(size=20), tickfont=dict(size=20), overlaying='y', side='right', range=[0, 100 * 1.1]), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

#%% FIG 3 - Investments

# eb_inv = []
# hp_inv = []
# st_inv = []
# wi_inv = []
# gt_inv = []
# dgt_inv = []
# ieh_inv = []
# chp_inv = []
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
#     ttes_inv.append(py.value(model.v_ttes_k_inv[visualize_scenario, year]))

# technologies = ['Electric Boiler', 'Heat Pump', 'Solar Thermal', 'Waste Incineration', 'Geothermal', 'Deep Geothermal', 'Industrial Excess Heat', 'Combined Heat and Power', 'TTES']
# technologies_map = {'Electric Boiler': eb_inv, 'Heat Pump': hp_inv, 'Solar Thermal': st_inv, 'Waste Incineration': wi_inv, 'Geothermal': gt_inv, 'Deep Geothermal': dgt_inv, 'Industrial Excess Heat': ieh_inv, 'Combined Heat and Power': chp_inv, 'TTES': ttes_inv}
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

ratio_eb_inv = []
ratio_hp_inv = []
ratio_gt_inv = []
ratio_ieh_inv = []
ratio_inv = []
index = 0

for year in years[:5]:
    index +=1
    
    heating_eb_inv_sum = sum(list(eb_inv[visualize_scenario].values())[:index])
    heating_hp_inv_sum = sum(list(hp_inv[visualize_scenario].values())[:index])
    heating_gt_inv_sum = sum(list(gt_inv[visualize_scenario].values())[:index])
    heating_ieh_inv_sum = sum(list(ieh_inv[visualize_scenario].values())[:index])
    heating_technology_inv_sum = sum(list(eb_inv[visualize_scenario].values())[:index]) + sum(list(hp_inv[visualize_scenario].values())[:index]) + sum(list(st_inv[visualize_scenario].values())[:index]) + sum(list(wi_inv[visualize_scenario].values())[:index]) + sum(list(gt_inv[visualize_scenario].values())[:index]) + sum(list(dgt_inv[visualize_scenario].values())[:index]) + sum(list(ieh_inv[visualize_scenario].values())[:index]) + sum(list(chp_inv[visualize_scenario].values())[:index])
    storage_technology_inv_sum = sum(list(ttes_inv[visualize_scenario].values())[:index])
    
    ratio_eb_inv.append(heating_eb_inv_sum / storage_technology_inv_sum * 100)
    ratio_hp_inv.append(heating_hp_inv_sum / storage_technology_inv_sum * 100)
    ratio_gt_inv.append(heating_gt_inv_sum / storage_technology_inv_sum * 100)
    ratio_ieh_inv.append(heating_ieh_inv_sum / storage_technology_inv_sum * 100)
    ratio_inv.append(heating_technology_inv_sum / storage_technology_inv_sum * 100)
    
    technologies = ['Electric boiler', 'Heat pump', 'Solar thermal', 'Waste incineration', 'Geothermal', 'Deep geothermal', 'Industrial excess heat', 'Combined heat and power', 'Absorption with cooling tower', 'Absorption with heat pump', 'Compression with heat pump']
    technologies_map = {'Electric boiler': eb_inv, 'Heat pump': hp_inv, 'Solar thermal': st_inv, 'Waste incineration': wi_inv, 'Geothermal': gt_inv, 'Deep geothermal': dgt_inv, 'Industrial excess heat': ieh_inv, 'Combined heat and power': chp_inv, 'Absorption with cooling tower': ab_ct_inv, 'Absorption with heat pump': ab_hp_inv, 'Compression with heat pump': cp_hp_inv}
    storages = ['Tank thermal energy storage']
    storages_map = {'Tank thermal energy storage': ttes_inv}

fig = go.Figure()

fig = sp.make_subplots(rows=2, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}], [{'colspan': 1}, None]], subplot_titles=('Heating technology investments', 'Storage technology investments', 'Ratio heating to storage capacity'))

fig.add_trace(go.Scatter(x=years[:5], y=ratio_inv[:5], name='Ratio'), row=2, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(storages_map['Tank thermal energy storage'][visualize_scenario].values())[:5], name='Tank thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Electric boiler'][visualize_scenario].values())[:5], name='Electric boiler', marker=dict(color='#FF6692')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Industrial excess heat'][visualize_scenario].values())[:5], name='Industrial excess heat', marker=dict(color='#B6E880')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Heat pump'][visualize_scenario].values())[:5], name='Heat pump', marker=dict(color='#19D3F3')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Geothermal'][visualize_scenario].values())[:5], name='Geothermal', marker=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Solar thermal'][visualize_scenario].values())[:5], name='Solar thermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Deep geothermal'][visualize_scenario].values())[:5], name='Deep geothermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Waste incineration'][visualize_scenario].values())[:5], name='Waste incineration', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Combined heat and power'][visualize_scenario].values())[:5], name='Combined heat and power', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with cooling tower'][visualize_scenario].values())[:5], name='Absorption with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with heat pump'][visualize_scenario].values())[:5], name='Absorption with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with heat pump'][visualize_scenario].values())[:5], name='Compression with heat pump', marker=dict(color='grey')), row=1, col=1)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=2)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=2, col=1)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=1)

fig.update_yaxes(range=[0, 20], row=2, col=1)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(x=0.7, y=0, traceorder='normal', font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack', width=1200, height=900)

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=2, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}], [{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Heating technology investments', 'Storage technology investments', 'Ratio heating to storage capacity', 'Ratio heating to storage capacity'))

fig.add_trace(go.Scatter(x=years[:5], y=ratio_inv[:5], name='Ratio total', line=dict(color='#EF553B')), row=2, col=2)

fig.add_trace(go.Scatter(x=years[:5], y=ratio_gt_inv[:5], name='Ratio geothermal', line=dict(color='#00CC96')), row=2, col=1)
fig.add_trace(go.Scatter(x=years[:5], y=ratio_hp_inv[:5], name='Ratio heat pump', line=dict(color='#19D3F3')), row=2, col=1)
fig.add_trace(go.Scatter(x=years[:5], y=ratio_ieh_inv[:5], name='Ratio industrial excess heat', line=dict(color='#B6E880')), row=2, col=1)
fig.add_trace(go.Scatter(x=years[:5], y=ratio_eb_inv[:5], name='Ratio electric boiler', line=dict(color='#FF6692')), row=2, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with heat pump'][visualize_scenario].values())[:5], name='Compression with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with heat pump'][visualize_scenario].values())[:5], name='Absorption with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with cooling tower'][visualize_scenario].values())[:5], name='Absorption with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Combined heat and power'][visualize_scenario].values())[:5], name='Combined heat and power', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Waste incineration'][visualize_scenario].values())[:5], name='Waste incineration', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Deep geothermal'][visualize_scenario].values())[:5], name='Deep geothermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Solar thermal'][visualize_scenario].values())[:5], name='Solar thermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Geothermal'][visualize_scenario].values())[:5], name='Geothermal', marker=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Heat pump'][visualize_scenario].values())[:5], name='Heat pump', marker=dict(color='#19D3F3')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Industrial excess heat'][visualize_scenario].values())[:5], name='Industrial excess heat', marker=dict(color='#B6E880')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Electric boiler'][visualize_scenario].values())[:5], name='Electric boiler', marker=dict(color='#FF6692')), row=1, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(storages_map['Tank thermal energy storage'][visualize_scenario].values())[:5], name='Tank thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=2)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=2, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=2, col=2)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=1)
fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20), row=2, col=2)

fig.update_yaxes(range=[0, 10], row=2, col=1)
fig.update_yaxes(range=[0, 20], row=2, col=2)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack')

fig.show()

fig = go.Figure()

fig = sp.make_subplots(rows=1, cols=2, specs=[[{'colspan': 1}, {'colspan': 1}]], subplot_titles=('Heating technology investments', 'Storage technology investments'))

fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Compression with heat pump'][visualize_scenario].values())[:5], name='Compression with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with heat pump'][visualize_scenario].values())[:5], name='Absorption with heat pump', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Absorption with cooling tower'][visualize_scenario].values())[:5], name='Absorption with cooling tower', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Combined heat and power'][visualize_scenario].values())[:5], name='Combined heat and power', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Waste incineration'][visualize_scenario].values())[:5], name='Waste incineration', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Deep geothermal'][visualize_scenario].values())[:5], name='Deep geothermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Solar thermal'][visualize_scenario].values())[:5], name='Solar thermal', marker=dict(color='grey')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Geothermal'][visualize_scenario].values())[:5], name='Geothermal', marker=dict(color='#00CC96')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Heat pump'][visualize_scenario].values())[:5], name='Heat pump', marker=dict(color='#19D3F3')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Industrial excess heat'][visualize_scenario].values())[:5], name='Industrial excess heat', marker=dict(color='#B6E880')), row=1, col=1)
fig.add_trace(go.Bar(x=years[:5], y=list(technologies_map['Electric boiler'][visualize_scenario].values())[:5], name='Electric boiler', marker=dict(color='#FF6692')), row=1, col=1)

fig.add_trace(go.Bar(x=years[:5], y=list(storages_map['Tank thermal energy storage'][visualize_scenario].values())[:5], name='Tank thermal energy storage', marker=dict(color='#FFA15A')), row=1, col=2)

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=1)
fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5], row=1, col=2)

fig.update_yaxes(title_text='Newly installed capacity in MW', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=1)
fig.update_yaxes(title_text='Newly installed capacity in MWh', titlefont=dict(size=20), tickfont=dict(size=20), row=1, col=2)

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), annotations=[dict(font=dict(size=25))], legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), barmode='stack')

fig.show()

fig = go.Figure()

fig.add_trace(go.Scatter(x=years[:5], y=ratio_eb_inv[:5], name='Ratio electric boiler', line=dict(width=4, color='#FF6692')))
fig.add_trace(go.Scatter(x=years[:5], y=ratio_ieh_inv[:5], name='Ratio industrial excess heat', line=dict(width=4, color='#B6E880')))
fig.add_trace(go.Scatter(x=years[:5], y=ratio_hp_inv[:5], name='Ratio heat pump', line=dict(width=4, color='#19D3F3')))
fig.add_trace(go.Scatter(x=years[:5], y=ratio_gt_inv[:5], name='Ratio geothermal', line=dict(width=4, color='#00CC96')))

fig.update_xaxes(title_text='Investment year', titlefont=dict(size=20), tickfont=dict(size=20), tickvals=years[:5])

fig.update_yaxes(title_text='Ratio in %', titlefont=dict(size=20), tickfont=dict(size=20))

fig.update_yaxes(range=[0, 10])

fig.update_layout(title=dict(text='Investments', font=dict(size=30)), legend=dict(font=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)))

fig.show()

#%% FIG 4 - LCOH

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

demand_heat_sum_variation = {}

for building in range(1, 36):
    variation = 0
    
    for scenario in scenarios:
            
        for year in years:
            variation += buildings[building][year] * demand_heat_variation[scenario][year]
    
    demand_heat_sum_variation[building] = variation / len(scenarios)

buildings_demand = {}
buildings_demand_sum = {}
buildings_lcoh = {}

path_to_file_heating_demand_building = os.path.join(path_to_input_folder, 'districts_heating_demand_phase2.xlsx')
df_heating_demand_building = pd.read_excel(path_to_file_heating_demand_building)

for building in range(1, 36):
    heating_demand_building = df_heating_demand_building[f'heating_demand_building_{building}'].tolist()
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
                    building_c_sum += buildings[building][year] * demand_heat_variation[scenario][year] * buildings_demand[building][hour] / eta_electricity * (electricity_price[scenario][year][hour] + electricity_co2_share[scenario][year][hour] * co2_price[scenario][year])
            
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
building_lcoh_min_index = [i + 1 for i in sorted(range(len(building_lcoh_min)), key=lambda i: building_lcoh_min[i], reverse=True)]
building_lcoh_avg_index = [i + 1 for i in sorted(range(len(building_lcoh_avg)), key=lambda i: building_lcoh_avg[i], reverse=True)]

x_bar = []
y_bar = []
widths = []
bases = []
labels = []

for building in range(1, 36):
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
    sum_heating_cost = 0
    sum_heating_demand = 0
    for year in years:
        sum_heating_demand_scenario = 0
        
        sum_heating_demand_scenario = sum(heating_demand[scenario][year])
        sum_heating_demand += sum_heating_demand_scenario * year_expansion_range[year]
        sum_heating_cost += sum(eb_c_var[scenario][year]) + sum(hp_c_var[scenario][year]) + sum(st_c_var[scenario][year]) + sum(wi_c_var[scenario][year]) + sum(gt_c_var[scenario][year]) + sum(dgt_c_var[scenario][year]) + sum(ieh_c_var[scenario][year]) + sum(chp_c_var[scenario][year]) + sum(ab_ct_c_var[scenario][year]) + sum(ab_hp_c_var[scenario][year]) + sum(cp_hp_c_var[scenario][year]) * cp_seer / (cp_seer + cp_hp_cop) + sum(ttes_c_var[scenario][year]) + \
                            eb_c_inv[scenario][year] + hp_c_inv[scenario][year] + st_c_inv[scenario][year] + wi_c_inv[scenario][year] + gt_c_inv[scenario][year] + dgt_c_inv[scenario][year] + ieh_c_inv[scenario][year] + chp_c_inv[scenario][year] + ab_ct_c_inv[scenario][year] + ab_hp_c_inv[scenario][year] + cp_hp_c_inv[scenario][year] * (1 + 1 / cp_seer) / (1 + 1 + 1 / cp_seer) + ttes_c_inv[scenario][year] + \
                            eb_c_fix[scenario][year] + hp_c_fix[scenario][year] + st_c_fix[scenario][year] + wi_c_fix[scenario][year] + gt_c_fix[scenario][year] + dgt_c_fix[scenario][year] + ieh_c_fix[scenario][year] + chp_c_fix[scenario][year] + ab_ct_c_fix[scenario][year] + ab_hp_c_fix[scenario][year] + cp_hp_c_fix[scenario][year] * (1 + 1 / cp_seer) / (1 + 1 + 1 / cp_seer) + ttes_c_fix[scenario][year]
                            
    lcoh[scenario] = sum_heating_cost / sum_heating_demand

fig = go.Figure()

lcoh_min = min(lcoh, key=lcoh.get)
lcoh_max = max(lcoh, key=lcoh.get)

# for scenario in scenarios:
#     fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario], y=[lcoh[scenario], lcoh[scenario]], mode='lines', name=scenario))

fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario], y=[lcoh[lcoh_min], lcoh[lcoh_min]], mode='lines', line=dict(color='black'), name=lcoh_min, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario], y=[lcoh[lcoh_max], lcoh[lcoh_max]], mode='lines', line=dict(color='black'), name=lcoh_max, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario, sum_heating_demand_scenario, 0], y=[lcoh[lcoh_min], lcoh[lcoh_min], lcoh[lcoh_max], lcoh[lcoh_max]],  fill='toself', fillcolor='gray', opacity=0.5, line=dict(color='gray'), showlegend=False))
# , fillpattern=dict(shape="x",  fgcolor="black")

for i in range(len(x_bar)):
    fig.add_trace(go.Bar(x=[x_bar[i]], y=[y_bar[i]], width=widths[i], base=bases[i], text=labels[i], textposition='outside', textangle=0, name=labels[i]))

fig.update_xaxes(range=[0, sum_heating_demand_scenario])

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
#     fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario], y=[lcoh[scenario], lcoh[scenario]], mode='lines', name=scenario))

fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario], y=[lcoh[lcoh_min], lcoh[lcoh_min]], mode='lines', line=dict(color='rgb(253, 180, 98)'), name=lcoh_min, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario], y=[lcoh[lcoh_max], lcoh[lcoh_max]], mode='lines', line=dict(color='rgb(253, 180, 98)'), name=lcoh_max, showlegend=False))
fig.add_trace(go.Scatter(x=[0, sum_heating_demand_scenario, sum_heating_demand_scenario, 0], y=[lcoh[lcoh_min], lcoh[lcoh_min], lcoh[lcoh_max], lcoh[lcoh_max]], name='DH-system', fill='toself', fillcolor='rgb(253, 180, 98)', opacity=0.5, line=dict(color='rgb(253, 180, 98)')))
# , fillpattern=dict(shape="x",  fgcolor="black")

for i in range(len(x_bar)-1):
    fig.add_trace(go.Bar(x=[x_bar[i]], y=[y_bar[i]], width=widths[i], base=bases[i], marker=dict(color='rgb(128, 177, 211)'), showlegend=False))

fig.add_trace(go.Bar(x=[x_bar[i+1]], y=[y_bar[i+1]], width=widths[i+1], base=bases[i+1], marker=dict(color='rgb(128, 177, 211)'), name='Buildings'))

fig.update_xaxes(range=[0, sum_heating_demand_scenario])
fig.update_yaxes(range=[0, bases[0]+y_bar[0]+20])

fig.update_layout(title=dict(text='Levelized costs of heating', font=dict(size=30)), uniformtext_minsize=10, uniformtext_mode='show', xaxis=dict(title='Annual building heat demand in MWh', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='LCOH in $/MWh', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='LCOH', font=dict(size=20)), legend=dict(font=dict(size=20)), barmode='overlay', bargap=0)

fig.show()

#%% FIG 5 - Load duration curve

load_duration_curve_demand = heating_demand[visualize_scenario][visualize_year]

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
    load_duration_curve_scenario = [elec_0 + elec_1 + elec_2 + elec_3 + elec_4 + elec_5 + elec_6 + elec_7 + elec_8 + elec_9 for elec_0, elec_1, elec_2, elec_3, elec_4, elec_5, elec_6, elec_7, elec_8, elec_9 in zip(eb_elec[scenario][visualize_year], hp_elec[scenario][visualize_year], st_elec[scenario][visualize_year], gt_elec[scenario][visualize_year], dgt_elec[scenario][visualize_year], ieh_elec[scenario][visualize_year], ab_ct_elec[scenario][visualize_year], ab_hp_elec[scenario][visualize_year], cp_hp_elec[scenario][visualize_year], ttes_elec[scenario][visualize_year])]
    load_duration_curve[scenario] =  sorted(load_duration_curve_scenario, reverse=True)

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=load_duration_curve_demand, mode='lines', fill='tozeroy', name='Buildings'))
fig.add_trace(go.Scatter(x=df_0['hour'], y=load_duration_curve[visualize_scenario], mode='lines', fill='tozeroy', name=visualize_scenario))

fig.update_layout(title=dict(text='Load duration curve', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Electric energy per hour in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Profiles', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()
