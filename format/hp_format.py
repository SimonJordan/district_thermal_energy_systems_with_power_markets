import os
import pandas as pd

def replace_zeros_with_mean(filename, column_name, output_filename):
    cur_dir = os.path.dirname(__file__)
    path_to_data_folder = os.path.join(cur_dir, '..', 'data')
    path_to_file_hp_cop = os.path.join(path_to_data_folder, filename)
    path_to_file_output = os.path.join(path_to_data_folder, output_filename)

    df = pd.read_excel(path_to_file_hp_cop)
    zero_indices = df.index[df[column_name] == 0].tolist()

    # for idx in zero_indices:
    #     prev_value = df.loc[:idx-1, column_name][df[column_name] != 0].iloc[-1]
    #     next_value = df.loc[idx+1:, column_name][df[column_name] != 0].iloc[0]
        
    #     mean_value = (prev_value + next_value) / 2
    #     df.at[idx, column_name] = mean_value
    
    i = 0
    while i < len(zero_indices):
        start_idx = zero_indices[i]
        if start_idx == 0:
            prev_value = 0
        else:
            prev_value = df.loc[:start_idx-1, column_name][df[column_name] != 0].iloc[-1]
        end_idx = start_idx
        while end_idx + 1 in zero_indices:
            end_idx += 1
        if end_idx + 1 >= len(df):
            next_value = prev_value
        else:
            next_value = df.loc[end_idx+1:, column_name][df[column_name] != 0].iloc[0]
        num_zeros = end_idx - start_idx + 1
        increment = (next_value - prev_value) / (num_zeros + 1)
        for j in range(num_zeros):
            df.at[start_idx + j, column_name] = prev_value + (j + 1) * increment
        i += num_zeros
    
    df.to_excel(path_to_file_output, index=False)

replace_zeros_with_mean('hp_cop.xlsx', 'p_hp_cop', 'hp_cop_format.xlsx')