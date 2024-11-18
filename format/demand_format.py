import os
import pandas as pd

def loads_format(filename, columns_1, columns_2, columns_3, output_filename_1, output_filename_2):
    cur_dir = os.path.dirname(__file__)
    path_to_data_folder = os.path.join(cur_dir, '..', 'data', 'flxenabler-loads-v2')
    path_to_file_csv = os.path.join(path_to_data_folder, filename)
    path_to_file_output_1 = os.path.join(path_to_data_folder, '..', output_filename_1)
    path_to_file_output_2 = os.path.join(path_to_data_folder, '..', output_filename_2)

    data = pd.read_csv(path_to_file_csv)
    
    cooling_load = data[columns_1]
    cooling_data = cooling_load.map(lambda x: abs(x) / 1_000_000 if isinstance(x, (int, float)) else 0)
    cooling_data.insert(0, 'hour', range(len(cooling_data)))
    cooling_data.to_excel(path_to_file_output_1, index=False)
    
    heating_data = pd.DataFrame()

    for heating, hotwater in zip(columns_2, columns_3):
        if heating in data.columns and hotwater in data.columns:
            heating_data[heating] = data[heating].abs() / 1_000_000 + data[hotwater].abs() / 1_000_000
    
    heating_data.insert(0, 'hour', range(len(heating_data)))
    heating_data.to_excel(path_to_file_output_2, index=False)
    
columns_1 = [f'TotalCoolingSensibleLoad (W) Building {i}' for i in range(1, 36) if i != 20]
columns_2 = [f'TotalHeatingSensibleLoad (W) Building {i}' for i in range(1, 36) if i != 20]
columns_3 = [f'TotalWaterHeating (W) Building {i}' for i in range(1, 36) if i != 20]
loads_format('loads_60min.csv', columns_1, columns_2, columns_3, 'loads_60min_cooling.xlsx', 'loads_60min_heating.xlsx')
