import os
import io
import sys
import time
import datetime
import numpy as np
import pandas as pd
import pyomo.environ as py

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

scenarios = ['basic']
years = [2025, 2030, 2035, 2040, 2045, 2050]
demand_baltimore = {}
electricity_price = {}
electricity_mean_price = {}
data_eb = {}
data_hp = {}
data_ttes = {}
data = {}

#-----------------------------------------------------------------------------#
#                                                                             #
# setting file paths for reading the data                                     #
#                                                                             #
#-----------------------------------------------------------------------------#

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, 'data')
path_to_file_demand_baltimore = os.path.join(path_to_input_folder, 'demand_baltimore.xlsx')
path_to_file_electricity_price = os.path.join(path_to_input_folder, 'electricity_price.xlsx')
path_to_file_eb = os.path.join(path_to_input_folder, 'eb.xlsx')
path_to_file_hp = os.path.join(path_to_input_folder, 'hp.xlsx')
path_to_file_hp_cop = os.path.join(path_to_input_folder, 'hp_cop.xlsx')
path_to_file_ttes = os.path.join(path_to_input_folder, 'ttes.xlsx')

#-----------------------------------------------------------------------------#
#                                                                             #
# reading the input data                                                      #
#                                                                             #
#-----------------------------------------------------------------------------#

for year in years:
    df_demand_baltimore = pd.read_excel(path_to_file_demand_baltimore, sheet_name=str(year))
    df_electricity_price = pd.read_excel(path_to_file_electricity_price, sheet_name=str(year))
    df_eb = pd.read_excel(path_to_file_eb, sheet_name=str(year))
    df_hp = pd.read_excel(path_to_file_hp, sheet_name=str(year))
    df_hp_cop = pd.read_excel(path_to_file_hp_cop, sheet_name=str(year))
    df_ttes = pd.read_excel(path_to_file_ttes, sheet_name=str(year))
    hours_per_year = df_demand_baltimore['hour'].tolist()
    demand_baltimore[year] = df_demand_baltimore['demand_baltimore'].tolist()
    electricity_price[year] = df_electricity_price['electricity_price'].tolist()
    electricity_mean_price[year] = np.mean(electricity_price[year])
    p_eb_eta = df_eb['p_eb_eta'].tolist()[0]
    p_eb_c_inv = df_eb['p_eb_c_inv'].tolist()[0]
    p_eb_c_fix = df_eb['p_eb_c_fix'].tolist()[0]
    data_eb[year] = {'p_eb_eta' : p_eb_eta, 'p_eb_c_inv' : p_eb_c_inv, 'p_eb_c_fix': p_eb_c_fix}
    p_hp_c_inv = df_hp['p_hp_c_inv'].tolist()[0]
    p_hp_c_fix = df_hp['p_hp_c_fix'].tolist()[0]
    p_hp_cop = df_hp_cop['p_hp_cop'].tolist()
    data_hp[year] = {'p_hp_c_inv' : p_hp_c_inv, 'p_hp_c_fix' : p_hp_c_fix, 'p_hp_cop': p_hp_cop}
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

data['basic'] = {'demand': demand_baltimore, 'electricity_price': electricity_price, 'electricity_mean_price': electricity_mean_price, 'eb': data_eb, 'hp': data_hp, 'ttes': data_ttes}
data_structure = {'scenarios': scenarios, 'years': years, 'hours': hours_per_year}
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

#-----------------------------------------------------------------------------#
#                                                                             #
# adding the parameters, variables and equations of the storage technologies  #
#                                                                             #
#-----------------------------------------------------------------------------#

from ttes import add_ttes_variables, add_ttes_parameters, add_ttes_equations
add_ttes_parameters(model)
add_ttes_variables(model)
add_ttes_equations(model)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting the demand balance equation                                         #
#                                                                             #
#-----------------------------------------------------------------------------#

def demand_balance(m, y, t, s):
    return m.v_eb_q_heat_in[y, t, s] + m.v_hp_q_heat_in[y, t, s] + m.v_ttes_q_thermal_in[y, t, s] - m.v_ttes_q_thermal_out[y, t, s] == model.data_values[s]['demand'][y][t]

model.con_demand_balance = py.Constraint(model.set_years, model.set_hours, model.set_scenarios, rule=demand_balance)

#-----------------------------------------------------------------------------#
#                                                                             #
# setting objective function                                                  #
#                                                                             #
#-----------------------------------------------------------------------------#

def objective_function(m):
    return sum(m.v_eb_c_inv[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_eb_c_fix[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_eb_c_var[y, t, s] for y in m.set_years for t in m.set_hours for s in m.set_scenarios) + \
           sum(m.v_hp_c_inv[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_hp_c_fix[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_hp_c_var[y, t, s] for y in m.set_years for t in m.set_hours for s in m.set_scenarios) + \
           sum(m.v_ttes_c_inv[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ttes_c_fix[y, s] for y in m.set_years for s in m.set_scenarios) + sum(m.v_ttes_c_var[y, t, s] for y in m.set_years for t in m.set_hours for s in m.set_scenarios)

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

print('Script intermediate time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_1, minutes_1, seconds_1))

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
# setting end point for runtime measurement                                   #
#                                                                             #
#-----------------------------------------------------------------------------#

end_time = time.time()
elapsed_time_2 = end_time - start_time
hours_2 = elapsed_time_2 // 3600
minutes_2 = (elapsed_time_2 % 3600) // 60
seconds_2 = elapsed_time_2 % 60

print('Script solving time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours_2, minutes_2, seconds_2))

seconds = seconds_1 + seconds_2
minutes = minutes_1 + minutes_2 + seconds // 60
seconds = seconds % 60
hours = hours_1 + hours_2 + minutes // 60
minutes = minutes % 60

print('Script execution time: {:.0f} h ; {:.0f} min ; {:.0f} sec'.format(hours, minutes, seconds))