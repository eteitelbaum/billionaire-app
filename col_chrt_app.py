import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Load the data
df = pd.read_csv('billionaires_with_country_data.csv')

# Preprocess the data
df['year'] = pd.to_datetime(df['year'], format='%Y')
df['net_worth'] = pd.to_numeric(df['net_worth'], errors='coerce')

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    html.H1("Top 30 Billionaires Wealth Over Time", className="text-center mt-4 mb-4"),
    dcc.Graph(id="wealth-chart"),
    dcc.Slider(
        id="year-slider",
        min=df['year'].dt.year.min(),
        max=df['year'].dt.year.max(),
        value=df['year'].dt.year.min(),
        marks={str(year): str(year) for year in range(df['year'].dt.year.min(), df['year'].dt.year.max()+1)},
        step=None
    ),
    dbc.Button("Play", id="play-button", className="mt-3"),
    dcc.Interval(id="animation-interval", interval=1000, n_intervals=0, disabled=True)
])

# Define the callbacks
# Function to get flag emoji from ISO3 code
def get_flag_emoji(iso3):
    if pd.isna(iso3) or len(iso3) != 3:
        return ''
    # Convert ISO3 to ISO2
    iso2 = iso3[:2]
    return ''.join(chr(ord(c) + 127397) for c in iso2)

# Update the update_chart function
@callback(
    Output("wealth-chart", "figure"),
    Input("year-slider", "value")
)
def update_chart(selected_year):
    # Filter data for the selected year
    year_df = df[df['year'].dt.year == selected_year]
    
    # Get top 30 billionaires for this year
    top_30 = year_df.nlargest(30, 'net_worth')
    
    # Add flag emojis to names
    top_30['name_with_flag'] = top_30.apply(lambda row: f"{get_flag_emoji(row['iso3c'])} {row['full_name']}", axis=1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_30['name_with_flag'],
        x=top_30['net_worth'],
        orientation='h',
        text=top_30['net_worth'],
        texttemplate='%{text:.2s}',
        textposition='outside',
    ))
    
    fig.update_layout(
        title=f"Top 30 Billionaires Net Worth in {selected_year}",
        xaxis_title="Net Worth (USD)",
        yaxis_title="Billionaire",
        height=800,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

@callback(
    Output("year-slider", "value"),
    Output("animation-interval", "disabled"),
    Input("play-button", "n_clicks"),
    Input("animation-interval", "n_intervals"),
    Input("year-slider", "value"),
    prevent_initial_call=True
)
def control_animation(n_clicks, n_intervals, current_year):
    triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "play-button":
        return current_year, False
    elif triggered_id == "animation-interval":
        next_year = min(current_year + 1, df['year'].dt.year.max())
        if next_year == df['year'].dt.year.max():
            return next_year, True
        return next_year, False
    else:
        return current_year, True

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
