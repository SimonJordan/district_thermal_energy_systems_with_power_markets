import os
import pandas as pd

def replace_zeros_with_mean(filename, columns_1, columns_2, output_filename_1, output_filename_2):
    cur_dir = os.path.dirname(__file__)
    path_to_data_folder = os.path.join(cur_dir, '..', 'data')
    path_to_file_csv = os.path.join(path_to_data_folder, filename)
    path_to_file_output_1 = os.path.join(path_to_data_folder, output_filename_1)
    path_to_file_output_2 = os.path.join(path_to_data_folder, output_filename_2)

    data = pd.read_csv(path_to_file_csv)

    heating_data = data[columns_1]
    heating_data.insert(0, 'hour', range(len(heating_data)))
    heating_data.to_excel(path_to_file_output_1, index=False)
    
    cooling_data = data[columns_2]
    cooling_data.insert(0, 'hour', range(len(cooling_data)))
    cooling_data.to_excel(path_to_file_output_2, index=False)
    
columns_1 = [f'Heating:Electricity Building {i}' for i in range(1, 40)]
columns_2 = [f'Cooling:Electricity Building {i}' for i in range(1, 40)]
replace_zeros_with_mean('power_60min.csv', columns_1, columns_2, 'power_60min_heating_format.xlsx', 'power_60min_cooling_format.xlsx')