import os
import pandas as pd

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, 'data')
path_to_text_files = os.path.join(path_to_input_folder, 'Districts', 'sum')
# path_to_output_file_heating = os.path.join(path_to_input_folder, 'districts_heating_demand.xlsx')
# path_to_output_file_cooling = os.path.join(path_to_input_folder, 'districts_cooling_demand.xlsx')
# file_names = [f'Building_{i}.txt' for i in range(1, 40)]
# path_to_output_file_heating = os.path.join(path_to_input_folder, 'districts_heating_demand_phase0.xlsx')
# path_to_output_file_cooling = os.path.join(path_to_input_folder, 'districts_cooling_demand_phase0.xlsx')
# file_names = [f'Building_{i}.txt' for i in [1, 2, 3, 4, 5, 6, 8, 9, 12, 14, 19, 23, 26, 27, 32, 33, 36, 38]]
# path_to_output_file_heating = os.path.join(path_to_input_folder, 'districts_heating_demand_phase1.xlsx')
# path_to_output_file_cooling = os.path.join(path_to_input_folder, 'districts_cooling_demand_phase1.xlsx')
# file_names = [f'Building_{i}.txt' for i in [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 38]]
path_to_output_file_heating = os.path.join(path_to_input_folder, 'districts_heating_demand_phase2.xlsx')
path_to_output_file_cooling = os.path.join(path_to_input_folder, 'districts_cooling_demand_phase2.xlsx')
file_names = [f'Building_{i}.txt' for i in range(1, 40)]

data_heating = {'hour': list(range(8760))}
data_cooling = {'hour': list(range(8760))}

for file_name in file_names:
    building_data_heating = []
    building_data_cooling = []
    path_to_text_file = os.path.join(path_to_text_files, file_name)

    with open(path_to_text_file, 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            value_cooling = abs(float(parts[1])) / 1000000
            value_heating = (float(parts[2]) + float(parts[3])) / 1000000
            building_data_heating.append(value_heating)
            building_data_cooling.append(value_cooling)
    data_heating[f'heating_demand_{file_name.split(".")[0].lower()}'] = building_data_heating
    data_cooling[f'cooling_demand_{file_name.split(".")[0].lower()}'] = building_data_cooling

df_heating = pd.DataFrame(data_heating)
df_cooling = pd.DataFrame(data_cooling)
df_heating['heating_demand_sum'] = df_heating.loc[:, df_heating.columns != 'hour'].sum(axis=1)
df_cooling['cooling_demand_sum'] = df_cooling.loc[:, df_cooling.columns != 'hour'].sum(axis=1)
df_heating.to_excel(path_to_output_file_heating, index=False)
df_cooling.to_excel(path_to_output_file_cooling, index=False)