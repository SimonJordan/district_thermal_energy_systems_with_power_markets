import os
import pandas as pd

cur_dir = os.path.dirname(__file__)
path_to_input_folder = os.path.join(cur_dir, 'data')
path_to_file_pjm = os.path.join(path_to_input_folder, 'pjm_real_time_prices.csv')
path_to_file_pjm_bge = os.path.join(path_to_input_folder, 'pjm_real_time_prices_bge.csv')


df = pd.read_csv(path_to_file_pjm)
filtered_df = df[df['pnode_name'] == 'BGE']['total_lmp_rt']
filtered_df = filtered_df.apply(lambda x: f"{x:.2f}".replace('.', ','))
filtered_df.to_csv(path_to_file_pjm_bge, index=False)
