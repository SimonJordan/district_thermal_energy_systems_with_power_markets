import pandas as pd
import re
import os

def clean_and_extract_column(file_name, sheet_name=0):
    cur_dir = os.path.dirname(__file__)
    path_to_data_folder = os.path.join(cur_dir, '..', 'data')
    file_path = os.path.join(path_to_data_folder, file_name)
    
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
    time_pattern = re.compile(r'^\d{2}:\d{2} - \d{2}:\d{2}$')

    df_filtered = df.iloc[7:]
    df_filtered = df_filtered[df_filtered.iloc[:, 0].apply(lambda x: bool(time_pattern.match(str(x))) if pd.notna(x) else False)]
    df_result = df_filtered.iloc[:, [1]].copy()
    df_result.insert(0, 'hour', range(len(df_result)))
    df_result.iloc[:, 1] = df_result.iloc[:, 1].astype(str).str.replace('.', ',', regex=False)
    df_result.columns = ['hour', 'price']

    output_path = file_path.replace('.xlsx', '_processed.xlsx')
    df_result.to_excel(output_path, index=False)

    print(f"Gefilterte Datei gespeichert als: {output_path}")

clean_and_extract_column('day_ahead_prices_norway_2023.xlsx', 'Sheet1')
