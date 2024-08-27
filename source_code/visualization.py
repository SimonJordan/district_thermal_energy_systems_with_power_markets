import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

# Setze den Renderer auf 'browser'
pio.renderers.default = 'browser'

# Beispiel-Daten erstellen
hours = list(range(8760))  # 8760 Stunden im Jahr
demand = [100] * 8760  # Konstanter Demand für Einfachheit (ersetze dies mit deinen echten Daten)
tech1 = [30] * 8760  # Beispiel-Daten für Technologie 1 (ersetze dies mit deinen echten Daten)
tech2 = [50] * 8760  # Beispiel-Daten für Technologie 2 (ersetze dies mit deinen echten Daten)
tech3 = [20] * 8760  # Beispiel-Daten für Technologie 3 (ersetze dies mit deinen echten Daten)

# DataFrame erstellen
df = pd.DataFrame({
    'hour': hours,
    'demand': demand,
    'tech1': tech1,
    'tech2': tech2,
    'tech3': tech3
})

# Plotly-Figur erstellen
fig = go.Figure()

# Gestapelte Flächen für jede Technologie hinzufügen
fig.add_trace(go.Scatter(x=df['hour'], y=df['tech1'], fill='tozeroy', name='Technologie 1'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['tech2'], fill='tonexty', name='Technologie 2'))
fig.add_trace(go.Scatter(x=df['hour'], y=df['tech3'], fill='tonexty', name='Technologie 3'))

# Diagramm-Layout anpassen
fig.update_layout(
    title='Beitrag der Technologien zur Deckung des Demand',
    xaxis_title='Stunden',
    yaxis_title='Leistung',
    legend_title='Technologien'
)

# Diagramm anzeigen
fig.show()

#%%
import plotly.graph_objects as go
import pandas as pd

# Beispiel-Daten
data = {
    'Datetime': pd.date_range(start='2023-01-01', periods=10, freq='H'),
    'Demand': [100, 120, 150, 130, 140, 170, 160, 180, 190, 200],
    'Renewable': [30, 40, 45, 35, 50, 55, 60, 65, 70, 75],
    'Non-Renewable': [70, 80, 105, 95, 90, 115, 100, 115, 120, 125]
}

df = pd.DataFrame(data)

# Erstellen des gestapelten Flächenplots
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Datetime'], 
    y=df['Renewable'], 
    mode='lines', 
    name='Renewable',
    stackgroup='one'  # Diese Option sorgt für das Stapeln der Flächen
))

fig.add_trace(go.Scatter(
    x=df['Datetime'], 
    y=df['Non-Renewable'], 
    mode='lines', 
    name='Non-Renewable',
    stackgroup='one'  # Gleiche stackgroup, um die Flächen zu stapeln
))

# Hinzufügen der Demand-Linie
fig.add_trace(go.Scatter(
    x=df['Datetime'], 
    y=df['Demand'], 
    mode='lines', 
    name='Demand',
    line=dict(color='black', width=2, dash='dash')
))

# Layout-Anpassungen
fig.update_layout(
    title='Energiebedarf und Erzeugung',
    xaxis_title='Datum',
    yaxis_title='Energie (MWh)',
    legend_title='Legende'
)

# Plot anzeigen
fig.show()

#%%


import plotly.graph_objects as go

# Beispiel-Daten
categories = ['A', 'B', 'C', 'D']
values_1 = [10, 20, 30, 40]
values_2 = [15, 25, 35, 20]
values_3 = [25, 10, 15, 30]

# Erstellen des gestapelten Balkendiagramms
fig = go.Figure()

# Füge die einzelnen Kategorien hinzu
fig.add_trace(go.Bar(x=categories, y=values_1, name='Serie 1'))
fig.add_trace(go.Bar(x=categories, y=values_2, name='Serie 2'))
fig.add_trace(go.Bar(x=categories, y=values_3, name='Serie 3'))

# Konfiguration für gestapeltes Diagramm
fig.update_layout(barmode='stack')

# Zeige das Diagramm
fig.show()

