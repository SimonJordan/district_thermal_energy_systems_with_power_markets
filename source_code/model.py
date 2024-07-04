import os
import io
import sys
import time
import datetime
import pandas as pd
import pyomo.environ as py

start_time = time.time()
current_time = datetime.datetime.now()
formatted_time = current_time.strftime('%H:%M')
print('Start of the script at:', formatted_time)

scenarios = ['basic']
years = [2025, 2030, 2035, 2040, 2045, 2050]
demand_baltimore = {}
electricity_price = {}
data_eb = {}
data_ttes = {}
data = {}

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, 'data')
path_to_file_demand_baltimore = os.path.join(path_to_input_folder, 'demand_baltimore.xlsx')
path_to_file_electricity_price = os.path.join(path_to_input_folder, 'electricity_price.xlsx')
path_to_file_eb = os.path.join(path_to_input_folder, 'eb.xlsx')
path_to_file_ttes = os.path.join(path_to_input_folder, 'ttes.xlsx')

for year in years:
    df_demand_baltimore = pd.read_excel(path_to_file_demand_baltimore, sheet_name=str(year))
    df_electricity_price = pd.read_excel(path_to_file_electricity_price, sheet_name=str(year))
    df_eb = pd.read_excel(path_to_file_eb, sheet_name=str(year))
    df_ttes = pd.read_excel(path_to_file_ttes, sheet_name=str(year))
    hours_per_year = df_demand_baltimore['hour'].tolist()
    demand_baltimore_per_year = df_demand_baltimore['demand_baltimore'].tolist()
    demand_baltimore[year] = (hours_per_year, demand_baltimore_per_year)
    electricity_price_per_year = df_electricity_price['electricity_price'].tolist()
    electricity_price[year] = (hours_per_year, electricity_price_per_year)
    p_eb_eta = df_eb['p_eb_eta'].tolist()[0]
    p_eb_c_inv = df_eb['p_eb_c_inv'].tolist()[0]
    data_eb[year] = {'p_eb_eta' : p_eb_eta, 'p_eb_c_inv' : p_eb_c_inv}
    p_ttes_losses = df_ttes['p_ttes_losses'].tolist()[0]
    p_ttes_eta = df_ttes['p_ttes_eta'].tolist()[0]
    p_ttes_init = df_ttes['p_ttes_init'].tolist()[0]
    p_ttes_end = df_ttes['p_ttes_end'].tolist()[0]
    p_ttes_c_inv = df_ttes['p_ttes_c_inv'].tolist()[0]
    p_ttes_elec = df_ttes['p_ttes_elec'].tolist()[0]
    data_ttes[year] = {'p_ttes_losses' : p_ttes_losses, 'p_ttes_eta' : p_ttes_eta, 'p_ttes_init' : p_ttes_init, 'p_ttes_end' : p_ttes_end, 'p_ttes_c_inv' : p_ttes_c_inv, 'p_ttes_elec' : p_ttes_elec}

data['basic'] = [demand_baltimore, electricity_price, data_eb, data_ttes]
data_structure = {'scenarios': scenarios, 'years': years, 'hours': hours_per_year}
model_name = 'FLXenabler'

model = py.ConcreteModel()
model.name = model_name
model.set_scenarios = py.Set(initialize=data_structure['scenarios'])
model.set_years = py.Set(initialize=data_structure['years'])
model.set_hours = py.Set(initialize=data_structure['hours'])
model.data_values = data

from eb import add_eb_variables, add_eb_parameters, add_eb_equations
add_eb_parameters(model)
add_eb_variables(model)
add_eb_equations(model)

from ttes import add_ttes_variables, add_ttes_parameters, add_ttes_equations
add_ttes_parameters(model)
add_ttes_variables(model)
add_ttes_equations(model)


def demand_balance(m, y, t, s):
    return m.v_eb_q_heat_in[y, t, s] + m.v_ttes_q_thermal_in[y, t, s] - m.v_ttes_q_thermal_out[y, t, s] == model.data_values[s][0][y][1][t]

model.con_demand_balance = py.Constraint(model.set_years, model.set_hours, model.set_scenarios, rule=demand_balance)

def objective_function(m):
    return sum(m.v_eb_c_fix[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_eb_c_var[y, t, s] for y in m.set_years for t in m.set_hours for s in m.set_scenarios) + \
           sum(m.v_ttes_c_fix[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ttes_c_var[y, s] for y in m.set_years for s in m.set_scenarios)# + \
           #sum(m.v_ttes_c_penalty[y, t, s] for y in m.set_years for t in m.set_hours for s in m.set_scenarios)

model.obj = py.Objective(expr=objective_function, sense=py.minimize)
solver = py.SolverFactory('gurobi')
#solver.options['NonConvex'] = 2
solution = solver.solve(model)




#DEMAND FEHLT

#OBJECTIV FUNCTION reperaieren (+ttes mit stromkosten bei variable mit t ändern)
#nichtlinear beseitigen in ttes (cop)
#data statt liste dictionary verwenden
#eb limitieren, damit speicher verwendet wird
#einheiten überprüfen
#ttes stromkosten für wärmepumpe
#ttes das mit 1 prozent von maximaler größe funktioniert in gleichung nicht, weil von t abhängig
#ev tupel löschen

# Speichern der aktuellen Standardausgabe
original_stdout = sys.stdout

# Erstellen eines StringIO-Objekts, um die Ausgabe zu speichern
captured_output = io.StringIO()
sys.stdout = captured_output  # Umleiten der Standardausgabe auf das StringIO-Objekt

# Aufruf der display-Methode des Modells
model.display()

# Wiederherstellen der ursprünglichen Standardausgabe
sys.stdout = original_stdout

# Den Inhalt des StringIO-Objekts in eine Datei schreiben
output = captured_output.getvalue()
with open('output.txt', 'w') as f:
    f.write(output)




print(solution)

end_time = time.time()
elapsed_time = end_time - start_time
hours = elapsed_time // 3600
minutes = (elapsed_time % 3600) // 60
seconds = elapsed_time % 60

print('Script execution time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours, minutes, seconds))