import pandas as pd
import os

def filter_day_ahead_prices(file_name, sheet_name=0):
    cur_dir = os.path.dirname(__file__)
    path_to_data_folder = os.path.join(cur_dir, '..', 'data')
    file_path = os.path.join(path_to_data_folder, file_name)

    output_path = file_path.replace('.csv', '_processed.csv')

    # Datei öffnen, alle " entfernen und temporär im Speicher bereinigen
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('"', '')  # Alle " entfernen

    # Jetzt Datei aus dem bereinigten String einlesen
    from io import StringIO
    df = pd.read_csv(StringIO(content), sep=',')  # Komma als Trenner

    # Debug: Spalten prüfen
    print("Spalten:", df.columns.tolist())

    col_name = 'Day-ahead Price (EUR/MWh)'

    # Float-Konvertierung
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    filtered = df[[col_name]].dropna()

    # Speichern mit Komma als Dezimaltrennzeichen
    filtered.to_csv(output_path, index=False, decimal=',')

    print(f"{len(filtered)} Werte gespeichert in '{output_path}'.")

# Aufruf
filter_day_ahead_prices('day_ahead_prices_norway_2024.csv', 'Sheet1')
