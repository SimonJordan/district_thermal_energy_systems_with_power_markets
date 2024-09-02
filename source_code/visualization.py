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
x = list(range(10))
y1 = [2 * i + 1 for i in x]  # Erste Gerade
y2 = [3 * i + 2 for i in x]  # Zweite Gerade

# Erstellen der Linien und der gefüllten Fläche
fig = go.Figure()

# Erste Linie
fig.add_trace(go.Scatter(
    x=x, y=y1,
    mode='lines',
    name='y1 = 2x + 1'
))

# Zweite Linie
fig.add_trace(go.Scatter(
    x=x, y=y2,
    mode='lines',
    name='y2 = 3x + 2'
))

# Fläche zwischen den Linien füllen
fig.add_trace(go.Scatter(
    x=x + x[::-1],  # x-Koordinaten für die Fläche (hin und zurück)
    y=y1 + y2[::-1],  # y1 gefolgt von y2 in umgekehrter Reihenfolge
    fill='toself',
    fillcolor='gray',
    opacity=0.5,
    line=dict(color='gray'),
    showlegend=False
))

# Layout anpassen
fig.update_layout(
    title="Gefüllte Fläche zwischen zwei Geraden",
    xaxis_title="x",
    yaxis_title="y"
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

#%%

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Erstellen der Subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

# Hinzufügen der Daten zu den Subplots
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines', name='Plot 1'), row=1, col=1)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[6, 5, 4], mode='lines', name='Plot 2'), row=1, col=2)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 3, 4], mode='lines', name='Plot 3'), row=2, col=1)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 3, 2], mode='lines', name='Plot 4'), row=2, col=2)

# Layout anpassen
fig.update_layout(height=600, width=600, title_text="Subplots Example")

# Zeige das Diagramm
fig.show()

fig = make_subplots(
    rows=2, cols=2,
    specs=[[{"colspan": 2}, None], [{"colspan": 1}, {"colspan": 1}]],
    subplot_titles=("Breiter Plot", "Plot 2", "Plot 3")
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines', name='Breiter Plot'), row=1, col=1)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[6, 5, 4], mode='lines', name='Plot 2'), row=2, col=1)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 3, 4], mode='lines', name='Plot 3'), row=2, col=2)

fig.update_layout(height=600, width=800, title_text="Flexible Subplots Example")
fig.show()

#%%

import plotly.graph_objects as go

# Daten für den Plot
x = [0.5, 2, 4, 10]  # x-Position der Balken (die Mitte des Balkens)
y = [10, 20, 15, 25]  # Höhe der Balken
widths = [1, 2, 2, 6]  # Individuelle Breiten der Balken
bases = [5, 10, 7, 15]  # Startpunkte der Balken auf der y-Achse
labels = ['Balken 1', 'Balken 2', 'Balken 3', 'Balken 4']  # Namen der Balken

# Erstellen der Balken mit unterschiedlicher Breite und benutzerdefinierten Startpunkten
fig = go.Figure()

# Schleife über die Balken, um sie individuell hinzuzufügen
for i in range(len(x)):
    fig.add_trace(go.Bar(
        x=[x[i]],  # Einzelne x-Position
        y=[y[i]],  # Einzelne Höhe
        width=widths[i],  # Breite des Balkens
        base=bases[i],  # Startpunkt des Balkens
        text=labels[i],  # Textlabel des Balkens
        textposition='outside',  # Position des Textes (außerhalb unterhalb des Balkens)
        textangle=0,  # Winkel des Textes (horizontal)
        name=labels[i]  # Optional: Name des Balkens
    ))

# Layout anpassen
fig.update_layout(
    title="Balken mit unterschiedlichen Breiten und benutzerdefinierten Startpunkten",
    xaxis=dict(title='X-Achse'),
    yaxis=dict(title='Y-Achse'),
    barmode='overlay',  # Balken übereinander legen, aber mit unterschiedlichen Positionen
    bargap=0,  # Kein Abstand zwischen den Balken
)

# Zeige das Diagramm
fig.show()

