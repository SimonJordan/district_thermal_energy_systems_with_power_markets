import os
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import plotly.subplots as sp

# assumptions
eta_electricity = 0.99
cp_seer = 5
cp_hp_cop = 6.0525

pio.renderers.default = 'browser'

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, '..', 'inputs')
path_to_result_folder = os.path.join(cur_dir, '..', 'results')
path_to_file_scenarios = os.path.join(path_to_result_folder, 'scenarios.txt')

scenarios = []
scenarios_weighting = {}

with open(path_to_file_scenarios, 'r') as file:
    for line in file:
        scenario, weighting = line.strip().split(',')
        scenarios.append(scenario)
        scenarios_weighting[scenario] = float(weighting)
        
years = [2025, 2030, 2035, 2040, 2045, 2050]
year_expansion_range = {2025: 5, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 1}
hours = list(range(8760))

visualize_scenario = '1_reference'
visualize_year = 2035

heating_demand = {}
eb_heat_in = {}
gb_heat_in = {}
hp_heat_in = {}
st_heat_in = {}
wi_heat_in = {}
ieh_heat_in = {}
chp_heat_in = {}
ab_ct_heat_out = {}
ab_hp_heat_in = {}
ab_hp_heat_out = {}
cp_hp_heat_in = {}
ttes_heat_in = {}
ttes_heat_out = {}
btes_heat_in = {}

cooling_demand = {}
ac_cool_in = {}
ab_ct_cool_in = {}
ab_hp_cool_in = {}
cp_ct_cool_in = {}
cp_hp_cool_in = {}
ites_cool_in = {}
ites_cool_out = {}

eb_inv = {}
gb_inv = {}
hp_inv = {}
st_inv = {}
wi_inv = {}
ieh_inv = {}
chp_inv = {}
ab_ct_inv = {}
ab_hp_inv = {}
cp_hp_inv = {}
ttes_inv = {}
btes_inv = {}
ac_inv = {}
cp_ct_inv = {}
ites_inv = {}

eb_elec = {}
hp_elec = {}
st_elec = {}
ieh_elec = {}
ab_ct_elec = {}
ab_hp_elec = {}
cp_hp_elec = {}
ttes_elec = {}
btes_elec = {}
ac_elec = {}
cp_ct_elec = {}
ites_elec = {}

ttes_soc = {}
btes_soc = {}
ites_soc = {}

electricity_price = {}
electricity_co2_share = {}
gas_price = {}
co2_price = {}

for scenario in scenarios:
    print(scenario)
    heating_demand_scenario = {}
    eb_heat_in_scenario = {}
    gb_heat_in_scenario = {}
    hp_heat_in_scenario = {}
    st_heat_in_scenario = {}
    wi_heat_in_scenario = {}
    ieh_heat_in_scenario = {}
    chp_heat_in_scenario = {}
    ab_ct_heat_out_scenario = {}
    ab_hp_heat_in_scenario = {}
    ab_hp_heat_out_scenario = {}
    cp_hp_heat_in_scenario = {}
    ttes_heat_in_scenario = {}
    ttes_heat_out_scenario = {}
    btes_heat_in_scenario = {}
    
    cooling_demand_scenario = {}
    ac_cool_in_scenario = {}
    ab_ct_cool_in_scenario = {}
    ab_hp_cool_in_scenario = {}
    cp_ct_cool_in_scenario = {}
    cp_hp_cool_in_scenario = {}
    ites_cool_in_scenario = {}
    ites_cool_out_scenario = {}
    
    eb_elec_scenario = {}
    hp_elec_scenario = {}
    st_elec_scenario = {}
    ieh_elec_scenario = {}
    ab_ct_elec_scenario = {}
    ab_hp_elec_scenario = {}
    cp_hp_elec_scenario = {}
    ttes_elec_scenario = {}
    btes_elec_scenario = {}
    ac_elec_scenario = {}
    cp_ct_elec_scenario = {}
    ites_elec_scenario = {}
    
    ttes_soc_scenario = {}
    btes_soc_scenario = {}
    ites_soc_scenario = {}
    
    electricity_price_scenario = {}
    gas_price_scenario = {}
    co2_price_scenario = {}
    
    path_to_heat_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_heat_supply.xlsx')
    path_to_cool_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_cool_supply.xlsx')
    path_to_elec_consumption = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_consumption.xlsx')
    path_to_elec_price_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_gas_price.xlsx')
    path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
    path_to_storage_soc = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_storage_soc.xlsx')
    
    for year in years:
        print(year)
        df_heat_supply = pd.read_excel(path_to_heat_supply, sheet_name=str(year))
        df_cool_supply = pd.read_excel(path_to_cool_supply, sheet_name=str(year))
        df_elec_consumption = pd.read_excel(path_to_elec_consumption, sheet_name=str(year))
        df_elec_price_gas_price = pd.read_excel(path_to_elec_price_gas_price, sheet_name=str(year))
        df_co2_price = pd.read_excel(path_to_co2_price, sheet_name=str(year))
        df_storage_soc = pd.read_excel(path_to_storage_soc, sheet_name=str(year))
        
        heating_demand_scenario[year] = df_heat_supply['heating'].tolist()
        eb_heat_in_scenario[year] = df_heat_supply['eb'].tolist()
        gb_heat_in_scenario[year] = df_heat_supply['gb'].tolist()
        hp_heat_in_scenario[year] = df_heat_supply['hp'].tolist()
        st_heat_in_scenario[year] = df_heat_supply['st'].tolist()
        wi_heat_in_scenario[year] = df_heat_supply['wi'].tolist()
        ieh_heat_in_scenario[year] = df_heat_supply['ieh'].tolist()
        chp_heat_in_scenario[year] = df_heat_supply['chp'].tolist()
        ab_ct_heat_out_scenario[year] = df_heat_supply['ab_ct-'].tolist()
        ab_hp_heat_in_scenario[year] = df_heat_supply['ab_hp+'].tolist()
        ab_hp_heat_out_scenario[year] = df_heat_supply['ab_hp-'].tolist()
        cp_hp_heat_in_scenario[year] = df_heat_supply['cp_hp+'].tolist()
        ttes_heat_in_scenario[year] = df_heat_supply['ttes+'].tolist()
        ttes_heat_out_scenario[year] = df_heat_supply['ttes-'].tolist()
        btes_heat_in_scenario[year] = df_heat_supply['btes+'].tolist()
        
        cooling_demand_scenario[year] = df_cool_supply['cooling'].tolist()
        ac_cool_in_scenario[year] = df_cool_supply['ac'].tolist()
        ab_ct_cool_in_scenario[year] = df_cool_supply['ab_ct'].tolist()
        ab_hp_cool_in_scenario[year] = df_cool_supply['ab_hp'].tolist()
        cp_ct_cool_in_scenario[year] = df_cool_supply['cp_ct'].tolist()
        cp_hp_cool_in_scenario[year] = df_cool_supply['cp_hp'].tolist()
        ites_cool_in_scenario[year] = df_cool_supply['ites+'].tolist()
        ites_cool_out_scenario[year] = df_cool_supply['ites-'].tolist()
        
        eb_elec_scenario[year] = df_elec_consumption['eb'].tolist()
        hp_elec_scenario[year] = df_elec_consumption['hp'].tolist()
        st_elec_scenario[year] = df_elec_consumption['st'].tolist()
        ieh_elec_scenario[year] = df_elec_consumption['ieh'].tolist()
        ab_ct_elec_scenario[year] = df_elec_consumption['ab_ct'].tolist()
        ab_hp_elec_scenario[year] = df_elec_consumption['ab_hp'].tolist()
        cp_hp_elec_scenario[year] = df_elec_consumption['cp_hp'].tolist()
        ttes_elec_scenario[year] = df_elec_consumption['ttes'].tolist()
        btes_elec_scenario[year] = df_elec_consumption['btes'].tolist()
        ac_elec_scenario[year] = df_elec_consumption['ac'].tolist()
        cp_ct_elec_scenario[year] = df_elec_consumption['cp_ct'].tolist()
        ites_elec_scenario[year] = df_elec_consumption['ites'].tolist()
        
        ttes_soc_scenario[year] = df_storage_soc['ttes'].tolist()
        btes_soc_scenario[year] = df_storage_soc['btes'].tolist()
        ites_soc_scenario[year] = df_storage_soc['ites'].tolist()
        
        electricity_price_scenario[year] = df_elec_price_gas_price['elec'].tolist()
        gas_price_scenario[year] = df_elec_price_gas_price['gas'].tolist()
        co2_price_scenario[year] = df_co2_price['co2'].tolist()[0]
        
    heating_demand[scenario] = heating_demand_scenario
    eb_heat_in[scenario] = eb_heat_in_scenario
    gb_heat_in[scenario] = gb_heat_in_scenario
    hp_heat_in[scenario] = hp_heat_in_scenario
    st_heat_in[scenario] = st_heat_in_scenario
    wi_heat_in[scenario] = wi_heat_in_scenario
    ieh_heat_in[scenario] = ieh_heat_in_scenario
    chp_heat_in[scenario] = chp_heat_in_scenario
    ab_ct_heat_out[scenario] = ab_ct_heat_out_scenario
    ab_hp_heat_in[scenario] = ab_hp_heat_in_scenario
    ab_hp_heat_out[scenario] = ab_hp_heat_out_scenario
    cp_hp_heat_in[scenario] = cp_hp_heat_in_scenario
    ttes_heat_in[scenario] = ttes_heat_in_scenario
    ttes_heat_out[scenario] = ttes_heat_out_scenario
    btes_heat_in[scenario] = btes_heat_in_scenario
    
    cooling_demand[scenario] = cooling_demand_scenario
    ac_cool_in[scenario] = ac_cool_in_scenario
    ab_ct_cool_in[scenario] = ab_ct_cool_in_scenario
    ab_hp_cool_in[scenario] = ab_hp_cool_in_scenario
    cp_ct_cool_in[scenario] = cp_ct_cool_in_scenario
    cp_hp_cool_in[scenario] = cp_hp_cool_in_scenario
    ites_cool_in[scenario] = ites_cool_in_scenario
    ites_cool_out[scenario] = ites_cool_out_scenario
    
    eb_elec[scenario] = eb_elec_scenario
    hp_elec[scenario] = hp_elec_scenario
    st_elec[scenario] = st_elec_scenario
    ieh_elec[scenario] = ieh_elec_scenario
    ab_ct_elec[scenario] = ab_ct_elec_scenario
    ab_hp_elec[scenario] = ab_hp_elec_scenario
    cp_hp_elec[scenario] = cp_hp_elec_scenario
    ttes_elec[scenario] = ttes_elec_scenario
    btes_elec[scenario] = btes_elec_scenario
    ac_elec[scenario] = ac_elec_scenario
    cp_ct_elec[scenario] = cp_ct_elec_scenario
    ites_elec[scenario] = ites_elec_scenario
    
    ttes_soc[scenario] = ttes_soc_scenario
    btes_soc[scenario] = btes_soc_scenario
    ites_soc[scenario] = ites_soc_scenario
    
    electricity_price[scenario] = electricity_price_scenario
    gas_price[scenario] = gas_price_scenario
    co2_price[scenario] = co2_price_scenario

path_to_inv_capacity = os.path.join(path_to_result_folder, '[all]_#_inv_capacity.xlsx')

for year in years:
    df_inv_capacity = pd.read_excel(path_to_inv_capacity, sheet_name=str(year))
    
    eb_inv[year] = df_inv_capacity['eb'].tolist()[0]
    gb_inv[year] = df_inv_capacity['gb'].tolist()[0]
    hp_inv[year] = df_inv_capacity['hp'].tolist()[0]
    st_inv[year] = df_inv_capacity['st'].tolist()[0]
    wi_inv[year] = df_inv_capacity['wi'].tolist()[0]
    ieh_inv[year] = df_inv_capacity['ieh'].tolist()[0]
    chp_inv[year] = df_inv_capacity['chp'].tolist()[0]
    ab_ct_inv[year] = df_inv_capacity['ab_ct'].tolist()[0]
    ab_hp_inv[year] = df_inv_capacity['ab_hp'].tolist()[0]
    cp_hp_inv[year] = df_inv_capacity['cp_hp'].tolist()[0]
    ttes_inv[year] = df_inv_capacity['ttes'].tolist()[0]
    btes_inv[year] = df_inv_capacity['btes'].tolist()[0]
    ac_inv[year] = df_inv_capacity['ac'].tolist()[0]
    cp_ct_inv[year] = df_inv_capacity['cp_ct'].tolist()[0]
    ites_inv[year] = df_inv_capacity['ites'].tolist()[0]

#%%

def count_consumption(values, max_value=0):
    if max_value == 0:
        max_value = max(values)
        
    thresholds = [0.5 * max_value, 0.75 * max_value, 0.9 * max_value]
    
    counts = {'base': 0, 'medium': 0, 'peak': 0, 'very_high_peak': 0}
    
    for v in values:
        if v <= thresholds[0]:
            counts['base'] += 1
        elif v <= thresholds[1]:
            counts['medium'] += 1
        elif v <= thresholds[2]:
            counts['peak'] += 1
        else:
            counts['very_high_peak'] += 1
            
    total = len(values)
    counts_percent = {k: (v, round((v/total)*100, 2)) for k, v in counts.items()}
    return counts_percent

def area_consumption(values, max_value=0):
    if max_value == 0:
        max_value = max(values)
        
    thresholds = [0.5 * max_value, 0.75 * max_value, 0.9 * max_value]
    
    areas = {'base': 0, 'medium': 0, 'peak': 0, 'very_high_peak': 0}
    
    total_area = 0.0
    
    for i in range(len(values)-1):
        v1, v2 = values[i], values[i+1]
        avg_height = (v1 + v2) / 2
        total_area += avg_height
        
        upper_v = max(v1, v2)
        if upper_v <= thresholds[0]:
            areas['base'] += avg_height
        elif upper_v <= thresholds[1]:
            areas['medium'] += avg_height
        elif upper_v <= thresholds[2]:
            areas['peak'] += avg_height
        else:
            areas['very_high_peak'] += avg_height
            
    areas_percent = {k: (round(v, 2), round((v/total_area)*100, 2)) for k, v in areas.items()}
    return areas_percent

def pie_chart(values_1, values_2={}):
    
    if values_2 == {}:
        values_2 = values_1
    
    name_list_1 = []
    value_list_1 = []
    
    name_list_2 = []
    value_list_2 = []
    
    for key_1, value_1 in values_1.items():
        name_list_1.append(key_1)
        value_list_1.append(value_1[1])
    
    for key_2, value_2 in values_2.items():
        name_list_2.append(key_2)
        value_list_2.append(value_2[1])
    
    name_list_1 = [name_list_1[0]] + name_list_1[1:][::-1]
    value_list_1 = [value_list_1[0]] + value_list_1[1:][::-1]
    name_list_2 = [name_list_2[0]] + name_list_2[1:][::-1]
    value_list_2 = [value_list_2[0]] + value_list_2[1:][::-1]
        
    #fig = go.Figure(data=[go.Pie(labels=name_list_1, values=value_list_1)])
    #fig.update_traces(sort=False)
    ###fig.update_traces(direction='clockwise')
    #fig.show()
    
    fig = sp.make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=name_list_1, values=value_list_1, name="Hours"),  1, 1)
    fig.update_traces(sort=False)
    fig.add_trace(go.Pie(labels=name_list_2, values=value_list_2, name="Energy"), 1, 2)
    fig.update_traces(sort=False)
    
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        #title_text="TEXT",
        
        annotations=[dict(text='Hours', x=sum(fig.get_subplot(1, 1).x) / 2, y=0.5,
                          font_size=20, showarrow=False, xanchor="center"),
                     dict(text='Energy', x=sum(fig.get_subplot(1, 2).x) / 2, y=0.5,
                          font_size=20, showarrow=False, xanchor="center")])
    fig.show()
    
elec_consumption = [sum(value) for value in zip(eb_elec[visualize_scenario][visualize_year], hp_elec[scenario][visualize_year], st_elec[scenario][visualize_year], ieh_elec[scenario][visualize_year], ab_ct_elec[scenario][visualize_year], ab_hp_elec[scenario][visualize_year], cp_hp_elec[scenario][visualize_year], ttes_elec[scenario][visualize_year], btes_elec[scenario][visualize_year], ac_elec[scenario][visualize_year], cp_ct_elec[scenario][visualize_year], ites_elec[scenario][visualize_year])]
elec_consumption_max = max(elec_consumption)
elec_consumption_count_1 = count_consumption(elec_consumption)
elec_consumption_area_1 = area_consumption(elec_consumption)

elec_consumption_count_2 = count_consumption([value * 0.92 for value in elec_consumption], elec_consumption_max)
elec_consumption_area_2 = area_consumption([value * 0.92 for value in elec_consumption], elec_consumption_max)


pie_chart(elec_consumption_count_1, elec_consumption_area_1)
pie_chart(elec_consumption_count_2, elec_consumption_area_2)
#({keys: [value * 0.9 for value in values] for keys, values in elec_consumption_count.items()}, {keys: [value * 0.9 for value in values] for keys, values in elec_consumption_area.items()})


thresholds = {'base': 0.5 * elec_consumption_max, 'medium': 0.75 * elec_consumption_max, 'peak': 0.9 * elec_consumption_max, 'very_high_peak': elec_consumption_max}
x_hours = list(range(len(elec_consumption)))


def create_fill(x, y_curve, y_min, y_max, color, name):
    x_poly = []
    y_poly = []

    for i in range(len(x)-1):
        # Werte am aktuellen Segment
        x0, x1 = x[i], x[i+1]
        y0, y1 = y_curve[i], y_curve[i+1]

        # Clipping der Werte auf y_min und y_max
        y0_clipped = np.clip(y0, y_min, y_max)
        y1_clipped = np.clip(y1, y_min, y_max)

        # Nur füllen, wenn Bereich über y_min liegt
        if y0_clipped > y_min or y1_clipped > y_min:
            x_poly.extend([x0, x1, x1, x0, None])
            y_poly.extend([y0_clipped, y1_clipped, y_min, y_min, None])

    return go.Scatter(x=x_poly, y=y_poly, fill="toself", mode='lines', line=dict(width=0), fillcolor=color, name=name)

# Plot
fig = go.Figure()

# Farbliche Flächen (von unten nach oben)
fig.add_trace(create_fill(x_hours, elec_consumption, 0, thresholds['base'], 'rgba(0,100,255,0.3)', 'base'))
fig.add_trace(create_fill(x_hours, elec_consumption, thresholds['base'], thresholds['medium'], 'rgba(0,200,0,0.3)', 'medium'))
fig.add_trace(create_fill(x_hours, elec_consumption, thresholds['medium'], thresholds['peak'], 'rgba(255,165,0,0.3)', 'peak'))
fig.add_trace(create_fill(x_hours, elec_consumption, thresholds['peak'], thresholds['very_high_peak'], 'rgba(255,0,0,0.3)', 'very_high_peak'))

# Die Haupt-Datenkurve
fig.add_trace(go.Scatter(x=x_hours, y=elec_consumption, mode='lines', name='Data Curve', line=dict(color='black', width=2)))

# Schwellenlinien
for key, val in thresholds.items():
    fig.add_trace(go.Scatter(x=[x_hours[0], x_hours[-1]], y=[val, val], mode='lines', name=f'{key} Threshold', line=dict(dash='dash', width=1, color='grey'), showlegend=False))

# Layout
fig.update_layout(title='Categorized Area Plot', xaxis_title='Hour', yaxis_title='Electricity consumption in MWh', showlegend=True)
fig.show()






#%%

total_heat_inv = 0.0

for year in years:
    total_heat_inv += eb_inv[year] + gb_inv[year] + hp_inv[year] + st_inv[year] + ieh_inv[year] + chp_inv[year]
    
    if year == visualize_year:
        break

total_heat_in = [sum(value) for value in zip(eb_heat_in[visualize_scenario][visualize_year], gb_heat_in[visualize_scenario][visualize_year], hp_heat_in[visualize_scenario][visualize_year], st_heat_in[visualize_scenario][visualize_year], ieh_heat_in[visualize_scenario][visualize_year], chp_heat_in[visualize_scenario][visualize_year])]





df_0 = pd.DataFrame({'hour': hours, 'heat_delivered': total_heat_in, 'capacity': [total_heat_inv] * len(total_heat_in)})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['heat_delivered'], mode='lines', name='Delivered heat', line=dict(color='#EF553B')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['capacity'], mode='lines', name='Capacity', line=dict(color='grey')))


fig.update_layout(title=dict(text='Flexibility potential', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()


# Unterhalb der Kapazität
under_capacity = [
    val if val <= cap else cap
    for val, cap in zip(df_0['heat_delivered'], df_0['capacity'])
]

# Oberhalb der Kapazität
over_capacity = [
    val if val > cap else None
    for val, cap in zip(df_0['heat_delivered'], df_0['capacity'])
]

# --------------------------------------
# Plot
fig = go.Figure()

# Fläche unterhalb der Kapazität
fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['heat_delivered'],
    fill='tozeroy',
    mode='none',
    name='Required capacity',
    fillcolor='rgba(0,200,0,0.3)',
    fillpattern=dict(shape='/')  # Schraffur!
))

# Schraffierte Fläche oberhalb der Kapazität
fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['capacity'],
    fill='tonexty',
    mode='none',
    name='Reserve capacity',
    fillcolor='rgba(255,0,0,0.2)',
    fillpattern=dict(shape='\\')  # Schraffur!
))

# Linien
fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['heat_delivered'],
    mode='lines',
    name='Delivered heat',
    line=dict(color='#EF553B', width=3)
))

fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['capacity'],
    mode='lines',
    name='Capacity',
    line=dict(color='grey', width=2)
))

# --------------------------------------
# Layout
fig.update_layout(
    title=dict(text='Flexibility potential', font=dict(size=30)),
    xaxis=dict(title='Hour', titlefont=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)),
    #legend_title=dict(text='Technologies', font=dict(size=20)),
    legend=dict(font=dict(size=20)),
    plot_bgcolor='white'
)

fig.show()

#CHANGE: Werte in Stundenzahl und Energiemenge berechnen


#%%

total_btes_inv = 0.0

for year in years:
    total_btes_inv += btes_inv[year]
    
    if year == visualize_year:
        break



df_5 = pd.DataFrame({'hour': hours, 'btes_absolute': btes_soc[visualize_scenario][visualize_year], 'capacity': total_btes_inv})






fig = go.Figure()

fig.add_trace(go.Scatter(x=df_5['hour'], y=df_5['btes_absolute'], mode='lines', name='SOC', line=dict(color='#EF553B')))
fig.add_trace(go.Scatter(x=df_5['hour'], y=df_5['capacity'], mode='lines', name='Capacity', line=dict(color='grey')))


fig.update_layout(title=dict(text='Flexibility potential', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()


# Unterhalb der Kapazität
under_capacity = [
    val if val <= cap else cap
    for val, cap in zip(df_5['btes_absolute'], df_5['capacity'])
]

# Oberhalb der Kapazität
over_capacity = [
    val if val > cap else None
    for val, cap in zip(df_5['btes_absolute'], df_5['capacity'])
]

#CHANGE: Werte in Stundenzahl und Energiemenge berechnen

fig = go.Figure()

# 1️⃣ Fläche von 0 bis btes_absolute (SOC)
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['btes_absolute'],
    fill='tozeroy',
    mode='none',
    name='Used capacity (SOC)',
    fillcolor='rgba(255,165,0,0.3)',
    fillpattern=dict(shape='/')  # Schraffur optional
))

# 2️⃣ Fläche zwischen btes_absolute und capacity (Reserve)
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['capacity'],
    fill='tonexty',
    mode='none',
    name='Reserve capacity',
    fillcolor='rgba(255,0,0,0.2)',
    fillpattern=dict(shape='\\')  # Andere Schraffur
))

# 3️⃣ Linie: SOC
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['btes_absolute'],
    mode='lines',
    name='SOC',
    line=dict(color='#EF553B', width=3)
))

# 4️⃣ Linie: Capacity
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['capacity'],
    mode='lines',
    name='Capacity',
    line=dict(color='grey', width=2)
))

# --------------------------------------
# Layout
fig.update_layout(
    title=dict(text='BTES Capacity Usage', font=dict(size=30)),
    xaxis=dict(title='Hour', titlefont=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title='Heat energy in MWh', titlefont=dict(size=20), tickfont=dict(size=20)),
    legend=dict(font=dict(size=20)),
    plot_bgcolor='white'
)

fig.show()


#%%

total_cool_inv = 0.0

for year in years:
    total_cool_inv += ac_inv[year] + ab_ct_inv[year] + ab_hp_inv[year] + cp_ct_inv[year] + cp_hp_inv[year]
    
    if year == visualize_year:
        break

total_cool_in = [sum(value) for value in zip(ac_cool_in[visualize_scenario][visualize_year], ab_ct_cool_in[visualize_scenario][visualize_year], ab_hp_cool_in[visualize_scenario][visualize_year], cp_ct_cool_in[visualize_scenario][visualize_year], cp_hp_cool_in[visualize_scenario][visualize_year])]





df_0 = pd.DataFrame({'hour': hours, 'cool_delivered': total_cool_in, 'capacity': [total_cool_inv] * len(total_cool_in)})

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['cool_delivered'], mode='lines', name='Delivered cool', line=dict(color='#EF553B')))
fig.add_trace(go.Scatter(x=df_0['hour'], y=df_0['capacity'], mode='lines', name='Capacity', line=dict(color='grey')))


fig.update_layout(title=dict(text='Flexibility potential', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='cool supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()


# Unterhalb der Kapazität
under_capacity = [
    val if val <= cap else cap
    for val, cap in zip(df_0['cool_delivered'], df_0['capacity'])
]

# Oberhalb der Kapazität
over_capacity = [
    val if val > cap else None
    for val, cap in zip(df_0['cool_delivered'], df_0['capacity'])
]

# --------------------------------------
# Plot
fig = go.Figure()

# Fläche unterhalb der Kapazität
fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['cool_delivered'],
    fill='tozeroy',
    mode='none',
    name='Required capacity',
    fillcolor='rgba(0,200,0,0.3)',
    fillpattern=dict(shape='/')  # Schraffur!
))

# Schraffierte Fläche oberhalb der Kapazität
fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['capacity'],
    fill='tonexty',
    mode='none',
    name='Reserve capacity',
    fillcolor='rgba(255,0,0,0.2)',
    fillpattern=dict(shape='\\')  # Schraffur!
))

# Linien
fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['cool_delivered'],
    mode='lines',
    name='Delivered cool',
    line=dict(color='#EF553B', width=3)
))

fig.add_trace(go.Scatter(
    x=df_0['hour'],
    y=df_0['capacity'],
    mode='lines',
    name='Capacity',
    line=dict(color='grey', width=2)
))

# --------------------------------------
# Layout
fig.update_layout(
    title=dict(text='Flexibility potential', font=dict(size=30)),
    xaxis=dict(title='Hour', titlefont=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title='Cold supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)),
    #legend_title=dict(text='Technologies', font=dict(size=20)),
    legend=dict(font=dict(size=20)),
    plot_bgcolor='white'
)

fig.show()

#CHANGE: Werte in Stundenzahl und Energiemenge berechnen


#%%

total_ites_inv = 0.0

for year in years:
    total_ites_inv += ites_inv[year]
    
    if year == visualize_year:
        break



df_5 = pd.DataFrame({'hour': hours, 'ites_absolute': ites_soc[visualize_scenario][visualize_year], 'capacity': total_ites_inv})






fig = go.Figure()

fig.add_trace(go.Scatter(x=df_5['hour'], y=df_5['ites_absolute'], mode='lines', name='SOC', line=dict(color='#EF553B')))
fig.add_trace(go.Scatter(x=df_5['hour'], y=df_5['capacity'], mode='lines', name='Capacity', line=dict(color='grey')))


fig.update_layout(title=dict(text='Flexibility potential', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='Heat supply in MWh/h', titlefont=dict(size=20), tickfont=dict(size=20)), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()


# Unterhalb der Kapazität
under_capacity = [
    val if val <= cap else cap
    for val, cap in zip(df_5['ites_absolute'], df_5['capacity'])
]

# Oberhalb der Kapazität
over_capacity = [
    val if val > cap else None
    for val, cap in zip(df_5['ites_absolute'], df_5['capacity'])
]

#CHANGE: Werte in Stundenzahl und Energiemenge berechnen

fig = go.Figure()

# 1️⃣ Fläche von 0 bis ites_absolute (SOC)
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['ites_absolute'],
    fill='tozeroy',
    mode='none',
    name='Used capacity (SOC)',
    fillcolor='rgba(255,165,0,0.3)',
    fillpattern=dict(shape='/')  # Schraffur optional
))

# 2️⃣ Fläche zwischen ites_absolute und capacity (Reserve)
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['capacity'],
    fill='tonexty',
    mode='none',
    name='Reserve capacity',
    fillcolor='rgba(255,0,0,0.2)',
    fillpattern=dict(shape='\\')  # Andere Schraffur
))

# 3️⃣ Linie: SOC
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['ites_absolute'],
    mode='lines',
    name='SOC',
    line=dict(color='#EF553B', width=3)
))

# 4️⃣ Linie: Capacity
fig.add_trace(go.Scatter(
    x=df_5['hour'],
    y=df_5['capacity'],
    mode='lines',
    name='Capacity',
    line=dict(color='grey', width=2)
))

# --------------------------------------
# Layout
fig.update_layout(
    title=dict(text='ITES Capacity Usage', font=dict(size=30)),
    xaxis=dict(title='Hour', titlefont=dict(size=20), tickfont=dict(size=20)),
    yaxis=dict(title='Cold energy in MWh', titlefont=dict(size=20), tickfont=dict(size=20)),
    legend=dict(font=dict(size=20)),
    plot_bgcolor='white'
)

fig.show()



#%% FIG 2 - SOC

df_4 = pd.DataFrame({'hour': hours, 'ttes_absolute': ttes_soc[visualize_scenario][visualize_year]})
df_4['ttes_relative'] = (df_4['ttes_absolute'] / df_4['ttes_absolute'].max()) * 100

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_4['hour'], y=df_4['ttes_absolute'], mode='lines', name='TTES SOC', line=dict(color='#FFA15A', width=2)))
fig.add_trace(go.Scatter(x=df_4['hour'], y=df_4['ttes_relative'], mode='lines', name='TTES SOC', line=dict(color='#FFA15A', width=2), yaxis='y2', showlegend=False))

fig.update_layout(title=dict(text='State of charge', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='State of charge in MWh', titlefont=dict(size=20), tickfont=dict(size=20), range=[0, df_4['ttes_absolute'].max() * 1.1], tickvals=np.linspace(0, df_4['ttes_absolute'].max(), 6), tickformat='.2f'), yaxis2=dict(title='State of charge in %', titlefont=dict(size=20), tickfont=dict(size=20), overlaying='y', side='right', range=[0, 100 * 1.1]), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()

df_5 = pd.DataFrame({'hour': hours, 'btes_absolute': btes_soc[visualize_scenario][visualize_year]})
df_5['btes_relative'] = (df_5['btes_absolute'] / df_5['btes_absolute'].max()) * 100

fig = go.Figure()

fig.add_trace(go.Scatter(x=df_5['hour'], y=df_5['btes_absolute'], mode='lines', name='BTES SOC', line=dict(color='#FFA15A', width=2)))
fig.add_trace(go.Scatter(x=df_5['hour'], y=df_5['btes_relative'], mode='lines', name='BTES SOC', line=dict(color='#FFA15A', width=2), yaxis='y2', showlegend=False))

fig.update_layout(title=dict(text='State of charge', font=dict(size=30)), xaxis=dict(title='Hour', tickformat=',', titlefont=dict(size=20), tickfont=dict(size=20)), yaxis=dict(title='State of charge in MWh', titlefont=dict(size=20), tickfont=dict(size=20), range=[0, df_5['btes_absolute'].max() * 1.1], tickvals=np.linspace(0, df_5['btes_absolute'].max(), 6), tickformat='.2f'), yaxis2=dict(title='State of charge in %', titlefont=dict(size=20), tickfont=dict(size=20), overlaying='y', side='right', range=[0, 100 * 1.1]), legend_title=dict(text='Technologies', font=dict(size=20)), legend=dict(font=dict(size=20)))

fig.show()



#%%



# Beispiel-Daten (Punkte pro Stunde)
data = [10, 20, 30, 50, 70, 80, 90, 100, 95, 85, 60, 30, 10]
x = list(range(len(data)))

# Schwellenwerte basierend auf Maximalwert
max_value = max(data)
thresholds = {
    '0-50%': 0.5 * max_value,
    '50-75%': 0.75 * max_value,
    '75-90%': 0.90 * max_value,
    '>90%': max_value
}

def interpolate(x0, y0, x1, y1, y_thresh):
    """Lineare Interpolation zum Finden des Schnittpunkts."""
    if y1 == y0:
        return x0  # kein Anstieg, egal welcher x-Wert
    return x0 + (y_thresh - y0) * (x1 - x0) / (y1 - y0)

def create_fill(x, y_curve, y_min, y_max, color, name):
    x_poly = []
    y_poly = []

    for i in range(len(x) - 1):
        x0, x1 = x[i], x[i+1]
        y0, y1 = y_curve[i], y_curve[i+1]

        segment_points = []

        # Punkt 1
        if y0 < y_min:
            if y1 > y_min:
                xi = interpolate(x0, y0, x1, y1, y_min)
                segment_points.append((xi, y_min))
            # sonst: komplett unter y_min -> nichts tun
        elif y0 > y_max:
            if y1 < y_max:
                xi = interpolate(x0, y0, x1, y1, y_max)
                segment_points.append((xi, y_max))
        else:
            segment_points.append((x0, y0))

        # Punkt 2
        if y1 < y_min:
            if y0 > y_min:
                xi = interpolate(x0, y0, x1, y1, y_min)
                segment_points.append((xi, y_min))
        elif y1 > y_max:
            if y0 < y_max:
                xi = interpolate(x0, y0, x1, y1, y_max)
                segment_points.append((xi, y_max))
        else:
            segment_points.append((x1, y1))

        # Wenn mindestens zwei Punkte übrig sind
        if len(segment_points) >= 2:
            # unteren Rand des Bereichs hinzufügen
            x_poly.extend([segment_points[0][0], segment_points[1][0], segment_points[1][0], segment_points[0][0], None])
            y_poly.extend([segment_points[0][1], segment_points[1][1], y_min, y_min, None])

    return go.Scatter(x=x_poly, y=y_poly, fill="toself", mode='lines', line=dict(width=0), fillcolor=color, name=name)
# Plot
fig = go.Figure()

# Farbliche Flächen (von unten nach oben)
fig.add_trace(create_fill(x, data, 0, thresholds['0-50%'], 'rgba(0,100,255,0.3)', '0-50%'))
fig.add_trace(create_fill(x, data, thresholds['0-50%'], thresholds['50-75%'], 'rgba(0,200,0,0.3)', '50-75%'))
fig.add_trace(create_fill(x, data, thresholds['50-75%'], thresholds['75-90%'], 'rgba(255,165,0,0.3)', '75-90%'))
fig.add_trace(create_fill(x, data, thresholds['75-90%'], thresholds['>90%'], 'rgba(255,0,0,0.3)', '>90%'))

# Die Haupt-Datenkurve
fig.add_trace(go.Scatter(x=x, y=data, mode='lines+markers', name='Data Curve', line=dict(color='black', width=2)))

# Schwellenlinien
for key, val in thresholds.items():
    fig.add_trace(go.Scatter(x=[x[0], x[-1]], y=[val, val], mode='lines', name=f'{key} Threshold', line=dict(dash='dash', width=1, color='grey'), showlegend=False))

# Layout
fig.update_layout(title='Categorized Area Plot', xaxis_title='Hour', yaxis_title='Value', showlegend=True)
fig.show()

#%%

import plotly.graph_objects as go

# Beispiel-Daten (Punkte pro Stunde)
data = [10, 20, 30, 50, 70, 80, 90, 100, 95, 85, 60, 30, 10]
x = list(range(len(data)))

# Schwellenwerte basierend auf Maximalwert
max_value = max(data)
thresholds = {
    '0-50%': 0.5 * max_value,
    '50-75%': 0.75 * max_value,
    '75-90%': 0.90 * max_value,
    '>90%': max_value
}

# Hilfsfunktion zum Clipping der Kurve in einem Schwellenbereich
def clipped_curve(x, y, y_min, y_max):
    y_clipped = []
    for val in y:
        if val is None or val < y_min or val > y_max:
            y_clipped.append(None)
        else:
            y_clipped.append(val)
    return y_clipped

# Plot
fig = go.Figure()

# Farbliche Flächen mit 'tozeroy' für Bereichsfüllung
fig.add_trace(go.Scatter(
    x=x,
    y=clipped_curve(x, data, 0, thresholds['0-50%']),
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,100,255,0.3)',
    name='0-50%'
))

fig.add_trace(go.Scatter(
    x=x,
    y=clipped_curve(x, data, thresholds['0-50%'], thresholds['50-75%']),
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(0,200,0,0.3)',
    name='50-75%'
))

fig.add_trace(go.Scatter(
    x=x,
    y=clipped_curve(x, data, thresholds['50-75%'], thresholds['75-90%']),
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,165,0,0.3)',
    name='75-90%'
))

fig.add_trace(go.Scatter(
    x=x,
    y=clipped_curve(x, data, thresholds['75-90%'], thresholds['>90%']),
    fill='tozeroy',
    mode='none',
    fillcolor='rgba(255,0,0,0.3)',
    name='>90%'
))

# Die Haupt-Datenkurve
fig.add_trace(go.Scatter(
    x=x,
    y=data,
    mode='lines+markers',
    name='Data Curve',
    line=dict(color='black', width=2)
))

# Schwellenlinien hinzufügen
for key, val in thresholds.items():
    fig.add_trace(go.Scatter(
        x=[x[0], x[-1]],
        y=[val, val],
        mode='lines',
        line=dict(dash='dash', color='grey', width=1),
        showlegend=False
    ))

# Layout
fig.update_layout(
    title='Categorized Area Plot',
    xaxis_title='Hour',
    yaxis_title='Value',
    showlegend=True,
    plot_bgcolor='rgba(240,240,255,0.4)'
)

fig.show()


